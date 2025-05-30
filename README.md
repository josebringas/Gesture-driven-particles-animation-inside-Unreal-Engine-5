# Gesture-driven-particles-animation-inside-Unreal-Engine-5
Kinetic Narratives is a real-time hand gesture and color object tracking tool that transmits normalized motion and depth data via OSC to interactive environments like Unreal Engine, TouchDesigner, or Unity. This version uses MediaPipe for gesture-based control and HSV color segmentation for object tracking — enabling responsive, kinetic interactions for digital artworks, installations, and experimental interfaces.

![screenshot-1-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/d7c4412b-b8ec-428d-bf31-080bde5636fa)

## Features
* MediaPipe Hand Tracking
  * Tracks a single hand in real time
  * Calculates and normalizes bounding box area
  * Provides a motion parameter usable for gesture-based scaling or triggering
    
* Color-Based Object Detection
  * Tracks a color-defined object (e.g., a glove, prop, or ball)
  * Uses HSV masking and contour detection via `cvzone`
  * Extracts smoothed position, size, and fake depth from bounding box height
    
* Real-Time OSC Data Streaming
  * Sends 4 normalized parameters over OSC:
    * `rel_x`: horizontal position (from safe zone)
    * `rel_y`: vertical position (from safe zone)
    * `relative_depth`: estimated depth based on object height
    * `area_hand`: smoothed area of MediaPipe hand bounding box
      
* Safe Interaction Zone
  * Frames the capture region to ignore boundary noise
  * All positions are calculated relative to this zone
    
* Smoothing and Jitter Suppression
  * Position and depth are smoothed using exponential decay
  * Depth values use a rolling average with jitter thresholding

![github_01-ezgif com-crop](https://github.com/user-attachments/assets/f4923e30-5a19-4ac5-baf3-1e72010edcc0)

## OSC Output Format
Sends to: `127.0.0.1:8000`

```
/handColorData [rel_x, rel_y, relative_depth, area_hand]
```
Each value is normalized between 0.0 and 1.0, ideal for driving:

* Shader effects
* Virtual object transformations
* Audio-reactive visuals
* Gesture-based triggers

## Example Applications
* Control 3D object scale or position in Unreal Engine 5 Blueprints
* Drive particle systems or generative forms in TouchDesigner
* Use fake depth to simulate z-axis movement in Unity
* Enable non-contact interfaces in interactive installations or performances

![blower_thingy_v001-ezgif com-crop](https://github.com/user-attachments/assets/f3c7f649-5119-468a-9401-cb9d5c55af38)


## HSV Tuning
Color tracking uses pre-calibrated HSV values:
```
hsvVals = {'hmin': 28, 'smin': 73, 'vmin': 80, 'hmax': 49, 'smax': 209, 'vmax': 229}
```
Use the `ColorFinder` module to fine-tune for your own prop or glove:
```
myColorFinder = ColorFinder(True)  # Enable live tuning
```

## Dependencies
* OpenCV
* cvzone
* Mediapipe
* `python-osc`

Install them with:
```
pip install opencv-python cvzone mediapipe python-osc
```

## Usage
```
python kinetic_narratives_mediapipe.py
```
Press `q` to quit.

## Input Device
Make sure your webcam index is correct:
```
cap = cv2.VideoCapture(1)  # Change to 0 if using built-in webcam
```

## YOLO-Based Hand Detection (Alternative Version)
An alternate version of this system uses a custom-trained YOLOv8 model for hand detection.
* Training Dataset: The model was trained using a curated public hand detection dataset collected and annotated through [Roboflow](https://universe.roboflow.com/work-tbypc/handdetection-qycc7).
* Synthetic Data Augmentation: We used the powerful [Albumentations](https://albumentations.ai) library to augment the training set, introducing controlled variation in lighting, blur, noise, and occlusion, making the detector more robust in real-world scenarios.
* Model Variant: YOLOv8n (nano) was selected for real-time inference on CPU/GPU.
* Training Pipeline: View the complete training pipeline in this [Google Colab notebook](https://colab.research.google.com/drive/1SYHiaUX-SddGqV_st1q_J8F7oNHcjfLN#scrollTo=hUMicYRBHWqU), which includes:
  * Dataset upload and preprocessing
  * Data augmentation via Albumentations
  * Model training and validation
  * Exporting the `.pt` model for inference

> This YOLO version is ideal for cases where MediaPipe underperforms, such as in low-light or partial-occlusion settings. You can easily swap between the YOLO and MediaPipe pipelines depending on your performance needs.

![Screenshot 2025-05-30 173325](https://github.com/user-attachments/assets/799eaae0-c8aa-4da4-803d-b83f79ea0a92)

