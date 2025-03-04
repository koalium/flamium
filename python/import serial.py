import serial
import FreeSimpleGUI as sg
import serial.tools.list_ports

def is_ascii_byte(byte):
    return 0 <= byte < 128

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def get_color(value, threshold, min_val=0, max_val=100):
    if value >= threshold:
        return '#ff0000'  # Red color for threshold and above
    # Normalize the value within the given range
    norm_value = (value - min_val) / (max_val - min_val)
    # Interpolate color from green to red
    red = int(norm_value * 255)
    green = int((1 - norm_value) * 255)
    return f'#{red:02x}{green:02x}00'

# Define the layout of the GUI window with frames for each segment
layout = [
    [sg.Frame("Monitoring", [
        [sg.Graph(canvas_size=(200, 200), graph_bottom_left=(0, 0), graph_top_right=(200, 200), key="pressure_square", background_color='white'), 
         sg.Graph(canvas_size=(200, 200), graph_bottom_left=(0, 0), graph_top_right=(200, 200), key="height_square", background_color='white')]
    ], border_width=2)],
    
    [sg.Frame("Serial Connection", [
        [sg.Text("Select Serial Port:")],
        [sg.Combo(list_serial_ports(), key="serial_port", readonly=True), sg.Button("Connect")]
    ], border_width=2)],
    
    [sg.Frame("Sensor Data", [
        [sg.Text("Pressure:"), sg.Text("", size=(10, 1), key="pressure_val")],
        [sg.Text("Height:"), sg.Text("", size=(10, 1), key="height_val")],
        [sg.Text("Mood:"), sg.Text("", size=(10, 1), key="mood_val")],
        [sg.Text("Duty Cycle:"), sg.Text("", size=(10, 1), key="dutycycle_val")]
    ], border_width=2)],
    
    [sg.Frame("Control Inputs", [
        [sg.Text("Final Height:"), sg.InputText("", key="final_height", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="height_dependency"),
        sg.Text("Final Pressure:"), sg.InputText("", key="final_pressure", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="pressure_dependency")]
    ], border_width=2)],
    
    
    [sg.Frame("Commands", [
        [sg.Button("+"), sg.Button("Run"), sg.Button("Drain"), sg.Button("Stop"), sg.Button("Pause"), sg.Button("Exit")]
    ], border_width=2)],
    
    [sg.Frame("Log", [
        [sg.Multiline(size=(60, 10), key="log", disabled=True)]
    ], border_width=2)]
]

# Create the GUI window
window = sg.Window("Arduino Data", layout, finalize=True)

# Function to read and sanitize data from Arduino
def read_sanitized_data(arduino):
    data = bytearray()
    while arduino.in_waiting > 0:
        byte = arduino.read()
        if is_ascii_byte(byte[0]):
            data.append(byte[0])
    return data.decode('utf-8')

arduino = None
pressure_threshold = 150  # Define threshold value for pressure
height_threshold = 1500  # Define threshold value for height

while True:
    event, values = window.read(timeout=100)
    
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    
    # Connect to the selected serial port
    if event == "Connect":
        selected_port = values["serial_port"]
        if selected_port:
            arduino = serial.Serial(selected_port, 115200)
            window['log'].print(f"Connected to {selected_port}")
    
    if arduino:
        # Send "pump" command to Arduino when "+" button is pressed
        if event == "+":
            arduino.write(b"pump\n")
            window['log'].print("Sent: pump")
        
        # Send "run", "duty", "fheight", and "fpressure" commands to Arduino when "Run" button is pressed
        if event == "Run":
            final_height = values["final_height"]
            final_pressure = values["final_pressure"]
            arduino.write(b"run\n")
            arduino.write(b"duty\n")
            arduino.write(f"fheight:{final_height}\n".encode('utf-8'))
            arduino.write(f"fpressure:{final_pressure}\n".encode('utf-8'))
            window['log'].print(f"Sent: run, duty, fheight:{final_height}, fpressure:{final_pressure}")
        
        # Send "drain" command to Arduino when "Drain" button is pressed
        if event == "Drain":
            arduino.write(b"drain\n")
            window['log'].print("Sent: drain")

        # Send "stop" command to Arduino when "Stop" button is pressed
        if event == "Stop":
            arduino.write(b"stop\n")
            window['log'].print("Sent: stop")

        # Send "pause" command to Arduino when "Pause" button is pressed
        if event == "Pause":
            arduino.write(b"pause\n")
            window['log'].print("Sent: pause")
        
        # Read and sanitize data from Arduino
        if arduino.in_waiting > 0:
            sanitized_data = read_sanitized_data(arduino).strip()
            
            if sanitized_data:
                # Ensure the data is not too much or null
                if '\n' in sanitized_data:
                    sanitized_data = sanitized_data[0:sanitized_data.find('\n')]
                if ':' in sanitized_data:
                    data_type, value = sanitized_data.split(":", 1)
                    
                    # Update the appropriate display field
                    if data_type == "pressure":
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                        window['pressure_val'].update(value)
                        color = get_color(value, pressure_threshold)
                        pressure_graph = window["pressure_square"]
                        pressure_graph.DrawRectangle((0, 0), (200, 200), fill_color=color, line_color='red')
                        pressure_graph.draw_text(str(value), (100, 100), color='black', font=('Helvetica', 24, 'bold'))
                    elif data_type == "height":
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                        window['height_val'].update(value)
                        height_graph = window["height_square"]
                        # color = get_color(value, height_threshold)
                        height_graph.DrawRectangle((0, 0), (200, 200), fill_color='green', line_color='magenta')
                        height_graph.draw_text(str(value), (100, 100), color='black', font=('Helvetica', 32, 'bold'))
                    elif data_type == "mood":
                        pass
                    elif data_type == "dutycycle":
                        pass
                    
                    # Log the received data
                    window['log'].print(f"Received: {data_type}:{value}")

# Close the window and the serial connection
if arduino:
    arduino.close()
window.close()
