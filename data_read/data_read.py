import serial
import time
import matplotlib.pyplot as plt
import sys

# ARDUINO_PORT = "/dev/cu.usbmodemF0F5BD4F35482"
ARDUINO_PORT = "/dev/cu.usbmodem14101"
BAUD_RATE = 9600
file_name = "data.csv"


def setup_serial(arduino_port, baud_rate):
    """
    Sets up the connection to the Arduino with two vars:

    Args:
        arduino_port (string): The port the Arduino is connected to
        baud_rate (int):  How much data is sent per second - 9600 default
            The higher the baud rate, the errors can occur

    Returns:
        serial.Serial | None: The serial connection
    """
    try:
        # Open the serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {arduino_port}")
        return [ser, arduino_port, baud_rate]
    except serial.SerialException:
        print("Failed to connect to Arduino. Check the port and try again.")
        return None


def read_data(ser, arduino_port, baud_rate):
    """
    Sets up the connection to the Arduino with two vars:

    Args:
        ser (serial.Serial): The serial connection object.
        arduino_port (string): The port the Arduino is connected to
        baud_rate (int):  How much data is sent per second - 9600 default
            The higher the baud rate, the errors can occur
    """
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


def read_out_data(ser, arduino_port, baud_rate):
    """
    Sets up the connection to the Arduino with two vars:

    Args:
        arduino_port (string): The port the Arduino is connected to
        baud_rate (int):  How much data is sent per second - 9600 default
            The higher the baud rate, the errors can occur

    Returns:
        string: The data from the Arduino
    """
    try:
        # Open the serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {arduino_port}")

        time.sleep(2)  # Allow time for Arduino to reset

        # Continuously read data
        while True:
            if ser.in_waiting > 0:  # Check if there is data in the buffer
                line = ser.readline().decode('utf-8').strip()  # Read and decode the data
                return line
    except serial.SerialException:
        print("Failed to connect to Arduino. Check the port and try again.")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")


def print_data_duration(ser, arduino_port, baud_rate, duration=3):
    """
    Reads and prints data from an Arduino over a serial connection for a specified duration.
    Args:
        ser (serial.Serial): The serial connection object.
        arduino_port (str): The port to which the Arduino is connected (e.g., 'COM3' or '/dev/ttyUSB0').
        baud_rate (int): The baud rate for the serial communication.
        duration (int, optional): The duration in seconds for which to read data from the Arduino. Defaults to 3 seconds.
    Raises:
        serial.SerialException: If the connection to the Arduino fails.
        KeyboardInterrupt: If the user interrupts the execution (e.g., by pressing Ctrl+C).
    """

    try:
        # Open the serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {arduino_port}")

        time.sleep(2)  # Allow time for Arduino to reset
        start_time = time.time()
        # Continuously read data
        while time.time() - start_time < duration:
            if ser.in_waiting > 0:  # Check if there is data in the buffer
                line = ser.readline().decode('utf-8').strip()  # Read and decode the data
                print(f"Data from Arduino: {line}")
        ser.close()
    except serial.SerialException:
        print("Failed to connect to Arduino. Check the port and try again.")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")


def save_data_duration(ser, arduino_port, baud_rate, duration=3):
    """
    Reads and returns data from an Arduino over a serial connection for a specified duration.
    Args:
        ser (serial.Serial): The serial connection object.
        arduino_port (str): The port to which the Arduino is connected (e.g., 'COM3' or '/dev/ttyUSB0').
        baud_rate (int): The baud rate for the serial communication.
        duration (int, optional): The duration in seconds for which to read data from the Arduino. Defaults to 3 seconds.
    Raises:
        serial.SerialException: If the connection to the Arduino fails.
        KeyboardInterrupt: If the user interrupts the execution (e.g., by pressing Ctrl+C).

    Returns:
        list of str: The data read during the specified duration.
    """
    measurements = []
    try:
        # Open the serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {arduino_port}")

        time.sleep(2)  # Allow time for Arduino to reset
        start_time = time.time()
        # Continuously read data
        while time.time() - start_time < duration:
            if ser.in_waiting > 0:  # Check if there is data in the buffer
                line = ser.readline().decode('utf-8').strip()  # Read and decode the data
                measurements.append(line)
        ser.close()
    except serial.SerialException:
        print("Failed to connect to Arduino. Check the port and try again.")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")
    return measurements


