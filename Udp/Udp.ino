/*
  firmware for ESP-Ledberg mod. Based on UDPSendReceive.pde
  set STASSID and STAPSK; will listen on port 1337.
  (c) 2019 Tobias Girstmair, GPLv3
  https://gir.st/blog/esp8266-ledberg.htm
*/


#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
typedef unsigned char uint8;

#ifndef STASSID
#define STASSID "FIXME"
#define STAPSK  "FIXME"
#endif

unsigned int localPort = 1337;      // local port to listen on
uint8 rgb[3] = {0xff, 0x6b, 0x55}; // gives nice, slightly warm, white on boot
int active = 1;
const int red = 14;
const int grn = 12;
const int blu = 13;

WiFiUDP Udp;

#define ACK 0x06
#define NAK 0x15

void setup() {
  pinMode(red, OUTPUT);
  pinMode(grn, OUTPUT);
  pinMode(blu, OUTPUT);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  Udp.begin(localPort);
}

void loop() {
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    uint8 response = NAK;
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());

    // read the packet into packetBufffer
    uint8 type;
    Udp.read(&type, 1);
    switch (type) {
    case 0: // get current power,r,g,b
      Udp.write(ACK);
      Udp.write(active);
      Udp.write(rgb[0]);
      Udp.write(rgb[1]);
      Udp.write(rgb[2]);
      break;
    case 1: // set on/off
      if (packetSize == 2) { //type+power
        active = Udp.read();
        Udp.write(ACK);
      } else {
        Udp.write(NAK);
      }
      break;
    case 2: // set rgb
      if (packetSize == 4) { //type+r+g+b
        uint8 tmp[3];
        Udp.read(tmp, 3);
        if (tmp[0]+tmp[1]+tmp[2] > 512) {
          Udp.write(NAK);
          break;
        }
        for (int i = 0; i < 3; i++) {
          rgb[i] = tmp[i];
        }
        Udp.write(ACK);
      } else {
        Udp.write(NAK);
      }
      break;
    case 3: // save color to eeprom
      Udp.write(NAK); //TODO: not implemented
      break;
    case 4: // set ssid and wpa2psk; write to non-volatile memory
      Udp.write(NAK); //TODO: not implemented
      break;
    case 5: //set static ip / dhcp 
      Udp.write(NAK); //TODO: not implemented
      break;
    default: //send nak
      Udp.write(NAK);
    }
    Udp.endPacket();
    if (active) {
      analogWrite(red, rgb[0]<<2);
      analogWrite(grn, rgb[1]<<2);
      analogWrite(blu, rgb[2]<<2);
    } else {
      analogWrite(red, 0);
      analogWrite(grn, 0);
      analogWrite(blu, 0);
    }
  }
  delay(10);
}
