# IoT Project Team 4 repository: Fire Safe Monitoring System

## 개요
### 주제 소개
- 시스템이 화재 발생 가능성을 실시간으로 감지 및 대응하고, 사용자는 GUI 또는 현장의 경보 모듈을 통해 상황을 파악하여 대처할 수 있도록 지원하는 서비스입니다.
### 기술 스택
|분류|기술|
|-----|-----|
|개발 언어|![js](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![js](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)|
|영상처리| <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV"> |
|UI| <img src="https://img.shields.io/badge/PyQt5-21C25E?style=for-the-badge&logo=quicktype"> |
|DBMS|![js](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)|
|개발 환경|![js](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white) <img src= "https://img.shields.io/badge/Arduino_IDE-00979D?style=for-the-badge&logo=arduino&logoColor=white" />|
|협업| ![js](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white) ![js](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white) ![js](https://img.shields.io/badge/confluence-%23172BF4.svg?style=for-the-badge&logo=confluence&logoColor=white) ![js](https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white) ![js](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)|


## 팀원 소개

|이름|담당|
|----|-----|
|김재창 <br> (Project Leader)|요구사항 분석 및 시스템 설계 <br> 설계/테스트 정보 문서화| 
|고선민|하드웨어 설계 <br> 마이크로프로세서 모듈 통합/검증|
|서영환|시스템 설계/검증 <br> DB 구축/관리| 
|이경민|시스템 통합/검증 <br> 통신 프로토콜 설계 <br> GUI 구현|

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
  
  ![new_new_system](https://github.com/user-attachments/assets/ad7cc2df-2375-426c-b0eb-918d9c39370e)

### 주요 시나리오
- 상황 발생 시나리오 시퀀스 다이어그램
  
  ![oos](https://github.com/user-attachments/assets/d62810d8-2872-45fe-81cd-16cfd23f0ac1)
- 카메라 수동 조작 시나리오 시퀀스 다이어그램
  
  ![mcc](https://github.com/user-attachments/assets/2d4225d5-a298-42d8-954a-15847a62b453)
- 상황 종료 시나리오 시퀀스 다이어그램
  
  ![eos](https://github.com/user-attachments/assets/feb24d92-f50c-4022-bae6-eff1a0478d4f)

### 통신 프로토콜 정의
#### Communication Protocol List
|Transmitter|Receiver|Communication Protocol|
|-----|-----|-----|
|Host PC (USB Port 1)|fireDetector Unit|Serial Peripheral Interface Protocol|
|fireDetector Unit|Host PC (USB Port 1)|Serial Peripheral Interface Protocol|
|Host PC (USB Port 2)|safetyControl Unit|Serial Peripheral Interface Protocol|
|safetyControl Unit|Host PC (USB Port 2)|Serial Peripheral Interface Protocol|
|camera|Host PC (USB port 3)|Picture Transfer Protocol|

#### Command List
<table>
  <thead>
    <tr>
      <th>Transmitter</th>
      <th>Command</th>
      <th>Full Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan=5>Host PC</td>
      <td rowspan=1>IS</td>
      <td>Indoor Status</td>
      <td>retrieve indoor room status through two sensors, inform current status using the status code: 0, 1, 2 or 3 {0:Normal, 1:Flame, 2:Gas, 3: Both sensors} and inform where camera should point at using the direction code: 0, 1 or 2 {0: default, 1:SensorModule1, 2: SensorModule2}.</td>
    </tr>
    <tr>
      <td rowspan=1>CC</td>
      <td>Camera Control</td>
      <td>control X and Y-axis of the camera, pass two integers</td>
    </tr>
    <tr>
      <td rowspan=1>VC</td>
      <td>Ventilator Control</td>
      <td>send OFF/ON status code (0 or 1) [0: OFF, 1: ON]</td>
    </tr>
    <tr>
      <td rowspan=1>GR</td>
      <td>Get RFID</td>
      <td>get the status of RFID, if tagged send turn off  signal</td>
    </tr>
    <tr>
      <td rowspan=1>GS</td>
      <td>Get Sensor values</td>
      <td>get Sensor data from fireDetector Unit</td>
    </tr>
    <tr>
      <td rowspan=1>fireDetector</td>
      <td> GS</td>
      <td>Get Sensor</td>
      <td> send integer sensor values from 2 different modules: SensorModule1(flameInfo1, gasInfo1) and SensorModule2(flameInfo2, gasInfo2) to the host PC</td>
    </tr>
    <tr>
      <td rowspan=1>safetyControl</td>
      <td> GR</td>
      <td>Get RFID</td>
      <td> send signal: 0 if unknown error has occured, 1 if unauthorized RFID transponder is tagged, 2 if authorized RFID transponder is tagged</td>
    </tr>
  </tbody>
</table>


#### Packet Structure
<table>
    <thead>
        <tr>
            <th colspan=6> Command for fireDetector Unit to Host PC</th>
        </tr>
        <tr>
            <th> Command ID </th>
            <th> Data1 </th>
            <th> Data2 </th>
            <th> Data3 </th>
            <th> Data4 </th>
            <th> End byte </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td> 2 bytes </td>
            <td> 4 bytes </td>
            <td> 4 bytes </td>
            <td> 4 bytes </td>
            <td> 4 bytes </td>
            <td> 1 byte </td>
        </tr>
        <tr>
        </tr>
        <tr>
            <td> GS </td>
            <td> (int) Sensor1 Value </td>
            <td> (int) Sensor2 Value </td>
            <td> (int) Sensor3 Value </td>
            <td> (int) Sensor4 Value </td>
            <td> \n </td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan=6> Command for Host PC to safetyControl Unit </th>
        </tr>
        <tr>
            <th> Command ID </th>
            <th> Data1 </th>
            <th> Data2 </th>
            <th> End byte </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td> 2 bytes </td>
            <td> 4 bytes </td>
            <td> 4 bytes </td>
            <td> 1 byte </td>
        </tr>
        <tr>
        </tr>
        <tr>
            <td> IS </td>
            <td> (int) State [0,1, 2, 3] </td>
            <td> (int) (int) Camera Direction Info [0, 1, 2] </td>
            <td> \n </td>
        </tr>
        <tr>
            <td> CC </td>
            <td> (int) Degree </td>
            <td> (int) Degree </td>
            <td> \n </td>
        </tr>
        <tr>
            <td> VC </td>
            <td> (int) State[0,1] </td>
            <td> - </td>
            <td> \n </td>
        </tr>
        <tr>
            <td> GR </td>
            <td> - </td>
            <td> - </td>
            <td> \n </td>
        </tr>
    </tbody>
</table>

### GUI 설계
![GUI](https://github.com/user-attachments/assets/073fa5ec-52f0-416e-82fb-5e6495403e87)

### Database 설계
- ERD
  
![ERD](https://github.com/user-attachments/assets/62bd0db8-d9f0-49f1-8322-5d19a0c60a02)

## 시연 영상
[![Watch the video](https://github.com/user-attachments/assets/64dde2a7-0494-4401-9b6e-c69f5848bcb0)](https://drive.google.com/file/d/1hy1FeOyQ_F7rgvRvqLCTZ0Ngx3BC0v6t/view?usp=drive_link)
- 센서가 순차적으로 가스 누출 감지, 불꽃 감지 이후 자동으로 상황 발령, 관리자가 허가된 카드를 RFID 모듈을 태그하며 상황 종료
