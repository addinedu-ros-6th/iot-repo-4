# IoT Project Team 4 repository: Fire Safe Monitoring System

## Introduction
- contents

## Skillset

|Category|Skills and Tools|
|:---:|:---:|
|IDE/OS| ![js](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)![js](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![js](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)![js](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) <img src= "https://img.shields.io/badge/Arduino_IDE-00979D?style=for-the-badge&logo=arduino&logoColor=white" /> |
|GUI| <img src="https://img.shields.io/badge/PyQt5-21C25E?style=for-the-badge&logo=quicktype"> |
|--| <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV"> |
|Collaboration| ![js](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)![js](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)![js](https://img.shields.io/badge/confluence-%23172BF4.svg?style=for-the-badge&logo=confluence&logoColor=white)![js](https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white)![js](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)|


## Team Members

|Name|Tasks|
|----|-----|
|김재창 (Project Leader)|Requirements analysis and system design|
| |Document design/test information|
|고선민 |Hardware design|
| |Microprocessor module integration/verification|
|서영환 |System design/verification|
| |DB construction/management|
|이경민 |System design/verification|
| |Communication protocol design|
| |GUI implementation|

## User Requirement Analysis
### Functional Goals 
An automated system that monitors the indoor environment in real time and automatically detects, warns and responds to filame and gas leaks
A system that allows managers to judge and resolve situations both directly on site and remotely  

### Technology Goals
A system that controls the I/O of multiple sensor modules and motors with a microprocessor
GUI-based system where the master PC detects/responds to the possibility of indoor fire in real time

### Derived Requirements
fire detection
- Collect sensor data and transmit to host computer
- Issue an alert when a situation occurs

remote control
- Operate omni-directional camera, solving blind spot problem
- The situation is terminated when the administrator determines that there is no problem.

on-site control
- Separate module that allows on-site managers to judge the situation and resolve the situation 

terminate situation
- Save and retrieve information about situations that have occurred

## System Architecture Design

### Status Diagram
![state_transition_diagram](https://github.com/user-attachments/assets/4b0194b7-ce89-4f23-89f2-79a7955c9ff8)

### System Design
![system_arch](https://github.com/user-attachments/assets/f5a53738-4222-4405-adbe-31200a9cf348)

### Major Scenarios 
- Occurrence-of-Situation Scenario
  ![oos](https://github.com/user-attachments/assets/d62810d8-2872-45fe-81cd-16cfd23f0ac1)
- Manual Camera Control Scenario
  ![mcc](https://github.com/user-attachments/assets/2d4225d5-a298-42d8-954a-15847a62b453)
- End-of-Situation Scenario
  ![eos](https://github.com/user-attachments/assets/feb24d92-f50c-4022-bae6-eff1a0478d4f)

### Serial Communication Protocol
![communication_protocol](https://github.com/user-attachments/assets/5e20ab46-04f4-496f-bf61-76a1b0ab3021)
![command_list](https://github.com/user-attachments/assets/5adad7cc-73fb-4944-811b-9f1ae88d8d8e)
![packet_structure](https://github.com/user-attachments/assets/93b590bc-4848-4f11-a389-4407652e6525)

### Hardware / Wiring
- photo

### GUI Design
![GUI](https://github.com/user-attachments/assets/073fa5ec-52f0-416e-82fb-5e6495403e87)
- contents

### DB Schema
![ERD](https://github.com/user-attachments/assets/8f79eb86-4841-45c1-9d9e-b1f276fc6373)

## Demo Video
[![Watch the video](https://github.com/user-attachments/assets/64dde2a7-0494-4401-9b6e-c69f5848bcb0)](https://drive.google.com/file/d/1hy1FeOyQ_F7rgvRvqLCTZ0Ngx3BC0v6t/view?usp=drive_link)
- After gas and flame sensor detection, end the incident by tagging a registered (authorized) card on the RFID module
