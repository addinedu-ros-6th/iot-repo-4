#include <SPI.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  SPI.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  int recv_size = 0;
  char recv_buffer[16];

  int flameInfo1 = analogRead(A0);
  Serial.print("flame1: ");
  Serial.println(flameInfo1);


  int gasInfo1 = analogRead(A1);
  Serial.print("gas1: ");
  Serial.println(gasInfo1);

  int flameInfo2 = analogRead(A2);
  Serial.print("flame2: ");
  Serial.println(flameInfo2);

  int gasInfo2 = analogRead(A3);
  Serial.print("gas2: ");
  Serial.println(gasInfo1);

  if (Serial.available() > 0) {
    recv_size = Serial.readBytesUntil('\n', recv_buffer, 16);
  }

  if (recv_size > 0) {
    char cmd[2];
    memset(cmd, 0x00, sizeof(cmd));
    memcpy(cmd, recv_buffer, 2);

    char send_buffer[18];
    memset(send_buffer, 0x00, sizeof(send_buffer));
    memcpy(send_buffer, cmd, 2);

    if (strncmp(cmd, "GS", 2) == 0) {
      memset(send_buffer+2, flameInfo1, 4);
      memset(send_buffer + 6, gasInfo1, 4);
      memset(send_buffer + 10, flameInfo2, 4);
      memset(send_buffer + 14, gasInfo2, 4);
      Serial.write(send_buffer, 18);
      Serial.println();
    }
  }
}
