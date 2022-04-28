const int NUM = 8;
int pwm_pins[NUM] = {2, 3, 4, 5, 6, 7, 8, 9};

void setup()
{
	Serial.begin(115200);
	for (int i = 0; i < NUM; i++)
		pinMode(pwm_pins[i], OUTPUT);
}

void loop()
{
	delay(10); // TODO: use clock

	String out_packet = String("");
	for (int i = 0; i < NUM; i++)
	{
		int val = analogRead(i);
		out_packet += String(val) + "|";
	}
	Serial.println(out_packet);


	String in_packet = Serial.readStringUntil('\n');
	for (int i = 0; i < NUM; i++)
	{
		int val = in_packet.substring(5 * i, 5 * i + 4).toInt();
		analogWrite(pwm_pins[i], val / 4);
		// analogRead values go from 0 to 1023, analogWrite values from 0 to 255
	}
}
