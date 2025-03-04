import serial
import time

# Configuration
PORT = 'COM7'
BAUD_RATE = 2000000  # 2 Mbps
TIMEOUT = 15  # 15 seconds timeout
START_MARKERS = [b'bihbih', bytes([5, 0])]  # Possible start markers
END_MARKERS = [b'migmig', bytes([0x00, 0xFF, 0x00, 0xFF, 0x00])]  # Possible end markers
FINISH_MARKER = b'finished!!!'  # Termination marker
RAW_DATA_FILE = 'data.dat'  # File to save all raw data
PRESSURE_FILE = 'pressure.txt'  # File to save processed pressure data
TIMER_FILE = 'timer.txt'  # File to save data after end marker until 'finished!!!'
DISTANCE = 1.33  # Distance between sensors in meters

# Function to receive and save all data
def receive_and_save_data():
    try:
        # Open the serial port
        ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {PORT} at {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return

    try:
        with open(RAW_DATA_FILE, 'wb') as file:
            print(f"Recording all data to {RAW_DATA_FILE}...")
            start_time = time.time()

            while True:
                # Read data from the serial port
                data = ser.read(ser.in_waiting or 1)

                if not data:
                    # No data received, check for timeout
                    if time.time() - start_time >= TIMEOUT:
                        print("Timeout reached. Stopping recording.")
                        break
                    continue

                # Write data to the file
                file.write(data)

                # Check for the finish marker
                if FINISH_MARKER in data:
                    print(f"Finish marker '{FINISH_MARKER.decode()}' detected. Stopping recording.")
                    break

    except IOError as e:
        print(f"Error writing to file: {e}")
    finally:
        # Close the serial port
        ser.close()
        print("Serial port closed.")

    print(f"All data saved to {RAW_DATA_FILE}.")

# Function to find a marker in the data
def find_marker(data, markers):
    for marker in markers:
        index = data.find(marker)
        if index != -1:
            return index, marker
    return -1, None

# Function to process the data
def process_data():
    try:
        with open(RAW_DATA_FILE, 'rb') as raw_file:
            raw_data = raw_file.read()

        # Find the start marker
        start_index, start_marker = find_marker(raw_data, START_MARKERS)
        if start_index == -1:
            print("Start marker not found in the data.")
            return

        # Find the end marker
        end_index, end_marker = find_marker(raw_data[start_index + len(start_marker):], END_MARKERS)
        if end_index == -1:
            print("End marker not found in the data.")
            return
        end_index += start_index + len(start_marker)  # Adjust end_index to the full raw_data

        # Find the finish marker
        finish_index = raw_data.find(FINISH_MARKER)
        if finish_index == -1:
            print("Finish marker not found in the data.")
            return

        # Extract data between start and end markers for pressure.txt
        extracted_pressure_data = raw_data[start_index + len(start_marker):end_index]

        # Convert each byte to its numeric value (0-255) and save to pressure.txt
        with open(PRESSURE_FILE, 'w') as pressure_file:
            for byte in extracted_pressure_data:
                pressure_file.write(f"{byte}\n")  # Write numeric value as text with newline

        print(f"Processed pressure data saved to {PRESSURE_FILE}.")

        # Extract data between end marker and finish marker for timer.txt
        extracted_timer_data = raw_data[end_index + len(end_marker):finish_index]

        # Save the extracted data to timer.txt
        with open(TIMER_FILE, 'wb') as timer_file:
            timer_file.write(extracted_timer_data)

        print(f"Timer data saved to {TIMER_FILE}.")

        # Process timer.txt to calculate speeds
        calculate_speeds()

    except IOError as e:
        print(f"Error reading or writing files: {e}")

# Function to calculate speeds from timer.txt
def calculate_speeds():
    try:
        with open(TIMER_FILE, 'r') as timer_file:
            timer_data = timer_file.read()

        # Extract time values for ir1, ir2, and ir5
        ir1_time = None
        ir2_time = None
        ir5_time = None

        for line in timer_data.splitlines():
            if line.startswith("ir1:"):
                ir1_time = int(line.split(":")[1].strip())  # Time in microseconds
            elif line.startswith("ir2:"):
                ir2_time = int(line.split(":")[1].strip())
            elif line.startswith("ir5:"):
                ir5_time = int(line.split(":")[1].strip())

        if ir1_time is None or ir2_time is None or ir5_time is None:
            print("Could not find all required time values in timer.txt.")
            return

        # Calculate time differences in seconds
        time_diff_ir1_ir2 = (ir2_time - ir1_time) / 1_000_000  # Convert microseconds to seconds
        time_diff_ir2_ir5 = (ir5_time - ir2_time) / 1_000_000

        # Calculate speeds
        speed_ir1_ir2 = DISTANCE / time_diff_ir1_ir2  # Speed in meters per second
        speed_ir2_ir5 = DISTANCE / time_diff_ir2_ir5

        # Print results
        print(f"Speed between ir1 and ir2: {speed_ir1_ir2:.2f} m/s")
        print(f"Speed between ir2 and ir5: {speed_ir2_ir5:.2f} m/s")

    except IOError as e:
        print(f"Error reading timer.txt: {e}")
    except ValueError as e:
        print(f"Error parsing time values: {e}")

# Main execution
if __name__ == "__main__":
    # Step 1: Receive and save all data
    receive_and_save_data()

    # Step 2: Process the data
    process_data()