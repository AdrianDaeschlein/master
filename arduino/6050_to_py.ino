#include <Wire.h> // Include the Wire library for I2C communication

const int MPU_ADDR = 0x68; // MPU6050 I2C address
float AccX, AccY, AccZ;    // Variables to store accelerometer data

void setup()
{
    Wire.begin();                     // Initialize I2C communication
    Wire.beginTransmission(MPU_ADDR); // Start communication with MPU6050
    Wire.write(0x6B);                 // Access the power management register
    Wire.write(0);                    // Wake up the MPU6050
    Wire.endTransmission(true);

    Serial.begin(9600); // Start Serial Monitor at 9600 baud rate
    Serial.println("Streaming accelerometer data...");
}

void loop()
{
    // Read accelerometer data
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B); // Start reading at register 0x3B
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDR, 6, true);

    // Combine high and low bytes for each axis and scale to 'g'
    AccX = (Wire.read() << 8 | Wire.read()) / 16384.0;
    AccY = (Wire.read() << 8 | Wire.read()) / 16384.0;
    AccZ = (Wire.read() << 8 | Wire.read()) / 16384.0;

    // Send accelerometer data to Serial
    Serial.print(AccX);
    Serial.print("\t");
    Serial.print(AccY);
    Serial.print("\t");
    Serial.println(AccZ);

    // Add a small delay for stability (optional, can be tuned as needed)
    delay(10); // 10 ms delay gives approx. 100 Hz sampling rate
}
