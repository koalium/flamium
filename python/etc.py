import serial
import serial.tools.list_ports
import PySimpleGUI as sg

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_to_port(port):
    try:
        ser = serial.Serial(port, 9600, timeout=1)
        sg.popup("Success", f"Connected to {port}")
        ser.close()
    except serial.SerialException as e:
        sg.popup_error("Error", f"Failed to connect to {port}: {e}")

ports = list_serial_ports()

menu_def = [['File', ['Exit']],
            ['Settings', ['Select Serial Port']]]

layout = [
    [sg.Menu(menu_def, tearoff=False)],
    [sg.Text('Select a serial port:')],
    [sg.Combo(ports, key='-PORT-', size=(20, 1))],
    [sg.Button('Connect')]
]

window = sg.Window('Serial Port Selector', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Select Serial Port':
        ports = list_serial_ports()
        window['-PORT-'].update(values=ports)
    elif event == 'Connect':
        selected_port = values['-PORT-']
        if selected_port:
            connect_to_port(selected_port)
        else:
            sg.popup_error("Error", "Please select a port")

window.close()
