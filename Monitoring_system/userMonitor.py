import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2, imutils
from PyQt5.QtCore import *
import time
import datetime
import serial 
import struct
# Receiver Thread
class Receiver(QThread):
    detected = pyqtSignal(int)
    updateSensorValue = pyqtSignal(int) #maybe (int,int,int,int)
    def __init__(self, conn, parent=None):
        super(Receiver, self).__init__(parent)
        self.is_running =False
        self.conn = conn
        print("recv init")
    def run(self):
        print("recv start")
        self.is_running = True
        while (self.is_running == True):
            if self.conn.readable():
                res = self.conn.read_until(b'\n')
                if len(res) > 0:
                    print("loook at herererere")
                    print(res)
                    res = res[:-2]
                    cmd = res[:2].decode()
                    if cmd =="GS":
                        self.flame_value1 = int.from_bytes(res[2:6],"little")
                        self.gas_value1 = int.from_bytes(res[6:10],"little")
                        self.flame_value2 = int.from_bytes(res[10:14],"little")
                        self.gas_value2 = int.from_bytes(res[14:18],"little")
                        self.updateSensorValue.emit(self.flame_value1, self.gas_value2, self.flame_value2, self.gas_value2)
                    elif cmd == "GR":
                        self.detected.emit(int.from_bytes(res[2:6],"little"))
                    else:
                        print("unknown error")
                        print(res)
    def stop(self):
        print("recv stop")
        self.is_running =False
# Class for Camera
class Camera(QThread):
    update = pyqtSignal()

    def __init__(self,sec=0.1, parent = None):
        super().__init__()
        self.main = parent
        self.running = True
    
    def run(self):
        count = 0 
        while self.running == True:
            self.update.emit()
            time.sleep(0.1)
    
    def stop(self):
        self.running = False

