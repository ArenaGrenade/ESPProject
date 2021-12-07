const int AirValue = 3600;
const int WaterValue = 1400;
const int SensorPin = 15;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  int soilMoistureValue = analogRead(SensorPin);
  int soilmoisturepercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);
  if(soilmoisturepercent < 0)
  {
    soilmoisturepercent = 0;
  }
  if(soilmoisturepercent > 100)
  {
    soilmoisturepercent = 100;
  }
  Serial.println(soilMoistureValue);
  Serial.print(soilmoisturepercent);
  Serial.println(" %");
  delay(500);
}
