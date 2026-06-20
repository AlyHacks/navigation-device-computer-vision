Computer Vision With OpenCV Python!
------
Overview:
This project utilizes different CNN models to do motion detection, and object tracking. The first iteration used OpenCV to do basic motion detection, but found that the system was too spurious and noisy. The second iteration explores YOLO software and motion tracking over multiple frames.

## Installing YOLO

Installing YOLO takes a couple of steps, and here are the ways that I installed it:

### 1. Install pytorch
I used this source to help me with set up: https://github.com/pytorch/pytorch#from-source

WARNING: You need python version 3.11 or older (I ran into the same dependency problem using 3.13)
Before you continue with the pytorch installation instructions, install and activate python version 3.11.

The source tells you to first clone the pytorch repository in order to enter the file saved in it: 

```
git clone https://github.com/pytorch/pytorch
cd pytorch
git submodule sync
git submodule update --init --recursive
```

This is directly pasted from the source above.
Then, you run this command:

```
pip install --group dev
```

Depending on your PC type (i.e. Mac, Linux, Windows), use the following appropriate options to continue installing. 

### 2. Install OpenCV

Run the command in your terminal:

```
pip3 install opencv-python
```

If it runs into a wheel developing error, run the following:

```
pip install opencv-python-headless
```

### 3. Install YOLO
Before you install YOLO, create a virtual environment for your libraries and packages to be downloaded into. This makes sure that your packages are compatible and do not run into any unwated incompatibility issues with other packages in other locations. 

```
python3 -m venv yolo-env
source yolo-env/bin/activate
```

In order to install YOLO from ultralytics, you need numpy versions less than numpy 2.
Run this command:

```
pip3 install "numpy<2" 
```

Then, run this command:

```
pip3 install ultralytics
```
You should be able to run the basics.py code now on your desktop!! (the file is in software --> YOLOCode --> basics.py)




Running YOLO on Raspberry Pi
-------------

### 1. Setting up your Raspberry Pi camera
In order to run this on your Raspi camera, you need to first connect your Raspberry Pi with your ribbon cable Raspi camera. This instruction uses the Raspberry Pi model 5, which is the recommended version if running YOLO on the Raspberry Pi.

(image goes here)

To test if your camera is working properly run the following command in your terminal:
```
rpicam-hello
```
A window with your camera feed should pop up.

### 2. Installing YOLO
The installation of YOLO is similar except, we have some preliminary steps. To update all available packages, run the following commands:

```
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y 
```

Then, create your virtual environment. If you already created one, activate it.
```
python3 -m venv yolovenv 
source yolovenv/bin/activate 
```

Then, uninstall Numpy to versions less than 2 (ultralytics and numpy packages have package dependency issues, so it's best to stick to Numpy<2)
```
pip install “numpy<2”
```

Lastly, install ultralytics for YOLO:
```
pip install ultralytics 
```

### 3. Running the code
Now, you're ready to run the YOLO code on your Raspi camera!
Run the code picam.py! (the file is in software --> YOLOCode --> picam.py)
