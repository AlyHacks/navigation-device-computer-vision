Computer Vision With OpenCV Python!
------
Overview:
This project utilizes different CNN models to do motion detection, and object tracking. The first iteration used OpenCV to do basic motion detection, but found that the system was too spurious and noisy. The second iteration explores YOLO software and motion tracking over multiple frames.

### Installing YOLO

Installing YOLO takes a couple of steps, and here are the ways that I installed it:

## 1. Install pytorch
I used this source to help me with set up: https://github.com/pytorch/pytorch#from-source

WARNING: You need python version 3.11 or older (I ran into the same dependency problem using 3.13)
Before you continue with the pytorch installation instructions, install and activate python version 3.11.

The source tells you to first clone the pytorch repository in order to enter the file saved in it: 

'''
git clone https://github.com/pytorch/pytorch
cd pytorch
git submodule sync
git submodule update --init --recursive
'''

This is directly pasted from the source above.
Then, you run this command:

'''
pip install --group dev
'''

Depending on your PC type (i.e. Mac, Linux, Windows), use the following appropriate options to continue installing. 

2. Install OpenCV

Run the command in your terminal:

'''
pip3 install opencv-python
'''

If it runs into a wheel developing error, run the following:

'''
pip install opencv-python-headless
'''

3. Install YOLO

In order to install YOLO from ultralytics, you need numpy versions less than numpy 2.
Run this command:

'''
pip3 install "numpy<2" 
'''

Then, run this command:

'''
pip3 install ultralytics
'''


