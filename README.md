# Gesture-driven-particles-animation-inside-Unreal-Engine-5
This case study explores new ways to interact with digital environments by translating physical gestures and kinetic movements into real-time changes in 3D assets inside Unreal Engine. The system detects sample objects, extracts meaningful data, and sends it to Unreal using the OSC protocol. Let’s dive into how that works.

**Why Bother Doing This?**
Sure, translating gestures into digital interactions isn’t new—but the tech is evolving fast. Now we can tap into real-time rendering, smarter computer vision, and high-fidelity game engines like Unreal to create interactive installations, in-game VFX, or live performance experiences that feel... well, alive. Endless possibilities lie ahead, folks. ✨

## 1. Data Preprocessing
First things first—we need a live camera feed.

Then, we clean and prep the data:

* **Noise filtering** (to reduce randomness)

* **Data labeling** (to keep it structured)

* **Normalization** (critical if you’re sending values to external programs like UE5)

* **Smoothing** (to avoid jittery, chaotic movements)

![github_01-ezgif com-crop](https://github.com/user-attachments/assets/f4923e30-5a19-4ac5-baf3-1e72010edcc0)

All of this is handled in the Python script attached—don’t stress. It’s structured, commented, and ready to roll.
I've tested both YOLO and MediaPipe for detection. MediaPipe is my go-to here because it’s lightweight and fast. YOLO is great for advanced detections, especially for tracking specific objects that MediaPipe's pre-trained models might not recognize.

Here’s what we’re detecting:

* **One hand** — bounding box per frame.

* **One lime** (yes, a lime 🍋—more fun than a banana).

  * We calculate its 2D position on screen.

  * We infer depth from the bounding box size (bigger = closer to camera).

This gives us four values. We label and normalize them before sending them to Unreal Engine.

💡 *Why the black glove?*
> Because MediaPipe sees skin tones. If I hold the lime in a bare hand, it might confuse the lime for part of my hand. The glove keeps things clear.

💡 *Why normalize values to [0, 1]?*
> Raw values can cause scaling issues in 3D. Normalization ensures more predictable behavior when manipulating virtual assets.

## 2. What Happens Inside UE5?

Let’s talk about the Unreal side.
First, **enable OSC** support inside Unreal Engine. OSC is a lightweight protocol designed to let devices and programs "talk" to each other in real time.

![Screenshot 2025-04-15 120744](https://github.com/user-attachments/assets/abd81f34-3e0a-46e5-94cd-304a74831098)

To receive incoming values:

* Create an **OSC Server** in UE5.

* It acts as the entry point to capture, decode, and feed incoming data into your Blueprint logic.

* You can then trigger events or update parameters based on that data.

In my setup, the values extracted from the lime drive the X, Y, and Z axis values of a particle system. The Blueprint logic to do this is also included in the repo. 🧩
Once the system is running, any value coming in from Python can affect a visual property in Unreal—position, color, scale, physics behavior—you name it. The more complex the 3D asset, the more expressive your interaction can be.
Ok, how to visualize those values inside Unreal Engine 5? First, let's enable OSC which is a popular communication protocol in networking (to simplify: it's meant to let machines "talk" and receieve data each other). Toggle it on inside UE5 and we're good to go. 

![2025-04-1512-18-00-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/88c37293-cfb6-4d82-9c25-577db7151d4f)

## Bonus: Sound Integration

See the image below? I added a built-in UE5 function to capture microphone input, extract an amplitude value, and use it to control how many particles spawn at once.

Simple setup, super satisfying results.

![2025-04-0914-30-47-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/08ac0741-436c-47ca-8433-d23388ea6d57)

33 3. Wrapping It Up

This project is a playground. It’s a gesture-tracking, object-following, particle-spawning experiment in real-time digital puppeteering. The code and Blueprints are there for you to remix, extend, and explore!

![github_03_b_gif](https://github.com/user-attachments/assets/6be5486d-caaa-4fe8-a8a0-e75aa474fba4)




