import data_read.data_read as dr
import os
import time

dr.BAUD_RATE = 115200

def main():
    print("Select the hardware you are using: ")
    print("1. MPU6050")
    print("2. geophone")
    hardware_choice = input("Enter your choice (1 or 2): ")

    if hardware_choice == "1":
        hardware_folder = "MPU6050"
    elif hardware_choice == "2":
        hardware_folder = "geophone"
    else:
        print("Invalid hardware selection. Exiting...")
        return

    LED = int(input("Do you want to turn on the LED? (1/0): "))

    time_1_or_samples_0 = int(input(
        "Do you want to record for a fixed time (3s) (1) or a fixed number of samples (500) (0)?: "))

    print("What do you want to do?")
    print("1. Save data - manual")
    print("2. Save data - automatic")
    choice = input("Enter your choice (1 or 2): ")

    # Get the absolute path of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Use the hardware-specific folder
    data_folder = os.path.join(script_dir, hardware_folder)

    # Create the hardware folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    if choice == "1":
        n = input("How many recordings? ")
        m_name = input("Enter the name of the merged file: ")

        for i in range(int(n)):
            print("")
            print("RUN " + str(i + 1))
            dr.file_name = m_name + str(i + 1) + ".csv"
            dr.record_csv(
                LED, n=1, time_1_or_samples_0=time_1_or_samples_0, samples=500, duration=3)

            input("Recording number " + str(i + 1) +
                  " done. Press enter to continue.")

        # Build the full file path: hardware_folder/<m_name>.csv
        csv_file_path = os.path.join(data_folder, f"{m_name}.csv")

        for i in range(int(n)):
            # Read the data from the individual files as a list [x1, x2, x3, ...]
            with open(m_name + str(i + 1) + ".csv", "r") as f:
                data = f.read().split(",")

            # Append the data to the merged file in the hardware folder
            with open(csv_file_path, "a") as f:
                f.write(",".join(data))

        # Delete the individual data files
        for i in range(int(n)):
            os.remove(m_name + str(i + 1) + ".csv")

    elif choice == "2":
        n = int(input("How many recordings? "))
        m_name = input("Enter the name of the merged file: ")

        time.sleep(5)

        dr.file_name = m_name + ".csv"
        dr.record_csv(
            LED, n=n, time_1_or_samples_0=time_1_or_samples_0, samples=500, duration=3)

        # Move the merged file to the hardware-specific folder
        csv_file_path = os.path.join(data_folder, f"{m_name}.csv")
        os.rename(m_name + ".csv", csv_file_path)

    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
