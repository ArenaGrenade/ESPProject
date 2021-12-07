#include <Wire.h>
#include <BH1750.h>
#include <WiFi.h>
#include "Adafruit_CCS811.h"
#include "Adafruit_SGP40.h"
#include "DHT.h"
#include "ThingSpeak.h"

#define DHTPIN 4     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SGP40 sgp;
Adafruit_CCS811 ccs;
BH1750 lightMeter;

const int AirValue = 3600;
const int WaterValue = 1400;
const int SensorPin = 15;

const char *ssid = "JioFiber_201 2.4GZ";
const char *password = "akuanki201";
const char *writeApiKey = "MW4R6SHLI6IX7KD0";
unsigned long channelNumber = 2;
int last_tsupdate = millis();
WiFiClient tsclient;

void setup()
{
  Serial.begin(115200);
  Wire.begin();
  WiFi.begin(ssid, password);
  ThingSpeak.begin(tsclient);
  
  lightMeter.begin();
  Serial.println(F("BH1750 Test begin"));
  
  Serial.println("\nI2C Scanner");
  Serial.println("CCS811 test");
  if(!ccs.begin())
  {
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }
  // Wait for the sensor to be ready
  while(!ccs.available());

  Serial.println("SGP40 test");
  if (! sgp.begin())
  {
    Serial.println("Sensor not found :(");
    while(1);
  }
  Serial.print("Found SGP40 serial #");
  Serial.print(sgp.serialnumber[0], HEX);
  Serial.print(sgp.serialnumber[1], HEX);
  Serial.println(sgp.serialnumber[2], HEX);

  Serial.println(F("DHTxx test!"));
  dht.begin();
}
 
void loop() {
  // connect to wifi
  if(WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Waiting for WiFi");
    delay(1000);
    return;
  }
  
  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");

  float co2 = -1;
  float tvoc = -1;
  if(ccs.available())
  {
    if(!ccs.readData())
    {
      co2 = ccs.geteCO2();
      tvoc = ccs.getTVOC();
      Serial.print("CO2: ");
      Serial.print(co2);
      Serial.print("ppm, TVOC: ");
      Serial.println(tvoc);
    }
    else
    {
      Serial.println("ERROR!");
      return;
    }
  }

  uint16_t raw_sgp = sgp.measureRaw();
  Serial.print("Measurement: ");
  Serial.println(raw_sgp);
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t))
  {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  float hic = dht.computeHeatIndex(t, h, false);
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C Heat index: "));
  Serial.print(hic);
  Serial.println(F("°C "));

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
//  Serial.println(soilMoistureValue);
  Serial.print("Moisture: ");
  Serial.print(soilmoisturepercent);
  Serial.println(" %");

  if(millis() - last_tsupdate > 15 * 1000)
  {
    ThingSpeak.setField(1, t);
    ThingSpeak.setField(2, h);
    ThingSpeak.setField(3, lux);
    ThingSpeak.setField(4, co2);
    ThingSpeak.setField(5, tvoc);
    ThingSpeak.setField(6, raw_sgp);
    ThingSpeak.setField(7, soilmoisturepercent);
    if(ThingSpeak.writeFields(channelNumber, writeApiKey) == 200)
    {
      Serial.println("Uploaded to ThingSpeak Server");
      last_tsupdate = millis();
    }
  }
  delay(1000); 
}
