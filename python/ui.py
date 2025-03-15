import serial
import FreeSimpleGUI as sg
import serial.tools.list_ports
import time
from string import *
import threading


sg.user_settings_filename(path='.')  # The settings file will be in the same folder as this program

def wait_for_handshake(ser, keywords=("height")):
    start_time = time.time()
    while True:
        line = ser.readline().decode().strip()
        for keyword in keywords:
            if keyword in line:
                return True
            if time.time() - start_time > 2:
                print(f"No handshake received within 2 seconds on port {ser.port}")
                sg.popup_quick_message(f"No handshake received within 2 seconds on port {ser.port}", text_color='darkgreen', background_color='orange', font='_ 18',)
                return False
            print(f"Received text: {line}")

def find_and_connect():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=115200, timeout=2)
            if wait_for_handshake(ser, keywords = ("height","handshake")):
                sg.popup_quick_message(f"Connection Successful: {ser.port}", text_color='white', background_color='red', font='_ 22',)
                return ser
            ser.close()
        except Exception as e:
            print(f"Error connecting to port {port.device}: {e}")
    sg.popup("Connection Fail","check your device connection:\nRESTART your board...??\nUNPLUG and plug your boar again...?!!\nTURN ON Caliper...??!\n...\nthen click on button : Reconnect !!!",text_color='magenta')
    return None



# Class holding the button graphic info. At this time only the state is kept
class BtnInfo:
    def __init__(self, state=True):
        self.state = state        # Can have 3 states - True, False, None (disabled)

def sanitize_input(data):
    return ''.join([str(c) for c in data if ord(c) < 128])

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_to_port(port):
    try:
        ser = serial.Serial(port, 115200, timeout=10)
        sg.popup("Success", f"Connected to {port}")
        return ser
    except serial.SerialException as e:
        sg.popup_error("Error", f"Failed to connect to {port}: {e}")

