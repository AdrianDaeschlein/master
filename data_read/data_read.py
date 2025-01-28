import serial
import time

# arduino_port = "/dev/tty.usbmodem14101"
arduino_port = "/dev/cu.usbmodem14101"
baud_rate = 9600  # Match this with the baud rate in your Arduino code

try:
    # Open the serial connection
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")

    time.sleep(2)  # Allow time for Arduino to reset

    # Continuously read data
    while True:
        if ser.in_waiting > 0:  # Check if there is data in the buffer
            line = ser.readline().decode('utf-8').strip()  # Read and decode the data
            print(f"Data from Arduino: {line}")
except serial.SerialException:
    print("Failed to connect to Arduino. Check the port and try again.")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
