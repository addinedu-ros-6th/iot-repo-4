import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2, imutils
from PyQt5.QtCore import *
import time
import datetime
from datetime import datetime 
import serial 
import struct
import mysql.connector

flame_value1 = 0
flame_value2 = 0
gas_value1 = 0
gas_value2 = 0

# Receiver Thread
class Receiver(QThread):
    detected = pyqtSignal(int)
    # updateSensorValue = pyqtSignal(int) #maybe (int,int,int,int)
    updateSensorValue = pyqtSignal()
    def __init__(self, conn, parent=None):
        super(Receiver, self).__init__(parent)
        self.is_running =False
        self.conn = conn
        print("recv init")
    def run(self):
        global flame_value1, flame_value2, gas_value1, gas_value2
        print("recv start")
        self.is_running = True
        flame_value1 = 50
        while (self.is_running == True):
            if self.conn.readable():
                res = self.conn.read_until(b'\n')
                # res = self.conn.read(4)
                if len(res) > 0:
                    print("loook at herererere")
                    print(res)
                    print(int.from_bytes(res,"little"))
                    res = res[:-1] # origin res = res[:2]
                    cmd = res[:2].decode()
                    if cmd =="GS":
                        print("im GGGGGGGGGGGGSSSSSSSSSSS")
                        flame_value1 = int.from_bytes(res[2:6],"little")
                        gas_value1 = int.from_bytes(res[6:10],"little")
                        flame_value2 = int.from_bytes(res[10:14],"little")
                        gas_value2 = int.from_bytes(res[14:18],"little")

                        # flame_value1= self.conn.readline().strip() # Testtttttttttingggggg
                        # flame_value1 = int.from_bytes(flame_value1,"little")
                        # gas_value1 = struct.unpack('<I', res[6:10])[0]
                        # flame_value2 = struct.unpack('<I', res[10:14])[0]
                        # gas_value2 = struct.unpack('<I', res[14:18])[0]
                        # self.updateSensorValue.emit(flame_value1, gas_value1, flame_value2, gas_value2)
                        # res = res[2:]
                        # print(res)
                        # flame_value1 = struct.unpack('>I', res[:4])[0]
                        # gas_value1 = struct.unpack('IIII', res)[1]
                        # flame_value2 = struct.unpack('iiii', res)[2]
                        # gas_value2 = struct.unpack('<IIII', res)[3]

                        # flame_value1 = res[:4].decode('utf-8')
                        # # flame_value1 = int(flame_value1)
                        # gas_value1 = res[4:8].decode('utf-8')
                        # # gas_value1 = int(gas_value1)
                        # flame_value2 = res[8:12].decode('utf-8')
                        # # flame_value2 = int(flame_value2)
                        # gas_value2 = res[12:].decode('utf-8')
                        # # gas_value2 = int(gas_value2)

                        print(flame_value1,gas_value1,flame_value2,gas_value2)
                        self.updateSensorValue.emit()
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

                            #change directory
from_class = uic.loadUiType("/home/zeki/dev_ws/git_ws/iot-repo-4/Monitoring_system/userMonitor.ui")[0]