# Settings for you to modify are the size of the element, the circle width & color and the font for the % complete
bgcwin='black'
GRAPH_SIZE = (300 , 300)          # this one setting drives the other settings
CIRCLE_LINE_WIDTH, LINE_COLOR = 20, 'yellow'
TEXT_FONT = 'Tahoma'
TEXT_FONT_V='Serif'
TEXT_FONT_U='Arial'
# Computations based on your settings above
TEXT_HEIGHT = GRAPH_SIZE[0]//4
TEXT_LOCATION = (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//1.4)
TEXT_COLOR = LINE_COLOR
TEXT_COLOR_V = 'cyan' 
TEXT_LOCATION_V= (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//2.2)
TEXT_COLOR_U = 'light green'
TEXT_LOCATION_U= (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//5.2)

def update_meter(graph_elem, val=10.11,maxval=100.00,show=[10.11,100.00,'mm','height']):
    """
    Update a circular progress meter
    :param graph_elem:              The Graph element being drawn in
    :type graph_elem:               sg.Graph
    :param percent_complete:        Percentage to show complete from 0 to 100
    :type percent_complete:         float | int
    """
    graph_elem.erase()
    arc_length = show[0]/show[1]*360+.9
    if arc_length >= 360:
        arc_length = 359.9
        pass
    arc_COLOR = get_color(val,maxval)
    percent = show[0]/show[1]*100
    arcaddedlin=CIRCLE_LINE_WIDTH#+percent//5
    
    graph_elem.draw_arc((arcaddedlin, GRAPH_SIZE[1] - arcaddedlin), (GRAPH_SIZE[0] - arcaddedlin, arcaddedlin),
                   arc_length, 0, 'arc', arc_color=arc_COLOR, line_width=arcaddedlin)
    
    graph_elem.draw_text(f'%{percent:.0f}', TEXT_LOCATION_U, font=(TEXT_FONT, -TEXT_HEIGHT), color=TEXT_COLOR)
    graph_elem.draw_text(f'{show[0]/100:.2f}', TEXT_LOCATION_V, font=(TEXT_FONT_V, -TEXT_HEIGHT), color=TEXT_COLOR_V)
    graph_elem.draw_text(f'{show[2]}', TEXT_LOCATION, font=(TEXT_FONT_U, -TEXT_HEIGHT), color=TEXT_COLOR_U)
# Set up serial communication with the Arduino
#arduino = #serial.Serial('COM7', 115200)  # Replace 'COM7' with your Arduino's serial port

# Function to determine color based on value
def get_color(value, max_value):
    ratio = value / max_value
    if ratio>=1:
        return'blue'
    elif ratio>=0.95:
        return 'red'
    elif ratio >= 0.8:
        return 'purple'
    elif ratio >= 0.6:
        return 'orange'
    elif ratio >= 0.4:
        return 'yellow'
    elif ratio >= 0.2:
        return 'lightgreen'
    else:
        return 'green'
FLAMEARRESTOR_LINE_TYPE =['end of line','in line']
FLAMEARRESTOR_EXPLOSION_TYPE =['Detonation','Deflagration','Short Burning','Burning','endurance Burning']
SPEC_GAS_MIXTURE_GROUP=['IIA1','IIA','IIB1','IIB2','IIB3','IIB','IIC']
SPEC_GAS_MIXTURE=[['IIA1',['Methane',8.4]],['IIA',['Propane',4.2]],['IIB1',['Ethylene',5.2]],['IIB2',['Ethylene',5.7]],['IIB3',['Ethylene',6.6]],['IIB',['Hydrogen',45]],['IIC',['Hydrogen',28.5]]]


fmw=300
fmh=440
fth=120
ftw=150
crw=400
crh=fmh

gcrm=gclm=gctm=gcbm=gcm=8
gcph=gcpv=4
gch=fmh-fth-2*gcpv
gcw=fmw+gcph
def makewindowframe():
    col2 = sg.Column([[sg.Frame('Gas Mixture:', [[sg.Column([[sg.T("Explosive"),sg.Input(key='-EXPGASIN-', size=(5,2),justification='c')],[
                                                               sg.T('Oxydizer:'),sg.Input(key='-OXYGASIN-', size=(5,2),justification='c')],[sg.Button('Add', key='-MIXBTN-',size=(10,1),button_color=('yellow','olive'))],[sg.Button('Mixing', key='-MIXBTN-',size=(10,1),button_color=('yellow','olive'))]],justification='c',element_justification='r',size=(ftw,fth))]])],
                                                               [sg.G(canvas_size=(gcw-gclm-gcrm,gch-gctm-gcbm),graph_bottom_left=(gclm,gcbm),graph_top_right=(gcw-gcrm,gch-gctm),enable_events=True,background_color='gray',k='-GRAPH-',p=(gcpv,gcph))]],size=(fmw,fmh),pad=(0,0),element_justification='r',justification='c')
    crtbh=60
    col1 = sg.Column([
        # Categories sg.Frame
        [sg.Frame('Type:',[[ sg.Combo(SPEC_GAS_MIXTURE_GROUP,  key='-SPEC_GAS_MIXTURE-', size=(10,1)),
                                sg.Combo(FLAMEARRESTOR_EXPLOSION_TYPE,  key='-FLAMEARRESTOR_EXPLOSION_TYPE-', size=(18,1)),sg.Combo(FLAMEARRESTOR_LINE_TYPE,  key='-FLAMEARRESTOR_LINE_TYPE-', size=(11,1))]],s=(crw-15,crtbh))],
        # Information sg.Frame
        [sg.Frame('Sensors:', [[sg.Text('Flame Detectors:')],
                               [sg.Button('IR1',button_color=('yellow','blue')),sg.Button('IR2',button_color=('yellow','blue')),sg.Button('IR3',button_color=('yellow','blue')),sg.Button('IR4',button_color=('yellow','blue')),sg.Button('IR5',button_color=('yellow','blue')),sg.Button('IR6',button_color=('yellow','blue')),sg.Button('IR7',button_color=('yellow','blue')),sg.Button('IR8',button_color=('yellow','blue'))], 
                                [sg.Button('Alarm',button_color='yellow on green'),sg.Button('Spark',button_color=('yellow','purple')),sg.Button('Fire',button_color=('yellow','purple'))],
                               [sg.Text('Explosion Pressure:')],
                               [sg.Button('Piezo',button_color=('yellow','darkgreen'))],

                               [sg.Text('Gas Sensore:')],
                               [sg.Button('MQ',button_color=('yellow','darkblue')),sg.Button('BMP',button_color=('yellow','darkblue')),sg.Button('Pressure',button_color=('yellow','darkblue')),sg.Button('Temprature',button_color=('yellow','darkblue')),sg.Button('Ratio',button_color=('yellow','darkblue'))],
                               [sg.Text('Valves:')],
                               [sg.Button('Exp',button_color=('yellow','purple')),sg.Button('Oxy',button_color=('yellow','purple')),sg.Button('Tank',button_color=('yellow','purple'))],

                                [sg.Multiline(key='-NOTES-', size=(50,5))],
                               
                               
                                
                                ],s=(crw-15,crh-crtbh-15))] ],justification='c', pad=(2,2),s=(crw,crh))
    cfbw=crw+fmw
    fbh=105
    col3 = sg.Column([[sg.Frame('Actions:',
                                [[sg.Column([[ sg.Stretch(),sg.Button('Fire !!!',button_color=('black','orange'),font='Arial 18 bold',s=(5,3)),sg.I('pass',size=(10,1),justification='c'), sg.Button('STOP',button_color=('yellow','Red'),s=(5,3),font='Arial 18 bold')]],
                                           justification='r',element_justification='r',s=(cfbw-45,fbh), pad=(0,0))]])]],element_justification='r',justification='r',expand_y=True, pad=(0,0),s=(crw+fmw,fbh+45))
    theme_dict = {'BACKGROUND': '#2B475D',
                'TEXT': '#FFFFFF',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'BORDER': 0,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

    sg.theme_add_new('Dashboard', theme_dict)
    sg.theme('Dashboard')

    import random
    import psutil
    from threading import Thread


    STEP_SIZE = 3
    SAMPLES = 300
    SAMPLE_MAX = 500
    CANVAS_SIZE = (300, 200)


    g_interval = .25
    g_cpu_percent = 0
    g_procs = None
    g_exit = False


    def CPU_thread(args):
        global g_interval, g_cpu_percent, g_procs, g_exit

        while not g_exit:
            try:
                g_cpu_percent = psutil.cpu_percent(interval=g_interval)
                g_procs = psutil.process_iter()
            except:
                pass


    BORDER_COLOR = '#C7D5E0'
    DARK_HEADER_COLOR = '#1B2838'
    BPAD_TOP = ((20,20), (20, 10))
    BPAD_LEFT = ((20,10), (0, 0))
    BPAD_LEFT_INSIDE = (0, (10, 0))
    BPAD_RIGHT = ((10,20), (10, 0))
    # A perhaps better layout would have been to use the vtop layout helpful function.
    # This would allow the col2 column to have a different height and still be top aligned
    # layout = [sg.vtop([col1, col2]),
    #           [col3]]

    

    # The final layout is a simple one
    layout = [[col1, col2],
            [col3]]
    window = sg.Window('Columns and Frames', layout, finalize=True,  grab_anywhere=True)
    return window     



def reinterperetrecived(data='pressure:100',check='pressure'):
    cc=check.__add__(':')
    ccl = len(cc)
    dcl=len(data)
    ndata=data
    phfc = ndata.find(cc) 
    rec = 0.00
    if phfc >-1:
        nsdata=ndata[phfc:dcl]
        rec= float(data[phfc+ccl:dcl])
    return rec
def reciveddata(data=" "):
    cif=data.find('\r')
    cnf= data.find('\n')
    if cif>-1 :
        if cnf>-1:
            cif = min(cif,cnf)
    else:
        if cnf>-1:
            cif = cnf
        else:
            return



RUN_MODE=1
STOP_MODE=2
PAUSE_MODE=3
PUMP_MODE=4
DRAIN_MODE=5
IDLE_MODE=6
DONE_MODE=7
DUTYCYCLE_DEFAULT=55
global arduino
arduino = None#find_and_connect()   # type: ignore
def loopgui():
    start_time = time.time()
    btndis=True
    # Create a UserSettings object. The JSON file will be saved in the same folder as this .py file
    window_contents = sg.UserSettings(path='.', filename='mysettings.json')
    keys_to_save = ()
    #arduino = find_and_connect()   # type: ignore
    
    down = graphic_off = True    
    recpressure=1.02
    recheight=0.01
    max_pressure = 250
    max_caliper = 10000
    max_duty_cycle = 255
    bgc_motor_power='green'
    pshow=[recpressure,max_pressure,'Bar','pressure']
    hshow=[recheight,max_caliper,'mm','height']
    fpressure=max_pressure
    fheight=max_caliper
    recduty=DUTYCYCLE_DEFAULT
    fduty=DUTYCYCLE_DEFAULT
    data_to_send=[]
    mode = IDLE_MODE
    mode_prev = mode
    # Maximum values for scaling (change based on your sensor range)
    loopcounter=0
    height_start=0
    height_remain=fheight-height_start
    f=[]
    window = makewindowframe()
    # Run the connection process in a separate thread
    

    #threading.Thread(target=run_connection, daemon=True).start()
    p_graph = window["-GRAPH-"]
    

    
        

    # Show log window for 2 seconds on startup
    

    # Run the connection process in a separate thread
    started=0
    # Event loop to process user interactions
    while True:
        #event, values = window.read(timeout=5)
        event, values = window.read(timeout=5)
        loopcounter+=1
        
        if event is sg.WIN_CLOSED:
            break
        elif event =='Exit':
            sg.popup_quick_message('Saving settings & Exiting', text_color='white', background_color='red', font='_ 20')
            for key in keys_to_save:
                window_contents[key] = values[key]
            break
            
        if event == 'log on':
            f.append(1)
           
        elif event == 'no log':
            f.clear()
           
            
        elif event == 'PUMP':
            if arduino is not None:
                arduino.write(f'c{fduty}\n'.encode())
                arduino.write(f'P100\n'.encode())
                mode=PUMP_MODE
        elif event == 'STOP':
            if arduino is not None:
                arduino.write(f'S\n'.encode())
                mode=STOP_MODE
        elif event == 'DRAIN':
            if arduino is not None:
                arduino.write(f'D\n'.encode())
            mode=DRAIN_MODE
        elif event == 'PAUSE':
            if arduino is not None:
                arduino.write(f'S\n'.encode())
                mode=PAUSE_MODE
        elif event == 'fire':
            if arduino is not None:
                arduino.write(f'h{fheight}\n'.encode())
                arduino.write(f'c{fduty}\n'.encode())
                if mode_prev is not RUN_MODE:
                    height_start=recheight
                mode=RUN_MODE
        
        elif event == 'Reconnect':
            if arduino is not None:
                arduino.close()
            arduino = find_and_connect()  
        
        elif event == 'PUMPON':
            if arduino is not None:
                arduino.write(f'c{fduty}\n'.encode())
                arduino.write(f'P1500\n'.encode())
                mode=PUMP_MODE
        elif event == 'SaveSettings':
            filename = sg.popup_get_file('Save Settings', save_as=True, no_window=True)
            window.SaveToDisk(filename)
            # save(values)
        elif event == 'LoadSettings':
            filename = sg.popup_get_file('Load Settings', no_window=True)
            window.LoadFromDisk(filename)
            # load(form)
        
        if started==0:
            started=1
            ports = list_serial_ports()
            
            
            for key in keys_to_save:
                saved_value = window_contents[key]
                window[key].update(saved_value)
            arduino = find_and_connect()
        if arduino is None:
            continue    
        
        
        
        
        

        
        if arduino.in_waiting > 0:
            sanitized_data = read_sanitized_data(arduino=arduino).strip()
            nlc = min(sanitized_data.find('\n'),sanitized_data.find('\r'))
            while nlc>-1:
                nsdata = sanitized_data[0:nlc]
                
                phfc = nsdata.find("duty:") 
                if phfc >-1:
                    nsdata=nsdata[phfc:len(nsdata)]
                    recduty= int(nsdata[phfc+len("duty:"):len(nsdata)])/2.55
                    
                sanitized_data = sanitized_data[nlc+2:len(sanitized_data)]
                nlc = min(sanitized_data.find('\n'),sanitized_data.find('\r'))
            
        
         # Close the window and serial port
        if mode == RUN_MODE:
            #window['DUTY_SLIDER'].update(recduty)
            if fheight>recheight:
                arduino.write(b'R\n')    
            else:
                mode = DONE_MODE
                arduino.write(b'S\n') 
        elif mode == STOP_MODE:
            #arduino.write(b'S\n')  # Send 'S' command to Arduino
            pass
        elif mode == PUMP_MODE:
            if mode_prev is not PUMP_MODE:
                #arduino.write(b'P\n')  # Send 'P' command to Arduino
                pass

            
            
        elif mode == DRAIN_MODE:
            #arduino.write(b'D\n')  # Send 'D' command to Arduino
            pass
        elif mode == PAUSE_MODE:
            #arduino.write(b'S\n')  # Send 'S' command to Arduino
            pass
        elif mode == DONE_MODE:
            if mode_prev is RUN_MODE:
                arduino.write(b'S\n')  # Send 'S' command to Arduino
                sg.popup('Forming finished')
                mode = IDLE_MODE
                pass
        
        if values['-FLAMEARRESTOR_EXPLOSION_TYPE-'] is 'Detonation':
            if values['FLAMEARRESTOR_LINE_TYPE'] is'end of line':
                window['IR4'].update(visible=False)
                window['IR4'].update(visible=True)
                window['IR4'].update(visible=False)
            elif values['FLAMEARRESTOR_LINE_TYPE'] is'in line':
                pass
        elif values['-FLAMEARRESTOR_EXPLOSION_TYPE-'] is 'Deflagration':
            if values['FLAMEARRESTOR_LINE_TYPE'] is'end of line':
                pass
            elif values['FLAMEARRESTOR_LINE_TYPE'] is'in line':
                pass
        elif values['-FLAMEARRESTOR_EXPLOSION_TYPE-'] is 'Short Burning':
            if values['FLAMEARRESTOR_LINE_TYPE'] is'end of line':
                pass
            elif values['FLAMEARRESTOR_LINE_TYPE'] is'in line':
                pass
            
        elif values['-FLAMEARRESTOR_EXPLOSION_TYPE-'] is 'Burning':
            if values['FLAMEARRESTOR_LINE_TYPE'] is'end of line':
                pass
            elif values['FLAMEARRESTOR_LINE_TYPE'] is'in line':
                pass
        elif values['-FLAMEARRESTOR_EXPLOSION_TYPE-'] is 'endurance Burning':
            if values['FLAMEARRESTOR_LINE_TYPE'] is'end of line':
                pass
            elif values['FLAMEARRESTOR_LINE_TYPE'] is'in line':
                pass

        mode_prev = mode
    if arduino is not None:
        arduino.write(b'S\n') 
        arduino.close()
    
    window.close()
    


def is_ascii_byte(byte):
    return 0 <= byte < 128
# Function to read and sanitize data from Arduino
def read_sanitized_data(arduino):
    data = bytearray()
    while arduino.in_waiting > 0:
        byte = arduino.read()
        if is_ascii_byte(byte[0]):
            data.append(byte[0])
    return data.decode('utf-8')# Function to read and sanitize data from Arduino


def main():
    loopgui()
    
if __name__ == '__main__':
    main()
