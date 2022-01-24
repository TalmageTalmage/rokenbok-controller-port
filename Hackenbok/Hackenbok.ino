/*
 * Copyright (c) 2022 Talmage
 * Licensed under the MIT License
 * See LICENSE.txt for details
*/
//Pin 2 = Serial Clock
//Pin 3 = Latch
//Pin 4 = Data

// For the UNO
#define WRITE_DATA_HIGH PORTD |= B00010000
#define WRITE_DATA_LOW PORTD &= B11101111
//For the Mega
// #define WRITE_DATA_HIGH PORTG |= B00100000 
// #define WRITE_DATA_LOW PORTG &= B11011111


volatile byte Data1 = 0;
volatile byte Data2 = 0;
volatile byte clocks = 0;



void setup(){
  Serial.begin(115200);
  attachInterrupt(0, serialClock, FALLING);
  attachInterrupt(1, latch, RISING);
  pinMode(4, OUTPUT);
  while(Serial.read() != 0x10); 
  Serial.write(0x12);

}

void loop(){
  if(Serial.available() > 1){
    Data1 = Serial.read();
    Data2 = Serial.read();
  }
}

void latch(){
    Serial.write(0x12); 
    clocks = 0;
}

void serialClock(){

  WRITE_DATA_LOW;
  
  clocks++;
  
//select
  if (Data2==0x10  && clocks ==1){
    WRITE_DATA_HIGH;
  }
//up
  else if((Data2==0x40|| Data2 == 0xc0 || Data2 == 0x42) && clocks ==6){
    WRITE_DATA_HIGH;
  }
//down
  else if((Data2==0x20|| Data2 == 0x22|| Data2 == 0xa0)  && clocks ==7){
    WRITE_DATA_HIGH;
  }
//right
  else if((Data2==0x80|| Data2 == 0xc0|| Data2 == 0xa0) && clocks ==8){
    WRITE_DATA_HIGH;
  }
//left
  else if((Data2==0x2 || Data2 == 0x42|| Data2 == 0x22) && clocks ==9){
    WRITE_DATA_HIGH;
  }
//A
  else if(Data1==0x10 && clocks ==10){
    WRITE_DATA_HIGH;
  }
  //B
  else if(Data1==0x1 && clocks ==11){
    WRITE_DATA_HIGH;
  }
  //X
  else if(Data1== 0x2&& clocks ==12){
    WRITE_DATA_HIGH;
  }
  //Y
  else if(Data1== 0x8 && clocks ==13){
    WRITE_DATA_HIGH;
  }
















}