class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initSQL()

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

        #large db screen hide
        self.groupBox.hide()
        self.groupBox_2.hide()

        # setting variables
        self.sensor_timer_interval = 500
        self.RFID_timer_interval = 500
        self.flame_criterion = 350
        self.gas_criterion = 350
        self.camera_up_limit = 50
        self.camera_down_limit = 20
        self.camera_left_limit = 180
        self.camera_right_limit = 0
        self.DeactivateButton_counter_reset_timer_interval = 5000


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
        self.sensor_loc = 0
        self.x_degree = 105
        self.y_degree = 30
        self.DeactivateButton_counter = 0

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
                sys.exit()
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


        #test timer
        #self.test_timer = QTimer()
        #self.test_timer.setInterval(self.sensor_timer_interval)
        #self.test_timer.timeout.connect(self.sql_total_sensor_insert)
        #self.test_timer.start()

        # reset RFID counter
        self.DeactivateButton_counter_reset_timer = QTimer()
        self.DeactivateButton_counter_reset_timer.setInterval(self.DeactivateButton_counter_reset_timer_interval)
        self.DeactivateButton_counter_reset_timer.timeout.connect(self.resetDeactivateButtonCounter)
        self.DeactivateButton_counter_reset_timer.start()
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
        self.deactivate_button.clicked.connect(lambda : self.deactivateButton(3))
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
        self.enlarge_button.clicked.connect(self.show_database_enlarge)
        self.exit_button.clicked.connect(self.exit_database_enlarge)
        self.notull_button.clicked.connect(self.show_notnull_data)

    #database putout
    def print_database(self):
        self.cursor.execute("SELECT * FROM (SELECT * FROM fireIncident ORDER BY id DESC LIMIT 5) AS subquery ORDER BY id ASC;") 

        self.log_tableWidget.setRowCount(0);  
        for value in self.cursor.fetchall():
            
            row  = self.log_tableWidget.rowCount() 
            self.log_tableWidget.insertRow(row)
            self.log_tableWidget.setItem(row, 0, QTableWidgetItem(str(value[0])))
            self.log_tableWidget.setItem(row, 1, QTableWidgetItem(str(value[1])))
            self.log_tableWidget.setItem(row, 2, QTableWidgetItem(str(value[2])))
            self.log_tableWidget.setItem(row, 3, QTableWidgetItem(str(value[3])))
            self.log_tableWidget.setItem(row, 4, QTableWidgetItem(str(value[4])))
            self.log_tableWidget.setItem(row, 5, QTableWidgetItem(str(value[5])))
            self.log_tableWidget.setItem(row, 6, QTableWidgetItem(str(value[6])))
            self.log_tableWidget.setItem(row, 7, QTableWidgetItem(str(value[7])))
            self.log_tableWidget.setItem(row, 8, QTableWidgetItem(str(value[8])))

    def exit_database_enlarge(self):
        self.groupBox.hide()

    def detail_sensors_show(self):
        self.groupBox_2.show()

    
    def exit_sensors(self):
        self.groupBox_2.hide()    

    def show_database_enlarge(self):
        self.groupBox.show()    

    def show_notnull_data(self):
        self.cursor.execute("""SELECT *FROM fireIncident 
                            WHERE flame_occurrence IS NOT NULL 
                            AND flame_sensor IS NOT NULL 
                            AND flame_value IS NOT NULL 
                            AND gas_occurrence IS NOT NULL 
                            AND gas_sensor IS NOT NULL
                            AND gas_value AND termination IS NOT NULL 
                            AND termination_info IS NOT NULL;""")  
        self.log_tableWidget_2.setRowCount(0);  
        for value in self.cursor.fetchall():
            
            row  = self.log_tableWidget_2.rowCount() 
            self.log_tableWidget_2.insertRow(row)
            self.log_tableWidget_2.setItem(row, 0, QTableWidgetItem(str(value[0])))
            self.log_tableWidget_2.setItem(row, 1, QTableWidgetItem(str(value[1])))
            self.log_tableWidget_2.setItem(row, 2, QTableWidgetItem(str(value[2])))
            self.log_tableWidget_2.setItem(row, 3, QTableWidgetItem(str(value[3])))
            self.log_tableWidget_2.setItem(row, 4, QTableWidgetItem(str(value[4])))
            self.log_tableWidget_2.setItem(row, 5, QTableWidgetItem(str(value[5])))
            self.log_tableWidget_2.setItem(row, 6, QTableWidgetItem(str(value[6])))
            self.log_tableWidget_2.setItem(row, 7, QTableWidgetItem(str(value[7])))
            self.log_tableWidget_2.setItem(row, 8, QTableWidgetItem(str(value[8])))        
        
    #enlarge database putout
    def print_database_enlarge(self):
        
        self.cursor.execute("select * from fireIncident")  

        self.log_tableWidget_2.setRowCount(0);  
        for value in self.cursor.fetchall():
            
            row  = self.log_tableWidget_2.rowCount() 
            self.log_tableWidget_2.insertRow(row)
            self.log_tableWidget_2.setItem(row, 0, QTableWidgetItem(str(value[0])))
            self.log_tableWidget_2.setItem(row, 1, QTableWidgetItem(str(value[1])))
            self.log_tableWidget_2.setItem(row, 2, QTableWidgetItem(str(value[2])))
            self.log_tableWidget_2.setItem(row, 3, QTableWidgetItem(str(value[3])))
            self.log_tableWidget_2.setItem(row, 4, QTableWidgetItem(str(value[4])))
            self.log_tableWidget_2.setItem(row, 5, QTableWidgetItem(str(value[5])))
            self.log_tableWidget_2.setItem(row, 6, QTableWidgetItem(str(value[6])))
            self.log_tableWidget_2.setItem(row, 7, QTableWidgetItem(str(value[7])))
            self.log_tableWidget_2.setItem(row, 8, QTableWidgetItem(str(value[8])))        
            
    # function resets DeactivateButton_counter
    def resetDeactivateButtonCounter(self):
        self.DeactivateButton_counter = 0

    # sql connect
    def initSQL(self):
        self.sql_conn = mysql.connector.connect(
        host = "192.168.0.221",
        port = 3306,
        user = "lkm",
        password = "1234",
        database = "mainServer"
        )

        self.cursor = self.sql_conn.cursor(buffered=True)

    #test
    def sql_total_sensor_insert(self):
       if(self.indoor_flag ==True):
            self.cursor.execute('''
                SELECT id FROM fireIncident ORDER BY id DESC LIMIT 1
                ''')
                # 결과 가져오기
            pri_id = self.cursor.fetchone()
            pri_id = int(pri_id[0])
            flame_value1, flame_value2, gas_value1, gas_value2 = 1,2,3,4
            self.cursor.execute("""insert into sensors (occurid, flameValue1, gasValue1, flameValue2, gasValue2) values 
                                (%s,%s,%s,%s,%s)""",(pri_id, flame_value1, flame_value2, gas_value1, gas_value2))
            
            self.sql_conn.commit()
    
            self.cursor.execute("SELECT * FROM sensors where occurid=%s", (pri_id,))
    
            self.log_tableWidget_3.setRowCount(0);  
            for value in self.cursor.fetchall():
                
                row  = self.log_tableWidget_3.rowCount() 
                self.log_tableWidget_3.insertRow(row)
                self.log_tableWidget_3.setItem(row, 0, QTableWidgetItem(str(value[0])))
                self.log_tableWidget_3.setItem(row, 1, QTableWidgetItem(str(value[1])))
                self.log_tableWidget_3.setItem(row, 2, QTableWidgetItem(str(value[2])))
                self.log_tableWidget_3.setItem(row, 3, QTableWidgetItem(str(value[3])))
                self.log_tableWidget_3.setItem(row, 4, QTableWidgetItem(str(value[4])))
                self.log_tableWidget_3.setItem(row, 5, QTableWidgetItem(str(value[5])))

    #sql data insert
    def sql_data_insert(self):
        #occurr_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        occurr_time = datetime.now()
        occur_flame = 0
        ocuur_gas=0
        occur_flame_loc =0
        occur_gas_loc=0
        
        if(self.curr_IS==1):
            if(self.sensor_loc==1):
                self.cursor.execute("""insert into fireIncident (flame_occurrence, flame_sensor, flame_value) values 
                            (%s,%s,%s)""",(occurr_time, self.sensor_loc,flame_value1))
                

            elif(self.sensor_loc==2):
                self.cursor.execute("""insert into fireIncident (flame_occurrence,gas_sensor,
                        flame_value) values 
                                (%s,%s,%s)""",(occurr_time,self.sensor_loc,flame_value2))
        elif(self.curr_IS==2):       
            if(self.sensor_loc==1):
                self.cursor.execute("""insert into fireIncident (gas_occurrence,gas_sensor,gas_value) values 
                            (%s,%s,%s)""",(occurr_time,self.sensor_loc,gas_value1))
            elif(self.sensor_loc==2):
                self.cursor.execute("""insert into fireIncident (gas_occurrence,gas_sensor,
                        gas_value) values 
                                (%s,%s,%s)""",(occurr_time,self.sensor_loc,gas_value2)) 
        else:
            if(flame_value1 > flame_value2):
                occur_flame_value = flame_value1
                occur_flame_loc =1
            else:
                occur_flame_value = flame_value2
                occur_flame_loc =2   

            if(gas_value1 > gas_value2):
                occur_gas_value = gas_value1
                occur_gas_loc=1
            else:
                occur_gas_value = gas_value2
                occur_gas_loc=2   

            self.cursor.execute("""insert into fireIncident (flame_occurrence,flame_sensor,flame_value,
                    gas_occurrence, gas_sensor, gas_value) values 
                (%s,%s,%s,%s,%s,%s)""",(occurr_time,occur_flame_loc,occur_flame_value, occurr_time,occur_gas_loc,occur_gas_value))
            
        self.sql_conn.commit()     
        self.print_database()
        self.print_database_enlarge()

    #sql data update
    def sql_data_update(self,data=3):
        occurr_time = datetime.now()
        occur_flame = 0
        ocuur_gas=0
        occur_flame_loc =0
        occur_gas_loc=0
        if(flame_value1 > flame_value2):
            occur_flame_value = flame_value1
            occur_flame_loc =1
        else:
            occur_flame_value = flame_value2
            occur_flame_loc =2   
        if(gas_value1 > gas_value2):
            occur_gas_value = gas_value1
            occur_gas_loc=1
        else:
            occur_gas_value = gas_value2
            occur_gas_loc=2   
        self.cursor.execute('''
            SELECT id FROM fireIncident ORDER BY id DESC LIMIT 1
            ''')
            # 결과 가져오기
        latest_id = self.cursor.fetchone()
        latest_id = int(latest_id[0])

        
        if(self.prev_IS==1 and self.curr_IS==3):
            self.cursor.execute("""update fireIncident SET gas_occurrence=%s, gas_sensor=%s, gas_value=%s WHERE id =%s
                        """,(occurr_time,occur_gas_loc,occur_gas_value, latest_id))
            
        elif(self.prev_IS==2 and self.curr_IS==3):
            self.cursor.execute("""update fireIncident SET gas_occurrence=%s, gas_sensor=%s, gas_value=%s WHERE id =%s
                        """,(occurr_time, occur_flame_loc, occur_flame_value, latest_id))
        elif(self.curr_IS==0):
            
            if(data==3):
                self.cursor.execute("""update fireIncident SET termination=%s, termination_info=%s WHERE id =%s
                            """,(occurr_time,"button clicked" ,latest_id))
            else:
                self.cursor.execute("""update fireIncident SET termination=%s, termination_info=%s WHERE id =%s
                            """,(occurr_time,"RFID TAG" ,latest_id))
        self.sql_conn.commit()         
        self.print_database()
        self.print_database_enlarge()
    # test funciton
    def gas1test(self):
        global gas_value1
        gas_value1 += 10
    def gas2test(self):
        global gas_value2
        gas_value2 += 10
    def flame1test(self):
        global flame_value1
        flame_value1 += 10
    def flame2test(self):
        global flame_value2
        flame_value2 += 10

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
        global flame_value1, flame_value2, gas_value1, gas_value2
        self.gas_value1_label.setText(str(gas_value1))
        self.gas_value2_label.setText(str(gas_value2))
        self.flame_value1_label.setText(str(flame_value1))
        self.flame_value2_label.setText(str(flame_value2))

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
        global flame_value1, flame_value2, gas_value1, gas_value2
        self.gas_value1_label.setText(str(gas_value1))
        self.gas_value2_label.setText(str(gas_value2))
        self.flame_value1_label.setText(str(flame_value1))
        self.flame_value1_label.setText(str(flame_value2))

        self.flag_list[0]=(1 if (flame_value1 > self.flame_criterion) else self.flag_list[0])
        self.flag_list[1]=(1 if (gas_value1 > self.gas_criterion) else self.flag_list[1])
        self.flag_list[2]=(1 if (flame_value2 > self.flame_criterion) else self.flag_list[2])
        self.flag_list[3]=(1 if (gas_value2 > self.gas_criterion) else self.flag_list[3])
        
        if self.sensor_loc == 0:
            if 1 in self.flag_list:
                if 1 in self.flag_list[0:2]:
                    self.sensor_loc = 1
                    self.x_degree = 60
                elif 1 in self.flag_list[2:]:
                    self.sensor_loc = 2
                    self.x_degree = 150
                else:
                    pass
            else:
                self.sensor_loc = 0
        gas_fire_flag = (self.flag_list[1]+self.flag_list[3] != 0, self.flag_list[0]+self.flag_list[2] != 0)
        print(gas_fire_flag)
        # print(self.flag_list.index(1)/2)
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
                if(self.prev_IS !=0):
                    self.sql_data_update() ##############################################db 업데이트 하는 곳
            if self.indoor_flag == False:
                self.RFID_timer.start()
                self.clickCamera() #displayCamera check indoor_flag and turn on if flag is true, off when false
                                        # or separate to activeCamera() deactiveCamera()
                self.sql_data_insert() #상황 발생 시 db 데이터 삽입 *********수정가능*******

            self.indoor_flag = True
            self.enable_cam_deactivate()
            if 1 in [self.flag_list[0],self.flag_list[2]]:
                self.enable_ventilation_button()
            else:
                self.disable_ventilation_button()
            print("flag_list")
            print(self.flag_list)

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
    def deactivateButton(self, data = 3):
        print("deactive")
        print("data값은 : " ,data, "입니다")
        if data == 0:
            QMessageBox.critical(self,"Error", "unknown error",QMessageBox.Ok)
        elif data ==1:
            QMessageBox.critical(self,"Error", "has occured, unauthorized",QMessageBox.Ok)

        else:
            self.DeactivateButton_counter +=1
            self.sensor_loc = 0
            self.prev_IS = 0
            self.curr_IS = 0
            self.x_degree = 105
            self.y_degree = 30
            self.send_safeC(b"IS",0,self.sensor_loc)
            self.gas_led_button.setStyleSheet("background-color: white")
            self.flame_led_button.setStyleSheet("background-color: white")

            self.indoor_flag = False
            self.RFID_timer.stop()

         #   self.clickCamera()
            #############33

            self.disable_cam_deactivate()
            self.disable_ventilation_button()
            self.ventilation_flag = False

            self.flag_list = [0,0,0,0]
            self.cam_label.clear()

            print("deactivateButton")
            print(self.prev_IS,self.curr_IS)
            
            self.sql_data_update(data) #############################################db update 하는곳
            if self.DeactivateButton_counter >=3:
                sys.exit()

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

        if self.x_degree >self.camera_left_limit:
            self.x_degree = self.camera_left_limit

        if self.x_degree == 10:
            self.x_degree = 11
        self.send_safeC(b"CC",self.x_degree,self.y_degree)
        print("cameraLeftButton")
    
    # function of cameraRightButton
    def cameraRightButton(self):
        self.x_degree -= 10

        if self.x_degree <self.camera_right_limit:
            self.x_degree = self.camera_right_limit

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
        self.video = cv2.VideoCapture(2)
    
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