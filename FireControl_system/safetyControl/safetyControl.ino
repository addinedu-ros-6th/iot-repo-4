#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

const int RST_PIN = 9;
const int SS_PIN = 10;
int R_LED = 2;
int Y_LED = 3;
int BUZZER = 4;

MFRC522 rc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

Servo cam_ver_servo;
Servo cam_hor_servo;

Servo fan_servo;
Servo door_top_servo;
Servo door_btm_servo;


int indoor_stat = 0;
int prev_pos = 0;

int default_pos[3][2] = {{115, 30}, {60, 30}, {150, 30}}; //middle, right, left (front door pov)
int degree_xy[2] = {105, 30};

const byte adminCards[2][4] = {
  {0xC3, 0x5C, 0xB7, 0x0F}, //card
  {0x63, 0xEB, 0x40, 0xFA} //tag
};


// ----------------------------------------------------------------------------------------------------

void fan_activation(int activate) {
  static int prev_activate = 0;
  static bool fan_active = false; // To keep track of whether the fan is running

  if (activate == 1 || fan_active) {
    prev_activate = 1;
    fan_active = true; // Mark the fan as active
    int pos = 0;
    for (pos = 0; pos <= 180; pos += 2) {
      fan_servo.write(pos); // start fan rotation (180 degrees)
      delay(15);
    }
    for (pos = 180; pos >= 0; pos -= 2) {
      fan_servo.write(pos); // start fan rotation (90 degrees)
      delay(15);
    }
    for (pos = 0; pos <= 180; pos += 2) {
      fan_servo.write(pos); // start fan rotation (180 degrees)
      delay(15);
    }
    for (pos = 180; pos >= 0; pos -= 2) {
      fan_servo.write(pos); // start fan rotation (90 degrees)
      delay(15);
    }
  }
  else {
    prev_activate = 0;
    fan_active = false; // Mark the fan as inactive
    fan_servo.write(0); // stop the fan
    // fan_servo.detach();
  }
}

// ----------------------------------------------------------------------------------------------------


void printUID(byte *uid, byte length) {
    for (byte i = 0; i < length; i++) {
        if (uid[i] < 0x10) Serial.print("0");  // Add leading zero if necessary
        Serial.print(uid[i], HEX);
        if (i < length - 1) Serial.print(" "); // Add space between bytes
    }
    Serial.println();
}

// ---------------------------------------------------------------------------------------------------



void deactivateAlarm() {
  digitalWrite(R_LED, LOW);
  digitalWrite(Y_LED, LOW);
  noTone(BUZZER);
  door_top_servo.write(0);
  door_btm_servo.write(0);
  cam_hor_servo.write(degree_xy[0]);
  cam_ver_servo.write(degree_xy[1]);
  fan_servo.write(0);
}

