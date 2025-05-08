# Gesture-driven-particles-animation-inside-Unreal-Engine-5
This case study focuses on expanding ways to interact with digital environments by mapping physical gestures and kinetic movement to real-time changes in 3D assets inside Unreal Engine. My system attemps to detect sample objects, extract meaningful data and send them to the engine via OSC protocol. We'll explore that option here.

Why bother doing this? translating physical gestures into real-time digital interactions is nothing new, but as technology evolves, so does possibilities to explore game engine rendering animation quality powered by computer vision capabilities to drive in-game VFX, interactive installations or other live performative experiences. Endless possiblities lies ahead guys...

## 1. Data Preprocessing

First, we need to get a live camera feed and do some filtering & cleaning like removing noise, labelling data, normalizing data (truly important if sending to external programs like UE5) and smoothing data (to avoid jitter). I'm providing these blocks in the py script attached so don't worry; structured and labelled code with comments has been added.

![github_01-ezgif com-crop](https://github.com/user-attachments/assets/f4923e30-5a19-4ac5-baf3-1e72010edcc0)

I've tried both YOLO and Mediapipe library for the detections but I'm sticking to Mediapipe for now. Both offer good tradeoffs and persoanlly, I'm using YOLO for more advanced detections (like to track specific objects that otherwise pre-trained models like Mediapipe won't be able to do it).

We're detecting 1 hand and calculating its bounding box per frame. Also, we're picking up 1 sample object, a lime (why not!), calculating its 2D position on the screen and inferring its depth by the size of the bounding box. Larger box means it's closer to the webcam, has a higher numerical value and viceversa. 

Have anybody wondered why I have a black glove on my other hand holding the lime? Because Mediapipe and machine are intelligent, but not enough to recognize that as a hand. Lastly, What's the point of normalizing values [0,1] ? we don't want to send raw values to the external package that can potentially offset or misalign the position of our assets especially in a 3D world environment. It's preferable to normalize values first and inside the external software to apply as many changes to the coming values as wished.

![Screenshot 2025-04-15 120651](https://github.com/user-attachments/assets/43d18b4a-9fed-49e6-8247-d047adfd0fb1)

## 2. What do we do with these values inside UE5?

Ok, first of all, we'll send over OSC communication these values and so, I added a snippet in the python script to make that happen. and now, how to visualize those values inside Unreal Engine 5? I've got you there! First, enable OSC inside UE5.

![Screenshot 2025-04-15 120809](https://github.com/user-attachments/assets/b6f9b086-bbf3-412b-ac17-45ad36806878)

Ok, if we're sending these values to Unreal, what do we need to do? Receieve it, for sure. We have to make sure Unreal Engine pays attention, 'listen', every frame for any upcoming value that will store in a Blueprint actor called 'OSC_Receiver'. (Highly encourage to you to learn networking, protocol communication between systems, devices. It's an amazing field :-) )

Once, we are able to visualize these values, a bit more work is needed. Before anything else, we need to parse these values a blueprint actor 'BP_Receiver' that contains the actual object whose behaviour will change dinamically with our gestures. Because these raw values were normalize in python [-1,1] we need to clamp, meaning, to remap them inside UE5 so when we translate objects with our head movement in real-time, we actually see those changes.

On the other hand (because we want to get creative) I added a function to read audio input inside UE5 and pass those values to change the behaviour of our 'BP_Receiver' again. in this case, translating its z-axis.

![2025-04-1512-18-00-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/88c37293-cfb6-4d82-9c25-577db7151d4f)

So, based on these actions can you guess what I'm trying to do? 

For me, the idea is to dinamically change the behavour of a 3D asset in real-time. By behaviour we mean position, rotation, scale, or any other measureable variable that a 3D object have. 

And why using gestures? (Other than it looks cool!) ...I truly think this workflow offers flexibility to create animations and interactions between objects that traditional means (splines or keyframing) cannot provide. It allows a more 'organic' interaction between machine and human. 

This work is still in progress. New features includes Niagara Particles driven by gestures and potentially, adding collision on top of that.

![2025-04-0914-30-47-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/08ac0741-436c-47ca-8433-d23388ea6d57)

