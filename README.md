# Gesture-driven-particles-animation-inside-Unreal-Engine-5
This case study focuses on expanding ways to interact with digital environments by mapping physical gestures and kinetic movement to real-time changes in 3D assets inside Unreal Engine. My system attemps to detect sample objects, extract meaningful data and send them to the engine via OSC protocol. We'll explore that option here.

Why bother doing this? translating physical gestures into real-time digital interactions is nothing new, but as technology evolves, so does possibilities to explore game engine rendering animation quality powered by computer vision capabilities to drive in-game VFX, interactive installations or other live performative experiences. Endless possiblities lies ahead guys...

## 1. Data Preprocessing

First, we need to get a live camera feed and do some filtering & cleaning like removing noise, labelling data, normalizing data (truly important if sending to external programs like UE5) and smoothing data (to avoid jitter). I'm providing these blocks in the py script attached so don't worry; structured and labelled code with comments has been added.

![github_01-ezgif com-crop](https://github.com/user-attachments/assets/f4923e30-5a19-4ac5-baf3-1e72010edcc0)

I've tried both YOLO and Mediapipe library for the detections but I'm sticking to Mediapipe for now. Both offer good tradeoffs and persoanlly, I'm using YOLO for more advanced detections (like to track specific objects that otherwise pre-trained models like Mediapipe won't be able to do it).

We're detecting 1 hand and calculating its bounding box per frame. Also, we're picking up 1 sample object, a lime (why not!), calculating its 2D position on the screen and inferring its depth by the size of the bounding box. Larger box means it's closer to the webcam, has a higher numerical value and viceversa. In total, we're extracting 4 values, labelling and preparing them to be sent over Unreal Engine.  

Have anybody wondered why I have a black glove on my other hand holding the lime? Because Mediapipe and machines are intelligent, but not enough to recognize that as a hand. Lastly, What's the point of normalizing values [0,1] ? we don't want to send raw values to the external package that can potentially offset or misalign the position of our assets especially in a 3D world environment. It's preferable to normalize values first and inside the external software to apply as many changes to the coming values as wished.

## 2. What do we do with these values inside UE5?

Ok, how to visualize those values inside Unreal Engine 5? First, let's enable OSC which is a popular communication protocol in networking (to simplify: it's meant to let machines "talk" and receieve data each other). Toggle it on inside UE5 and we're good to go. 

![Screenshot 2025-04-15 120809](https://github.com/user-attachments/assets/b6f9b086-bbf3-412b-ac17-45ad36806878)

To receieve this values we'll need to create a "server", the entrypoint inside UE5 to receieve, decode and use the upcoming values inside the blueprint logic. With this setup we can trigger blueprint events at any time Unreal detects new data feeding the logic. From this point, is up to the developer to properly set up the parameters and actors to be directly affected by any input data. In my case, the values extracted for the lime sample are mapped to drive x,y,z axis values for a particle system in the 3D world. 

A blueprint logic setup is provided here as well. The main idea is to effectively receieve the OSC packets and broadcast one or multiple events that will change behaviors of 3D assets in real-time. By behaviors, I mean change any type of property a 3D asset has. By default, the more complex the asset is, the more possiblities to explore changing different values for visualization.

![2025-04-1512-18-00-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/88c37293-cfb6-4d82-9c25-577db7151d4f)

So, based on these actions can you guess what I'm trying to do? 

For me, the idea is to dinamically change the behavour of a 3D asset in real-time. By behaviour we mean position, rotation, scale, or any other measureable variable that a 3D object have. 

And why using gestures? (Other than it looks cool!) ...I truly think this workflow offers flexibility to create animations and interactions between objects that traditional means (splines or keyframing) cannot provide. It allows a more 'organic' interaction between machine and human. 

This work is still in progress. New features includes Niagara Particles driven by gestures and potentially, adding collision on top of that.

![2025-04-0914-30-47-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/08ac0741-436c-47ca-8433-d23388ea6d57)

