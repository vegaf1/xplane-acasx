# xplane-acasx

Objectives

This repository contains packages developed for XPlane11 ACAS SxU simulation, developed during  summer'20 as part of the RISS program at CMU Air Lab. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

The software you need to install the software

```
* Obtain a copy of the ACAS sxU algorithm to test the logic on the xplane flight simulator
* Ubuntu 18.04, ROS Melodic
* XPlane11 Flight Simulator
* XPlane- Connect Plugin (follow instructions on the link below to have the plugin show on the XPlane11 window)
    https://github.com/nasa/XPlaneConnect
* Python3
    

### Installing

XPlane Connect can be installed with the link shown above. Once installed, make sure to put the contents 
in the following directory: [X-Plane Directory]/Resources/plugins/. This will enable you to use the 
plugin in the XPlane environment

pip3 install pygame

Move the Taranis folder to the /XPlane/Aircrafts directory. The Taranis is the main aircraft used since it fits the dimensionsions that 
ACAS sXu requires

## Running

Follow the instructions below:

```
Run the XPlane Application, select the Taranis as the main aicraft used.
* python3 [sxi_ros package] usb_cam-test.launch
* roslaunch darknet_ros yolo_v3_custom.launch
* rosrun cam_angle image_sub.py
* rosrun box_sub box_subscriber

To launch the P3DX Navigation ...

* roslaunch pioneer_nav pioneer_nav.launch 
* rosrun rosaria Rosaria 
* roslaunch p3dx_description rviz.launch      

Make sure laser is USB 0 and the USB to serial cable from the pioneer is USB1. Always configure it using:

* chmod a+rw /dev/ttyUSB0
* chmod a+rw /dev/ttyUSB1

In order to make a map
* roslaunch teleop_twist_joy teleop.launch (Press the LB  and the arrow keys in order to move the robot around)
* roslaunch gmapping slam_gmapping_pr2.launch


```

## Authors

* **Fausto Vega** - *REU student* - [Link](https://github.com/vegaf1)
* **Mohammadreza Mousaei** - *Grad Mentor* - [Link](https://github.com/)

## Acknowledgments
* Thank you to the Robotic Institute of Summer Scholars (RISS) program at Carnegie Mellon University for this great opportunity. 


