void setup() {
  Serial.begin(9600);          //  setup serial
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  
  int val = analogRead(0);    // read the input pin
  Serial.println(val);             // debug value
}