// ----------------------------------------------------------------------------------------------------


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  SPI.begin();
  rc522.PCD_Init();

  // Initialize Pins
  pinMode(R_LED, OUTPUT);
  pinMode(Y_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  cam_ver_servo.attach(A0);
  cam_hor_servo.attach(A1);

  fan_servo.attach(A3);
  door_top_servo.attach(A4);
  door_btm_servo.attach(A5);

  // Set initial positions
  fan_servo.write(0);
  door_top_servo.write(0);
  door_btm_servo.write(0);
  cam_hor_servo.write(degree_xy[0]);
  cam_ver_servo.write(degree_xy[1]);

  // default key for MFRC522
  for (int i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
}


void loop() {

  int recv_size = 0;
  char recv_buffer[11]; // buffer to hold incoming data

  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    recv_size = Serial.readBytesUntil('\n', recv_buffer, 11); // Read data into recv_buffer until newline or 11 bytes
  }

  if (recv_size > 0) { 
    // Get command ID

    char cmd[2];
    memset(cmd, 0x00, sizeof(cmd));
    memcpy(cmd, recv_buffer, 2); // Copy the first 2 bytes to cmd (Command ID)

    char send_buffer[7];
    memset(send_buffer, 0x00, sizeof(send_buffer));
    memcpy(send_buffer, cmd, 2); // Copy the Command ID to the send buffer

    // Process the command based on its type
    if (strncmp(cmd, "IS", 2) == 0) { // Check if the command is "IS" (Indoor Status)
      int current_pos;
      memcpy(&indoor_stat, recv_buffer + 2 , 4); // Copy 4 bytes from recv_buffer starting at position 2 to the integer temporary status
      memcpy(&current_pos, recv_buffer + 6 , 4); // Copy 4 bytes from recv_buffer starting at position 6 to the integer temporary coordinate

      //compares the previous state. move the cam servos in all scenarios except when the previous state is 0 (or 3) and the indoor status is 0 or 3.
      if (!(prev_pos == current_pos)) {
        degree_xy[0] = default_pos[current_pos][0]; 
        degree_xy[1] = default_pos[current_pos][1];
        cam_hor_servo.write(degree_xy[0]);
        cam_ver_servo.write(degree_xy[1]);
        delay(10);
      }

      if (indoor_stat == 0) { //normal (default) state
        deactivateAlarm();
        // Serial.println("IS - Normal(0) SafetyControl");
      }
      
      else if (indoor_stat == 1) { //flame sensor detected
        digitalWrite(R_LED, HIGH);
        digitalWrite(Y_LED, LOW);
        tone(BUZZER, 500);
        door_top_servo.write(120);
        door_btm_servo.write(120);
        delay(15);
        // Serial.println("IS - Flame(1) SafetyControl");
      }

      else if (indoor_stat == 2) { //gas sensor detected
        digitalWrite(R_LED, LOW);
        digitalWrite(Y_LED, HIGH);
        tone(BUZZER, 500);
        door_top_servo.write(120);
        door_btm_servo.write(120);
        delay(15);
        fan_activation(1);
        // Serial.println("IS - Gas(2) SafetyControl");

      }
      
      else if (indoor_stat == 3) { //both sensor detected, fire break out
        digitalWrite(R_LED, HIGH);
        digitalWrite(Y_LED, HIGH);
        tone(BUZZER, 5000);
        door_top_servo.write(120);
        door_btm_servo.write(120);
        delay(15);
        // Serial.println("IS - Both(3) SafetyControl");
      }

      prev_pos = current_pos; //store the current status as previous state for later use

    }
    else if (strncmp(cmd, "CC", 2) == 0) { //camera control

      int x_degree = 0;
      int y_degree = 0;

      Convert bytes to integers correctly considering the endianess
      x_degree = (int)recv_buffer[2] |
                ((int)recv_buffer[3] << 8) |
                ((int)recv_buffer[4] << 16) |
                ((int)recv_buffer[5] << 24);

      y_degree = (int)recv_buffer[6] |
                ((int)recv_buffer[7] << 8) |
                ((int)recv_buffer[8] << 16) |
                ((int)recv_buffer[9] << 24);

      cam_hor_servo.write(x_degree);
      cam_ver_servo.write(y_degree);

    }
    else if (strncmp(cmd, "VC", 2) == 0) { //ventilation control
      int vent_stat;
      memcpy(&vent_stat, recv_buffer + 2 , 4);
      // Serial.println(vent_stat);
      fan_activation(vent_stat);
    }
    else if (strncmp(cmd, "GR", 2) == 0) {
      int auth_state = 0;
      bool newCard = rc522.PICC_IsNewCardPresent();
      bool readCard = rc522.PICC_ReadCardSerial();

      if (newCard && readCard) {

          if (memcmp(rc522.uid.uidByte, adminCards[0], 4) == 0) { //compare tagged card info and registered admin card info
            deactivateAlarm(); //alarm deactivates once a registered admin card tagged
            auth_state = 2;
            // Serial.println("The fire alarm has been deactivated by the admin.");
          }
          else if (memcmp(rc522.uid.uidByte, adminCards[1], 4) == 0) { //compare tagged card info and registered admin card info
            deactivateAlarm(); 
            auth_state = 2;
            // Serial.println("The fire alarm has been deactivated by the admin.");
          }
          else {
            auth_state = 1; //unauthorized access
            // Serial.println("Unauthorized access. Please try again.");
          }
          memset(send_buffer, 0x00, sizeof(send_buffer)); //clear the send_buffer
          memcpy(send_buffer, "GR", 2); // Add GR to the send buffer
          memcpy(send_buffer + 2, &auth_state, sizeof(auth_state)); // Add auth state to the send buffer
          send_buffer[6] = '\n';
          Serial.write(send_buffer, 7);     // Send response
        }
      
      else {
        memset(send_buffer, 0x00, sizeof(send_buffer)); //clear the send_buffer
        memcpy(send_buffer, "GR", 2); // Add GR to the send buffer
        // send_buffer[2] = 0; //0 unknown error
        auth_state = 0;

        memcpy(send_buffer + 2, &auth_state, sizeof(auth_state)); // Add auth state to the send buffer
        send_buffer[6] = '\n';
        Serial.write(send_buffer, 7);     // Send response
        // Serial.println("Unknown/No card. Please try again.");
      }
    }
  }
}

