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
Run the XPlane Application, select the Taranis as the main aicraft used., and once you are in the scene,press b to unlock the brakes of the aircraft. 
Next, run the following script in this order: 

Open a terminal to run each command (no pid). 
* roscore
* rosrun xplane_data datapublish.py (right arrow into pygame window to spawn aircraft )
* run the following in one terminal: 
    * export ACASX_JULIA_HOME=$(pwd)/../Julia.1.0.3.linux/bin
    * export PATH=$(pwd)/../Julia.1.0.3.linux/bin:$PATH
    * python3 sxu_ros.py
    

Open a terminal to run each command (pid). 
* roscore
* rosrun xplane_data p_control_xplane.py (right arrow into pygame window to spawn aircraft)
* run the following in one terminal: 
    * export ACASX_JULIA_HOME=$(pwd)/../Julia.1.0.3.linux/bin
    * export PATH=$(pwd)/../Julia.1.0.3.linux/bin:$PATH
    * python3 sxu_ros.py

## Authors

* **Fausto Vega** - *REU student* - [Link](https://github.com/vegaf1)
* **Mohammadreza Mousaei** - *Grad Mentor* - [Link](https://github.com/mmousaei)

## Acknowledgments
* Thank you to the Robotic Institute of Summer Scholars (RISS) program at Carnegie Mellon University for this great opportunity. 


