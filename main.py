import data_read.data_read as dr
import os


def main():
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
            dr.record_csv(1)
            input("Recording number " + str(i + 1) +
                  " done. Press enter to continue.")

        for i in range(int(n)):
            # Read the data from the individual files as a individual list [x1, x2, x3, ...]
            with open(m_name + str(i + 1) + ".csv", "r") as f:
                data = f.read().split(",")

            # Create or open csv file named m_name + ".csv"
            with open(m_name + ".csv", "a") as f:
                f.write(",".join(data))

        # Delete the individual data files
        for i in range(int(n)):
            os.remove(m_name + str(i + 1) + ".csv")

    elif choice == "2":
        n = int(input("How many recordings? "))
        m_name = input("Enter the name of the merged file: ")

        dr.file_name = m_name + ".csv"
        dr.record_csv(n)

    else:
        print("Invalid choice. Exiting...")


if __name__ == "__main__":
    main()
