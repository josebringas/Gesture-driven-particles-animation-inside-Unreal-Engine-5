# Gesture-driven-particles-animation-inside-Unreal-Engine-5
Use computer vision libraries for object/motion tracking to drive real-time animations inside a game engine.

## 1. Set up object tracking script

First thing is to set up a script with MediaPipe library to create and detect landmarks on the face. Thankfully, this library does this job for us by creating keypoints in a human face. In this case, we're taking the tip of the nose as a reference point for our motion tracking only for the horizontal axis, that's what interests us.

Then we set up an initial neutral position for the center of the nose (let's call it 'nose_X'). If we run the script, we will be able to see how by rotating the head, we get positive/negative float values. :) ...The whole idea is to map the displacement of my nose dinamically.

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

