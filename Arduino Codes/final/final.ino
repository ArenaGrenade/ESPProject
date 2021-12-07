#include <Wire.h>
#include <BH1750.h>
#include "Adafruit_CCS811.h"
#include "Adafruit_SGP40.h"
#include "DHT.h"


#define DHTPIN 4     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SGP40 sgp;
Adafruit_CCS811 ccs;
BH1750 lightMeter;

const int AirValue = 3600;
const int WaterValue = 1400;
const int SensorPin = 15;

 
void setup() {
  Wire.begin();
  
  lightMeter.begin();
  Serial.println(F("BH1750 Test begin"));
  
  Serial.begin(115200);
  Serial.println("\nI2C Scanner");

  Serial.println("CCS811 test");

  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }

  // Wait for the sensor to be ready
  while(!ccs.available());

  Serial.println("SGP40 test");

  if (! sgp.begin()){
    Serial.println("Sensor not found :(");
    while (1);
  }
  Serial.print("Found SGP40 serial #");
  Serial.print(sgp.serialnumber[0], HEX);
  Serial.print(sgp.serialnumber[1], HEX);
  Serial.println(sgp.serialnumber[2], HEX);

  Serial.println(F("DHTxx test!"));
  dht.begin();
}
 
void loop() {
  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  delay(1000);

  if(ccs.available()){
    if(!ccs.readData()){
      Serial.print("CO2: ");
      Serial.print(ccs.geteCO2());
      Serial.print("ppm, TVOC: ");
      Serial.println(ccs.getTVOC());
    }
    else{
      Serial.println("ERROR!");
      while(1);
    }
  }
  delay(500);

  uint16_t raw;
  raw = sgp.measureRaw();

  Serial.print("Measurement: ");
  Serial.println(raw);
  delay(1000);
  
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));

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
