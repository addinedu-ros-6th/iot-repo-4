#include <SPI.h>

void toBytes(byte* buffer, int data, int offset=0)
{
  buffer[offset] = data & 0xFF;
  buffer[offset +1] = (data >> 8) & 0xFF;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  SPI.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  int recv_size = 0;
  char recv_buffer[16];

  uint64_t flameInfo1 = analogRead(A0);
  // Serial.print("flame1: ");
  // Serial.println(flameInfo1);


  int gasInfo1 = analogRead(A1);
  // Serial.print("gas1: ");
  // Serial.println(gasInfo1);

  int flameInfo2 = analogRead(A2);
  // Serial.print("flame2: ");
  // Serial.println(flameInfo2);

  int gasInfo2 = analogRead(A3);
  // Serial.print("gas2: ");
  // Serial.println(gasInfo1);
  // String f1 = String(flameInfo1);
  if (Serial.available() > 0) {
    recv_size = Serial.readBytesUntil('\n', recv_buffer, 16);
  }

  if (recv_size > 0) {
    char cmd[2];
    memset(cmd, 0x00, sizeof(cmd));
    memcpy(cmd, recv_buffer, 2);

    char send_buffer[19];
    memset(send_buffer, 0x00, sizeof(send_buffer));
    memcpy(send_buffer, cmd, 2);

    byte int_buffer[4];
    
    if (strncmp(cmd, "GS", 2) == 0) {
      // memcpy(send_buffer+2, &flameInfo1, 4);
      memset(int_buffer,0x00,sizeof(int_buffer));
      toBytes(int_buffer,flameInfo1);
      memcpy(send_buffer+2, &int_buffer, 4);

      memset(int_buffer,0x00,sizeof(int_buffer));
      toBytes(int_buffer,gasInfo1);
      memcpy(send_buffer + 6, &int_buffer, 4);

      memset(int_buffer,0x00,sizeof(int_buffer));
      toBytes(int_buffer,flameInfo2);
      memcpy(send_buffer + 10, &int_buffer, 4);

      memset(int_buffer,0x00,sizeof(int_buffer));
      toBytes(int_buffer,gasInfo2);
      memcpy(send_buffer + 14, &int_buffer, 4);
      send_buffer[18] = '\n';
      Serial.write(send_buffer,19);
      // Serial.println(int_buffer,4);
      // for(int i =0;i<19;i++){
      // Serial.println();

      
    }
  }
}
