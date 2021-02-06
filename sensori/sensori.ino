const uint8_t sensorsNumber = 1;
uint16_t sensorValues[sensorsNumber];
uint16_t sensorPins[sensorsNumber]={};


void setup() {
  Serial.begin(9600);
  for(int i=0;i<sensorsNumber;++i){
    sensorPins[i]=14+i;
  }
}

void loop() {

  
  for(int i=0;i<sensorsNumber;++i){
    sensorValues[i]=analogRead(sensorPins[i]);
  }
  sendMessage(sensorValues,sensorsNumber);
  
  delay(1000);
  
}

void sendMessage(uint16_t sensorValues[],int sensorsNumber){
  uint16_t mask   = B11111111;     
  uint8_t first_half;   
  uint8_t sencond_half; 
  
  Serial.write(0xff);
  Serial.write(0xff);

  Serial.write(0x00);
  Serial.write(sensorsNumber);

  for(int i=0;i<sensorsNumber;++i){
    first_half = sensorValues[i] >> 8;
    sencond_half = sensorValues[i] & mask;
    Serial.write(first_half);
    Serial.write(sencond_half);    
  }
    
  Serial.write(0xff);
  Serial.write(0xfe);
}
