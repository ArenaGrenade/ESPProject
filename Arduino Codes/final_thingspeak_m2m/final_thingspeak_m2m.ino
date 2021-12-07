#include <Wire.h>
#include <BH1750.h>
#include <WiFi.h>
#include "Adafruit_CCS811.h"
#include "Adafruit_SGP40.h"
#include "DHT.h"
#include "ThingSpeak.h"
#include "HTTPClient.h"
#include "mbedtls/aes.h"
#include "mbedtls/md.h"

#define DHTPIN 4     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SGP40 sgp;
Adafruit_CCS811 ccs;
BH1750 lightMeter;

const int AirValue = 3600;
const int WaterValue = 1400;
const int SensorPin = 15;
const char* host = "https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-29/Node-1/"; // Node-1 and Node-2 for 2 sets
const char* origin = "UFTf1YmvI7:lT47xE3PnI";
char key[] = "abcdefghijklmnop";


const char *ssid = "JioFiber_201 2.4GZ";
const char *password = "akuanki201";
const char *writeApiKey = "MW4R6SHLI6IX7KD0";
unsigned long channelNumber = 2;
int last_tsupdate = millis();
WiFiClient tsclient;

String post(String sensor, int ty, String rep)
{
  String URL = host + sensor;
  Serial.println("URL:" + URL);
  HTTPClient http;
  http.begin(URL);
  http.addHeader("Content-Type", "application/json;ty=4");
  http.addHeader("X-M2M-Origin", origin);
  http.addHeader("Accept", "application/json");
  int response = http.POST(rep);
  String text = http.getString();
  http.end();
  Serial.println(text);
  if(response > 0)
  {
    return text;
  }
  else
  {
    return "error";
  }
}
String encryption(String value)
{
  char input[value.length()+1];
  value.toCharArray(input, 1+value.length());
  unsigned char output[16];
  mbedtls_aes_context aes;
  mbedtls_aes_init( &aes );
  mbedtls_aes_setkey_enc( &aes, (const unsigned char*) key, strlen(key) * 8 );
  mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_ENCRYPT, (const unsigned char*)input, output);
  mbedtls_aes_free( &aes );
  String encrypted = "";
  for (int i = 0; i < 16; i++) {
 
    char str[3];
 
    sprintf(str, "%02x", (int)output[i]);
    encrypted = encrypted + String(str);
  }
  return encrypted;
}
String hashing(String value)
{
  char payload[value.length()+1];
  byte shaResult[32];
  value.toCharArray(payload, 1+value.length());
  const size_t payloadLength = strlen(payload);
  mbedtls_md_context_t ctx;
  mbedtls_md_type_t md_type = MBEDTLS_MD_SHA256;
  mbedtls_md_init(&ctx);
  mbedtls_md_setup(&ctx, mbedtls_md_info_from_type(md_type), 0);
  mbedtls_md_starts(&ctx);
  mbedtls_md_update(&ctx, (const unsigned char *) payload, payloadLength);
  mbedtls_md_finish(&ctx, shaResult);
  mbedtls_md_free(&ctx);
  String hashed = "";
  for(int i= 0; i< sizeof(shaResult); i++){
      char str[3];
 
      sprintf(str, "%02x", (int)shaResult[i]);
      hashed = hashed + String(str);
  }
  return hashed; 
}
String postData(String sensor, String value)
{
  String encrypted = encryption(value);
  String hashed = hashing(value);
  Serial.println(encrypted + " " + hashed);
  String rep = "{\"m2m:cin\":{"
                "\"con\": \"" + encrypted + " " + hashed + "\","
                "\"rn\": \"test-cin-last\""
                "}}";
  Serial.println(rep);
  String response = post(sensor, 4, rep);
  return response;
}


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
    postData("Temperature", String(t));
    ThingSpeak.setField(2, h);
    postData("Humidity", String(h));
    ThingSpeak.setField(3, lux);
    postData("Light", String(lux));
    ThingSpeak.setField(4, co2);
    ThingSpeak.setField(5, tvoc);
    postData("VOC1", String(tvoc));
    ThingSpeak.setField(6, raw_sgp);
    postData("VOC2", String(raw_sgp));
    ThingSpeak.setField(7, soilmoisturepercent);
    postData("Moisture", String(soilmoisturepercent));
    if(ThingSpeak.writeFields(channelNumber, writeApiKey) == 200)
    {
      Serial.println("Uploaded to ThingSpeak Server");
      last_tsupdate = millis();
    }
  }
  delay(1000); 
}