def save_data_duration_csv(ser, arduino_port, baud_rate, LED, duration=3):
    """
    Reads sensor data from Arduino and saves it to CSV.
    Optionally sends 'R' and 'S' to turn LEDs on/off if LED is True.

    Args:
        ser (serial.Serial): The serial connection object.
        arduino_port (str): Arduino's serial port.
        baud_rate (int): Baud rate.
        duration (int): Duration to record data (default: 3 seconds).
        LED (bool): Whether to send LED control commands (default: True).

    Returns:
        list: Collected measurements.
    """
    measurements = []
    try:
        # Open the serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {arduino_port}")

        time.sleep(2)  # Allow time for Arduino to reset

        # **Send 'R' to start recording if LED is enabled**
        if LED == 1:
            ser.write(b'R')
            time.sleep(0.1)  # Small delay to ensure command is sent

        start_time = time.time()

        # Continuously read data for the given duration
        while time.time() - start_time < duration:
            if ser.in_waiting > 0:  # Check if there is data in the buffer
                line = ser.readline().decode('utf-8').strip()  # Read and decode the data
                measurements.append(line)

        # **Send 'S' to stop recording if LED is enabled**
        if LED == 1:
            ser.write(b'S')
            time.sleep(0.1)  # Small delay to ensure command is sent

        ser.close()

        # Save the collected data to CSV
        measurements_to_csv(measurements)

    except serial.SerialException:
        print("Failed to connect to Arduino. Check the port and try again.")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

    return measurements


def save_data_n_samples(ser, arduino_port, baud_rate, LED, n_samples=500):
    """
    Reads a fixed number of samples from the Arduino and saves them to CSV.
    Optionally sends 'R' and 'S' to turn LEDs on/off if LED is True.

    Args:
        ser (serial.Serial): The serial connection object.
        arduino_port (str): Arduino's serial port.
        baud_rate (int): Baud rate.
        n_samples (int): Number of samples to record.
        LED (bool): Whether to send LED control commands (default: True).

    Returns:
        list: Collected measurements.
    """
    measurements = []
    try:
        # Open the serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {arduino_port}")

        time.sleep(2)  # Allow time for Arduino to reset

        # **Send 'R' to start recording if LED is enabled**
        if LED:
            ser.write(b'R')
            time.sleep(0.1)  # Small delay to ensure command is sent

        start_time = time.time()

        # Read exactly `n_samples` data points
        while len(measurements) < n_samples:
            if ser.in_waiting > 0:  # Check if there is data in the buffer
                line = ser.readline().decode('utf-8').strip()  # Read and decode the data
                measurements.append(line)

        total_time = time.time() - start_time  # Calculate total recording time

        # **Send 'S' to stop recording if LED is enabled**
        if LED:
            ser.write(b'S')
            time.sleep(0.1)  # Small delay to ensure command is sent

        ser.close()

        # Save the collected data to CSV
        measurements_to_csv(measurements)

        print(f"Recorded {total_time:.2f} seconds.")

    except serial.SerialException:
        print("Failed to connect to Arduino. Check the port and try again.")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

    return measurements


def measurements_to_csv(measurements):
    """
    Appends a list of measurements to a CSV file.

    Args:
        measurements (list of str): List of measurements to append to the CSV file.
    """
    with open(file_name, 'a') as file:
        file.write(",".join(map(str, measurements)))
        file.write("\n")
    print(f"Data saved to {file_name}")


def test_run():
    # setup
    setup_information = setup_serial(ARDUINO_PORT, BAUD_RATE)
    if setup_information:
        measurements = save_data_duration(setup_information[0],
                                          setup_information[1], setup_information[2])
    else:
        print("Failed to read setup information.")  # 3 sec run - read data
    print(len(measurements))
    plot_data(measurements)
    exit()


def plot_data(measurements):
    """
    Plots a list of numerical values as a line graph with Y-axis between 0 and 20.

    Args:
        data (list of str): List of numerical values as strings.
    """
    # Convert string values to float
    measurements = [float(value) for value in measurements]

    # Create figure and plot
    plt.figure(figsize=(10, 5))
    plt.plot(measurements, linestyle='-', marker='', color='b',
             label=f"Sensor Data; max: {max(measurements)}; min: {min(measurements)}")

    # Set axis limits
    # plt.ylim(0, 20)  # Y-axis fixed between 0 and 20
    plt.xlim(0, len(measurements))  # X-axis from 0 to the length of the data

    # Labels and title
    plt.xlabel("Sample Index")
    plt.ylabel("m/s^2")
    plt.title("MPU6050 Sensor Data")
    plt.legend()

    # Show the plot
    plt.show()


def record_csv(LED, n=10, time_1_or_samples_0=1, samples=500, duration=3):

    setup_information = setup_serial(ARDUINO_PORT, BAUD_RATE)
    if setup_information:
        ser = setup_information[0]

        for i in range(n):
            print("")
            print(f"Run {i + 1} of {n}")

            if time_1_or_samples_0 == 1:
                measurements = save_data_duration_csv(
                    ser, setup_information[1], setup_information[2], LED, duration)
            elif time_1_or_samples_0 == 0:
                measurements = save_data_n_samples(
                    ser, setup_information[1], setup_information[2], LED, samples)
            else:
                print("Invalid choice. Exiting TEST...")
                sys.exit(1)

            print(f"Run {i + 1}: {len(measurements)} measurements recorded.")

        ser.close()

    else:
        print("Failed to read setup information.")
