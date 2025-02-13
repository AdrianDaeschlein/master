#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads; // Create an ADS1115 instance

void setup()
{
    Serial.begin(115200);
    while (!Serial)
        ; // Wait for Serial Monitor to open
    // Serial.println("Initializing ADS1115...");

    if (!ads.begin())
    {
        // Serial.println("Failed to initialize ADS1115!");
        while (1)
            ;
    }

    // Set Gain: 0 = ±6.144V, 1 = ±4.096V, 2 = ±2.048V, 4 = ±1.024V, 8 = ±0.512V, 16 = ±0.256V
    // ads.setGain(GAIN_ONE);  // ±4.096V range (adjust as needed)
    ads.setGain(GAIN_EIGHT);
    ads.setDataRate(RATE_ADS1115_475SPS);

    // Serial.println("ADS1115 initialized.");
}

void loop()
{
    int16_t rawValue = ads.readADC_Differential_0_1(); // Read differential voltage A0 - A1
    float voltage = ads.computeVolts(rawValue);        // Convert to voltage

    // Serial.print("Raw ADC: ");
    Serial.println(rawValue);
    // Serial.print("\tVoltage: ");
    // Serial.print(voltage, 6);
    // Serial.println(" V");

    delay(10); // Adjust as needed
}
