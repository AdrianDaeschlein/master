#include <Wire.h>
#include <Adafruit_ADS1X15.h>
// need to install "Adafruit ADS1X15 by Adafruit" library
Adafruit_ADS1115 ads; // Create an ADS1115 instance

void setup()
{
    Serial.begin(115200);
    while (!Serial)
        ; // Wait for Serial Monitor to open
    Serial.println("Initializing ADS1115...");

    if (!ads.begin())
    {
        Serial.println("Failed to initialize ADS1115!");
        while (1)
            ;
    }

    /*
    Gain sets the sensitivity of the ADC. The higher the gain, the more sensitive the ADC is to small changes in voltage.
    Possible values:
    GAIN_TWOTHIRDS (±6.144V)
    GAIN_ONE (±4.096V)
    GAIN_TWO (±2.048V)
    GAIN_FOUR (±1.024V)
    GAIN_EIGHT (±0.512V)
    GAIN_SIXTEEN (±0.256V)
     */
    // ads.setGain(GAIN_ONE);
    ads.setGain(GAIN_EIGHT);

    Serial.println("ADS1115 initialized.");
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
