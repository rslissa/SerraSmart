int value;
int valuePin = A0;

void setup() {
 

}

void loop() {
  value = analogRead(valuePin);
  delay(1000);
  Serial.println(value);
}
