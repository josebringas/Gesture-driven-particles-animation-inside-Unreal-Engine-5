import cv2
import time
from cvzone.ColorModule import ColorFinder
import cvzone
from pythonosc.udp_client import SimpleUDPClient
import mediapipe as mp
from collections import deque

# ------------------------ Camera setup ------------------------
widthCam, heightCam = 640, 480
cap = cv2.VideoCapture(1)
cap.set(3, widthCam)
cap.set(4, heightCam)

# ------------------------ Color detection setup ------------------------
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 29, 'smin': 74, 'vmin': 45, 'hmax': 53, 'smax': 246, 'vmax': 255} #works for my sample!

# ------------------------ OSC setup ------------------------
osc_ip = "127.0.0.1"
osc_port = 8000
osc_client = SimpleUDPClient(osc_ip, osc_port)

# ------------------------ Smoothing factors ------------------------
alpha_pos = 0.3
alpha_area = 0.7
smoothed_x = smoothed_y = smoothed_area = smoothed_hand_area = None

# ------------------------ Deque for depth smoothing ------------------------
depth_history = deque(maxlen=5)

# ------------------------ Safe zone ------------------------
frame_reduction = 50
safe_left = frame_reduction
safe_top = frame_reduction
safe_right = widthCam - frame_reduction
safe_bottom = heightCam - frame_reduction
safe_width = safe_right - safe_left
safe_height = safe_bottom - safe_top

# ------------------------ FPS timing ------------------------
prev_time = time.time()

# ------------------------ MediaPipe setup ------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# ------------------------ Normalize helper ------------------------
def normalize(val, min_val, max_val):
    return max(0.0, min(1.0, (val - min_val) / (max_val - min_val)))

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    area_hand = 0
    rel_x, rel_y, relative_depth = 0, 0, 0

    # ------------------------ Draw Safe Zone ------------------------
    cv2.rectangle(frame, (safe_left, safe_top), (safe_right, safe_bottom), (255, 0, 255), 2)

    # ------------------------ MediaPipe Hand Detection ------------------------
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_coords = [lm.x for lm in hand_landmarks.landmark]
            y_coords = [lm.y for lm in hand_landmarks.landmark]

            x_min = int(min(x_coords) * widthCam)
            y_min = int(min(y_coords) * heightCam)
            x_max = int(max(x_coords) * widthCam)
            y_max = int(max(y_coords) * heightCam)

            raw_area = (x_max - x_min) * (y_max - y_min)

            smoothed_hand_area = (
                alpha_area * raw_area + (1 - alpha_area) * smoothed_hand_area
                if smoothed_hand_area else raw_area
            )
            area_hand = normalize(smoothed_hand_area, 10000, 30000)

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, f"MP Area: {area_hand:.2f}", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # ------------------------ Color Detection ------------------------
    imgColor, mask = myColorFinder.update(frame, hsvVals)
    imgContour, contours = cvzone.findContours(frame, mask, minArea=300)

    if contours:
        cx, cy = contours[0]['center']
        area = contours[0]['area']
        x, y, w, h = cv2.boundingRect(contours[0]['cnt'])

        # Estimate fake depth from bounding box height
        min_height = 60
        max_height = 120
        depth_scale = 1.2  # Boost contrast slightly
        depth_bias = -0.05  # Push average closer to 0
        h_clamped = max(min(h, max_height), min_height)
        raw_depth = 1 - ((h_clamped - min_height) / (max_height - min_height))
        raw_depth = depth_scale * raw_depth + depth_bias
        raw_depth = round(max(0.0, min(1.0, raw_depth)), 3)

        # Smooth only relative_depth using deque
        depth_history.append(raw_depth)
        relative_depth = round(sum(depth_history) / len(depth_history), 3)

        # Stability threshold for depth jitter suppression
        depth_threshold = 0.010
        if 'prev_depth' not in globals():
            prev_depth = relative_depth
        if abs(relative_depth - prev_depth) >= depth_threshold:
            prev_depth = relative_depth
        else:
            relative_depth = prev_depth

        # Smooth other values
        smoothed_x = alpha_pos * cx + (1 - alpha_pos) * smoothed_x if smoothed_x else cx
        smoothed_y = alpha_pos * cy + (1 - alpha_pos) * smoothed_y if smoothed_y else cy
        smoothed_area = alpha_area * area + (1 - alpha_area) * smoothed_area if smoothed_area else area

        # Draw smoothed center
        cv2.circle(frame, (int(smoothed_x), int(smoothed_y)), 8, (255, 255, 0), -1)

        # Relative coordinates from safe zone
        rel_x = normalize(smoothed_x - safe_left, 0, safe_width)
        rel_y = normalize(safe_bottom - smoothed_y, 0, safe_height)

        # Visualize values
        cv2.putText(frame, f"Rel X: {rel_x:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Rel Y: {rel_y:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Depth (est): {relative_depth:.2f}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 150, 255), 2)

    # ------------------------ OSC Send ------------------------
    values = [rel_x, rel_y, relative_depth, area_hand]
    osc_client.send_message("/handColorData", values)

    # ------------------------ FPS Display ------------------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 0), 2)

    # ------------------------ Show Frame ------------------------
    cv2.imshow("MediaPipe + Color Tracking", frame)

    # imgStack = cvzone.stackImages(
    #     [frame,
    #      imgColor, mask, imgContour], 3, 0.5
    # )
    # cv2.imshow("Combined Tracking View", imgStack)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