from_class = uic.loadUiType("/home/zeki/dev_ws/git_ws/iot-repo-4/Monitoring_system/userMonitor.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowTitle("Hello, Qt!")
        # codes for cam
        self.isCameraOn = False

        self.pixmap = QPixmap()

        self.camera = Camera(self)
        self.camera.daemon = True
        self.camera.running = False
#########################3delete it, it's just for test
        self.btn_camera.clicked.connect(self.clickCamera)######
        self.camera.update.connect(self.updateCamera)

    

        # setting variables
        self.sensor_timer_interval = 500
        self.RFID_timer_interval = 500
        self.flame_criterion =50
        self.gas_criterion = 50

        # default flags
        self.fire_conn_flag = False
        self.safety_conn_flag = False
        self.flag_list=[0,0,0,0]
        self.indoor_flag = False
        self.ventilation_flag = False

        # default variables
        self.prev_IS=0
        self.curr_IS=0
        self.try_count = 0
        self.flame_value1 = 0
        self.flame_value2 = 0
        self.gas_value1 = 0
        self.gas_value2 = 0
        self.sensor_loc = 0
        self.x_degree = 90
        self.y_degree = 90

        # connection of fireDetect_Unit
        while self.fire_conn_flag == False and self.try_count < 5:
            try:
                self.fire_conn = serial.Serial(port='/dev/ttyACM0',baudrate= 9600, timeout=1000)
                self.fire_conn_flag = True
            except:
                self.fire_conn_flag = False
                self.try_count+=1
                print(self.try_count)
        if self.fire_conn_flag == False and self.try_count>= 5:
            print("###############3endMessage################")
            print("###############3endProgram################")
            self.reply = QMessageBox.critical(self,"Error", "Failed to connect fireDetector Unit",QMessageBox.Ok)
            if self.reply:
                sys.exit(0)
        self.fire_recv = Receiver(self.fire_conn)
        self.fire_recv.start()
        self.try_count=0
        # connection of safetyControl_Unit
        while self.safety_conn_flag == False and self.try_count < 5:
            try:
                self.safety_conn = serial.Serial(port='/dev/ttyACM1',baudrate= 9600, timeout=1)
                self.safety_conn_flag = True
            except:
                self.safety_conn_flag = False
                self.try_count+=1
        if self.safety_conn_flag == False and self.try_count>= 5:
            print("###############3check error Message################")
            QMessageBox.critical(self,"Error", "Failed to connect safetyControl Unit",QMessageBox.Ok)
            self.safety_conn = object()
        if self.safety_conn_flag:
            self.safety_recv = Receiver(self.safety_conn)
            self.safety_recv.start()

        # sensor_timer
        self.sensor_timer = QTimer()
        self.sensor_timer.setInterval(self.sensor_timer_interval)
        self.sensor_timer.timeout.connect(self.getSensor)
        self.sensor_timer.start()

        # RFID_timer
        self.RFID_timer = QTimer()
        self.RFID_timer.setInterval(self.RFID_timer_interval)
        self.RFID_timer.timeout.connect(self.getRFID)

        # update sensor value
        self.fire_recv.updateSensorValue.connect(self.updateSensorValue)

        # wait signal from gui
        self.ventilation_button.clicked.connect(self.ventilation)
        self.deactivate_button.clicked.connect(lambda : self.deactivateButton(2))
        self.camera_up_button.clicked.connect(self.cameraUpButton)
        self.camera_down_button.clicked.connect(self.cameraDownButton)
        self.camera_left_button.clicked.connect(self.cameraLeftButton)
        self.camera_right_button.clicked.connect(self.cameraRightButton)
        self.safety_recv.detected.connect(self.deactivateButton)
        self.end_program_button.clicked.connect(self.endProgram)
        # for testign ui
        self.gas1_test.clicked.connect(self.gas1test)
        self.gas2_test.clicked.connect(self.gas2test)
        self.flame1_test.clicked.connect(self.flame1test)
        self.flame2_test.clicked.connect(self.flame2test)
        self.updateValue.clicked.connect(self.updateSensorValue)

    # test funciton
    def gas1test(self):
        self.gas_value1 += 10
    def gas2test(self):
        self.gas_value2 += 10
    def flame1test(self):
        self.flame_value1 += 10
    def flame2test(self):
        self.flame_value2 += 10

    # function ends program
    def endProgram(self):
        self.deactivateButton(2)
        sys.exit()
    # function send to fireDetector Unit
    def send_fireD(self, command):
        # print("send")
        req_data = struct.pack('<2sc',command, b'\n')
        self.fire_conn.write(req_data)
        ##############
        print("send_fireD")
        print(req_data)
        return
    
    # function send to safetyControl Unit
    def send_safeC(self, command, data1 =0,data2=0):
        # print("send")
        if self.safety_conn_flag:
            req_data = struct.pack('<2siic',command, data1, data2, b'\n')
            self.safety_conn.write(req_data)
            #####################3
            print("send_safeC")
            print(req_data)
        return
    # setText sensor Value
    def setValue(self):
        self.gas_value1_label.setText(str(self.gas_value1))
        self.gas_value2_label.setText(str(self.gas_value2))
        self.flame_value1_label.setText(str(self.flame_value1))
        self.flame_value2_label.setText(str(self.flame_value2))

    # getSensor
    def getSensor(self):
        self.send_fireD(b"GS")
        print("getSensor")

        self.setValue()

    # getRFID
    def getRFID(self):
        self.send_safeC(b"GR")
        print("getRFID")

    # updateSensorValue
    def updateSensorValue(self):
        print("updateSensorValue")
        self.gas_value1_label.setText(str(self.gas_value1))
        self.gas_value2_label.setText(str(self.gas_value2))
        self.flame_value1_label.setText(str(self.flame_value1))
        self.flame_value1_label.setText(str(self.flame_value1))

        self.flag_list[0]=(1 if (self.flame_value1 > self.flame_criterion) else self.flag_list[0])
        self.flag_list[1]=(1 if (self.gas_value1 > self.gas_criterion) else self.flag_list[1])
        self.flag_list[2]=(1 if (self.flame_value2 > self.flame_criterion) else self.flag_list[2])
        self.flag_list[3]=(1 if (self.gas_value2 > self.gas_criterion) else self.flag_list[3])
        
        if self.sensor_loc == 0:
            if 1 in self.flag_list:
                if 1 in self.flag_list[0:2]:
                    self.sensor_loc = 1
                elif 1 in self.flag_list[2:]:
                    self.sensor_loc = 2
                else:
                    pass
            else:
                self.sensor_loc = 0
        gas_fire_flag = (self.flag_list[1]+self.flag_list[3] != 0, self.flag_list[0]+self.flag_list[2] != 0)
        print(gas_fire_flag)
        print(self.flag_list.index(1)/2)
        if True in gas_fire_flag:
            if gas_fire_flag == (False, True):
                self.prev_IS = self.curr_IS
                self.curr_IS = 1
                self.flame_led_button.setStyleSheet("background-color: red;") #####################################
            elif gas_fire_flag == (True, False):
                print("Im in gasfireflag TF")
                self.prev_IS = self.curr_IS
                self.curr_IS = 2
                self.gas_led_button.setStyleSheet("background-color: yellow") #####################################
            elif gas_fire_flag == (True, True):
                self.prev_IS = self.curr_IS
                self.curr_IS = 3
                self.flame_led_button.setStyleSheet("background-color: red") #####################################
                self.gas_led_button.setStyleSheet("background-color: yellow") #####################################
            print(self.prev_IS,self.curr_IS)
            if self.prev_IS != self.curr_IS:
                self.send_safeC(b'IS',self.curr_IS,self.sensor_loc) #self.curr_IS is int
                print(self.flag_list)
            if self.indoor_flag == False:
                self.RFID_timer.start()
                self.clickCamera() #displayCamera check indoor_flag and turn on if flag is true, off when false
                                        # or separate to activeCamera() deactiveCamera()
            self.indoor_flag = True
            self.enable_cam_deactivate()
            if 1 in [self.flag_list[0],self.flag_list[2]]:
                self.enable_ventilation_button()
            else:
                self.disable_ventilation_button()

    # disable cam button and deactivate button  
    def disable_cam_deactivate(self):
        self.camera_up_button.setDisabled(True)
        self.camera_down_button.setDisabled(True)
        self.camera_left_button.setDisabled(True)
        self.camera_right_button.setDisabled(True)
        self.deactivate_button.setDisabled(True)
    
    # enable cam button and deactivate button
    def enable_cam_deactivate(self):
        self.camera_up_button.setDisabled(False)
        self.camera_down_button.setDisabled(False)
        self.camera_left_button.setDisabled(False)
        self.camera_right_button.setDisabled(False)
        self.deactivate_button.setDisabled(False)
    # enable / disable ventilation button
    def enable_ventilation_button(self):
        self.ventilation_button.setDisabled(False)
    def disable_ventilation_button(self):
        self.ventilation_button.setDisabled(True)

    # function of ventilation
    def ventilation(self):
        self.ventilation_flag = not self.ventilation_flag
        if self.ventilation_flag:
            self.send_safeC(b"VC",1)
        else:
            self.send_safeC(b"VC",0)
        print("ventilation")
    
    # funciton of deactiveButton
    def deactivateButton(self, data = 2):
        print("deactive")
        if data == 0:
            QMessageBox.critical(self,"Error", "unknown error",QMessageBox.Ok)
        elif data ==1:
            QMessageBox.critical(self,"Error", "has occured, unauthorized",QMessageBox.Ok)
        else:
            self.sensor_loc = 0
            self.prev_IS = 0
            self.curr_IS = 0
            self.send_safeC(b"IS",0,self.sensor_loc)
            self.gas_led_button.setStyleSheet("background-color: white")
            self.flame_led_button.setStyleSheet("background-color: white")

            self.indoor_flag = False
            self.RFID_timer.stop()

            self.clickCamera()
            #############33

            self.disable_cam_deactivate()
            self.disable_ventilation_button()
            self.ventilation_flag = False

            self.flag_list = [0,0,0,0]
            self.cam_label.clear()

            print("deactivateButton")
            print(self.prev_IS,self.curr_IS)

    # function of cameraUpButton
    def cameraUpButton(self):
        self.y_degree += 10
        if self.y_degree >100:
            self.y_degree = 100
        self.send_safeC(b"CC",self.x_degree,self.y_degree)
        print("cameraUpButton")
    
    # function of cameraDownButton
    def cameraDownButton(self):
        self.y_degree -= 10
        if self.y_degree <0:
            self.y_degree = 0
        self.send_safeC(b"CC",self.x_degree,self.y_degree)
        print("cameraDownButton")
    
    # function of cameraLeftButton
    def cameraLeftButton(self):
        self.x_degree += 10
        if self.x_degree >100:
            self.x_degree = 100
        if self.x_degree == 10:
            self.x_degree = 11
        self.send_safeC(b"CC",self.x_degree,self.y_degree)
        print("cameraLeftButton")
    
    # function of cameraRightButton
    def cameraRightButton(self):
        self.x_degree -= 10
        if self.x_degree <0:
            self.x_degree = 0
        if self.x_degree == 10:
            self.x_degree = 11
        self.send_safeC(b"CC",self.x_degree,self.y_degree)
        print("cameraRightButton")

    # set Camera to Gui
    # def displayCamera(self):
    #     print("dispaly")
    #self.x_degree == 10일 때 y,x 값이 이상해짐





    def updateCamera(self):
        # self.label.setText('Camera Running : ' + str(self.count))
        retval, self.image = self.video.read()
        if retval:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            h,w,c = image.shape
            qimage = QImage(image.data, w,h,w*c, QImage.Format_RGB888)

            self.pixmap= self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.cam_label.width(),self.cam_label.height())

            self.cam_label.setPixmap(self.pixmap)

    def clickCamera(self):
        if self.indoor_flag == False:
            # self.btn_camera.setText('Camera off')
            self.isCameraOn = True
            # self.btn_record.show()
            # self.btn_capture.show()

            self.cameraStart()
        else:
            # self.btn_camera.setText('Camera on')
            self.isCameraOn = False
            # self.btn_record.hide()
            # self.btn_capture.hide()

            self.cameraStop()
            # self.recordingStop()

    def cameraStart(self):
        # if self.playvideo.running == True:
        #     self.mp4Stop()
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)
    
    def cameraStop(self):
        self.camera.running = False
        self.count = 0
        self.video.release()
        self.cam_label.clear()

        
        
                


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())