# IoT Project Team 4 repository: Fire Safe Monitoring System

## 개요
### 주제 소개
- 주제
### 기술 스택
|Category|Skills and Tools|
|:---:|:---:|
|IDE/OS| ![js](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)![js](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![js](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)![js](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) <img src= "https://img.shields.io/badge/Arduino_IDE-00979D?style=for-the-badge&logo=arduino&logoColor=white" /> |
|GUI| <img src="https://img.shields.io/badge/PyQt5-21C25E?style=for-the-badge&logo=quicktype"> |
|--| <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV"> |
|Collaboration| ![js](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)![js](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)![js](https://img.shields.io/badge/confluence-%23172BF4.svg?style=for-the-badge&logo=confluence&logoColor=white)![js](https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white)![js](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)|


## 팀원 소개

|김재창 (Project Leader)|고선민 |서영환 |이경민 |
|----|-----|----|-----|
|요구사항 분석 및 시스템 설계, 설계/테스트 정보 문서화| 하드웨어 설계, 마이크로프로세서 모듈 통합/검증| 시스템 설계/검증, DB 구축/관리 | 시스템 통합/검증, 통신 프로토콜 설계, GUI 구현|




## 사용자 요구사항 분석
### 기능적 목표
- 실내 환경을 실시간으로 모니터링, 화재 및 가스 누출 여부를 자동 감지, 경고/대응하는 자동화 시스템
- 관리자가 현장에서 직접, 또는 원격으로 상황에 대한 판단 및 해제가 가능한 시스템
### 기술적 목표
- 다중 센서 모듈, 모터들의 i/o를 마이크로프로세서로 제어하는 시스템
- 마스터 PC가 실내의 화재 가능성을 실시간으로 감지/대응하는 GUI 기반 시스템 
### 사용자 요구사항 도출
![user_requirement](https://github.com/user-attachments/assets/f31357e0-bf6e-4406-91aa-e2d0c3d0c008)

## 시스템 아키텍처
### 상태 정의
- 상태 전이도
![state_transition_diagram](https://github.com/user-attachments/assets/4b0194b7-ce89-4f23-89f2-79a7955c9ff8)

### 시스템 설계
- 시스템 구성도
![system_arch](https://github.com/user-attachments/assets/0351d1a8-2d8e-4f0c-b182-472562c5726a)

### 주요 시나리오
- 상황 발생 시나리오 시퀀스 다이어그램
  ![oos](https://github.com/user-attachments/assets/d62810d8-2872-45fe-81cd-16cfd23f0ac1)
- 카메라 수동 조작 시나리오 시퀀스 다이어그램
  ![mcc](https://github.com/user-attachments/assets/2d4225d5-a298-42d8-954a-15847a62b453)
- 상황 종료 시나리오 시퀀스 다이어그램
  ![eos](https://github.com/user-attachments/assets/feb24d92-f50c-4022-bae6-eff1a0478d4f)

### 통신 프로토콜 정의
![communication_protocol](https://github.com/user-attachments/assets/5e20ab46-04f4-496f-bf61-76a1b0ab3021)
![command_list](https://github.com/user-attachments/assets/5adad7cc-73fb-4944-811b-9f1ae88d8d8e)
![packet_structure](https://github.com/user-attachments/assets/93b590bc-4848-4f11-a389-4407652e6525)

### Hardware / Wiring
- photo

### GUI 설계
![GUI](https://github.com/user-attachments/assets/073fa5ec-52f0-416e-82fb-5e6495403e87)
- contents

### Database 설계
- ERD
![ERD](https://github.com/user-attachments/assets/62bd0db8-d9f0-49f1-8322-5d19a0c60a02)

## Demo Video
[![Watch the video](https://github.com/user-attachments/assets/64dde2a7-0494-4401-9b6e-c69f5848bcb0)](https://drive.google.com/file/d/1hy1FeOyQ_F7rgvRvqLCTZ0Ngx3BC0v6t/view?usp=drive_link)
- After gas and flame sensor detection, end the incident by tagging a registered (authorized) card on the RFID module
