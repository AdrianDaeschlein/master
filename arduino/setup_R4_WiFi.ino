#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "Arduino_LED_Matrix.h"

Adafruit_MPU6050 mpu;
ArduinoLEDMatrix matrix;

byte frame[8][12] = {0};  // LED matrix frame buffer
bool recording = false;   // Tracking recording state

void setup() {
    Serial.begin(115200);
    while (!Serial);  // Wait for Python to connect

    // Initialize MPU6050
    if (!mpu.begin()) {
        Serial.println("Failed to find MPU6050 chip");
        while (1) { delay(10); }
    }

    // Configure MPU6050 settings
    mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    // Initialize LED matrix
    matrix.begin();
    matrix.clear();
    matrix.renderBitmap(frame, 8, 12);
}

void loop() {
    // **Check for Serial input from Python**
    if (Serial.available()) {
        char command = Serial.read();  // Read 1-byte command

        if (command == 'R') {  
            recording = true;
            drawRedSquare();  // Show red square when recording starts
        } 
        else if (command == 'S') {  
            recording = false;
            clearMatrix();  // Clear matrix when recording stops
        }
    }

    // **Read accelerometer data**
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Print acceleration Z-axis data
    Serial.println(a.acceleration.z);

    delay(10);  // Small delay to prevent excessive CPU usage
}

// **Draw a Red Square on LED Matrix**
void drawRedSquare() {
    memset(frame, 0, sizeof(frame));  // Clear frame buffer

    // Fill a 4x4 square in the center
    for (int x = 4; x < 8; x++) {
        for (int y = 2; y < 6; y++) {
            frame[y][x] = 1;
        }
    }

    matrix.renderBitmap(frame, 8, 12);  // ✅ Update LED matrix
}

// **Clear the LED Matrix**
void clearMatrix() {
    memset(frame, 0, sizeof(frame));  // Reset all LEDs
    matrix.renderBitmap(frame, 8, 12);
}
