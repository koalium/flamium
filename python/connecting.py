import serial.tools.list_ports
import time
import FreeSimpleGUI as sg
import threading

def popup_message(title, message):
    sg.popup(title, message)

def find_and_connect(window):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=115200, timeout=2)
            if wait_for_handshake(ser, keyword="height"):
                popup_message("Connection Successful", f"Connected to {ser.port}")
                time.sleep(1)  # Wait for 2 seconds before hiding the window
                #window.hide()
                return ser
            ser.close()
        except Exception as e:
            print(f"Error connecting to port {port.device}: {e}")
    window.write_event_value('NOT_FOUND', None)
    return None

def wait_for_handshake(ser, keyword="height"):
    start_time = time.time()
    while True:
        line = ser.readline().decode().strip()
        if keyword in line:
            return True
        if time.time() - start_time > 2:
            return False

def listen_and_parse(ser, window, log_window):
    while True:
        line = ser.readline().decode().strip()
        if line:
            key_value_pairs = [pair.split(':') for pair in line.split() if ':' in pair]
            for key, value in key_value_pairs:
                window['-OUTPUT-'].update(f"{key.strip()}: {value.strip()}\n", append=True)
                log_window['-LOG_OUTPUT-'].update(f"{key.strip()}: {value.strip()}\n", append=True)

def start_connection(window, log_window):
    ser = find_and_connect(window)
    if ser:
        window['-STATUS-'].update(f"Connected to {ser.port}")
        listen_and_parse(ser, window, log_window)
    else:
        window['-STATUS-'].update("Not connected")

def create_main_window():
    layout = [
        [sg.Text("Serial Port Connection Status: "), sg.Text("Not connected", key='-STATUS-')],
        [sg.Multiline(size=(50, 20), key='-OUTPUT-')],
        [sg.Button("Start"), sg.Button("Disconnect"), sg.Button("Exit")]
    ]

    layout_menu = [
        [sg.Button("Show Log", key='Show Log')]
    ]
    layout += layout_menu

    try:
        window = sg.Window("Serial Port Listener", layout, finalize=True)
    except Exception as e:
        print(f"Error creating window: {e}")
        popup_message("Error", "There was an error creating the window.")
        return None
    return window

def create_log_window():
    layout = [
        [sg.Text("Log Window")],
        [sg.Multiline(size=(50, 20), key='-LOG_OUTPUT-', disabled=True)]
    ]
    try:
        window = sg.Window("Log Window", layout, finalize=True)
    except Exception as e:
        print(f"Error creating window: {e}")
        popup_message("Error", "There was an error creating the window.")
        return None
    return window

def goto_cw():
    main_window = create_main_window()
    log_window = create_log_window()#.hide()

    if main_window and log_window:
        ser = None

        # Show log window for 2 seconds on startup
        log_window.un_hide()
        threading.Timer(22.0, log_window).start()

        # Run the connection process in a separate thread
        def run_connection():
            global ser
            ser = find_and_connect(main_window)
            if ser:
                main_window['-STATUS-'].update(f"Connected to {ser.port}")
                listen_and_parse(ser, main_window, log_window)
            else:
                main_window.write_event_value('NOT_FOUND', None)

        threading.Thread(target=run_connection, daemon=True).start()

        while True:
            event, values = main_window.read(timeout=100)
            if event == sg.WIN_CLOSED or event == "Exit":
                if ser:
                    ser.close()
                break
            elif event == "Start":
                threading.Thread(target=run_connection, daemon=True).start()
            elif event == "Disconnect":
                if ser:
                    ser.close()
                    ser = None
                    main_window['-STATUS-'].update("Disconnected")
            elif event == 'Show Log':
                log_window.un_hide()
                threading.Timer(2.0, log_window.hide).start()
            elif event == 'NOT_FOUND':
                popup_message("Error", "Serial port not found. Please connect your board.")

        main_window.close()
        log_window.close()

goto_cw()
