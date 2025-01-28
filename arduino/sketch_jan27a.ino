#include <Wire.h> // Include the Wire library for I2C communication

const int MPU_ADDR = 0x68; // MPU6050 I2C address
float AccX, AccY, AccZ;    // Variables to store accelerometer data
bool recordData = false;   // Flag to start recording data
unsigned long startTime = 0;

void setup()
{
  Wire.begin();                     // Initialize I2C communication
  Wire.beginTransmission(MPU_ADDR); // Start communication with MPU6050
  Wire.write(0x6B);                 // Access the power management register
  Wire.write(0);                    // Wake up the MPU6050
  Wire.endTransmission(true);

  Serial.begin(9600); // Start Serial Monitor at 9600 baud rate
  Serial.println("Send 'START' to record data for 3 seconds...");
}

void loop()
{
  // Check for a command from Serial Monitor
  if (Serial.available())
  {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any trailing whitespace
    if (command.equalsIgnoreCase("START"))
    {
      Serial.println("Recording data for 3 seconds...");
      recordData = true;
      startTime = millis(); // Mark the start time
    }
  }

  // Record data if the flag is set
  if (recordData)
  {
    unsigned long currentTime = millis();
    if (currentTime - startTime <= 3000)
    {
      // Read accelerometer data
      Wire.beginTransmission(MPU_ADDR);
      Wire.write(0x3B);
      Wire.endTransmission(false);
      Wire.requestFrom(MPU_ADDR, 6, true);
      AccX = (Wire.read() << 8 | Wire.read()) / 16384.0;
      AccY = (Wire.read() << 8 | Wire.read()) / 16384.0;
      AccZ = (Wire.read() << 8 | Wire.read()) / 16384.0;

      // Print data for Serial Plotter
      Serial.print(AccX);
      Serial.print("\t");
      Serial.print(AccY);
      Serial.print("\t");
      Serial.println(AccZ);
    }
    else
    {
      // Stop recording after 3 seconds
      recordData = false;
      Serial.println("Recording complete! Check the Serial Plotter for the graph.");
    }
  }
}
