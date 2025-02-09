import data_read.data_read as dr
import os

dr.BAUD_RATE = 115200


def main():

    LED = int(input("Do you want to turn on the LED? (1/0): "))

    time_1_or_samples_0 = int(input(
        "Do you want to record for a fixed time(3s) (1) or fixed number of samples(400)(0)?: "))

    print("what do you want to do?")
    print("1. Save data - manual")
    print("2. Save data - automatic")

    choice = input("Enter your choice: ")

    if choice == "1":
        n = input("How many recordings? ")
        m_name = input("Enter the name of the merged file: ")

        for i in range(int(n)):
            print("")
            print("RUN " + str(i + 1))
            dr.file_name = m_name + str(i + 1) + ".csv"
            dr.record_csv(
                LED, n=1, time_1_or_samples_0=time_1_or_samples_0, samples=400, duration=3)

            input("Recording number " + str(i + 1) +
                  " done. Press enter to continue.")

        # Get the absolute path of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the path to 'data_collection' within the script's directory
        data_folder = os.path.join(script_dir, "data_collection")

        # Build the full file path: data_collection/<m_name>.csv
        csv_file_path = os.path.join(data_folder, f"{m_name}.csv")

        for i in range(int(n)):
            # Read the data from the individual files as a individual list [x1, x2, x3, ...]
            with open(m_name + str(i + 1) + ".csv", "r") as f:
                data = f.read().split(",")

            # Create or open csv file named m_name + ".csv" in folder data
            with open(csv_file_path, "a") as f:
                # Write the data to the csv file
                f.write(",".join(data))

        # Delete the individual data files
        for i in range(int(n)):
            os.remove(m_name + str(i + 1) + ".csv")

    elif choice == "2":
        n = int(input("How many recordings? "))
        m_name = input("Enter the name of the merged file: ")

        dr.file_name = m_name + ".csv"
        dr.record_csv(
            LED, n=n, time_1_or_samples_0=time_1_or_samples_0, samples=400, duration=3)

        # Move the merged file to the 'data_collection' folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.join(script_dir, "data_collection")

        csv_file_path = os.path.join(data_folder, f"{m_name}.csv")
        os.rename(m_name + ".csv", csv_file_path)

    else:
        print("Invalid choice. Exiting...")


if __name__ == "__main__":
    main()