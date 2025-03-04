


import ui

def main():
    ui.main()

if __name__ == '__main__':
    main()


import PySimpleGUI as sg

menu_def = [['File', ['New', 'Exit']],
            ['Settings', ['Select Serial Port', 'log on', 'log off']]]
sg.theme('black')

GRAPH_SIZE = (400, 400)
bgcwin = 'black'

layout_progress_graph = [
    sg.Graph(GRAPH_SIZE, (0, 0), GRAPH_SIZE, key='-GRAPHH-', background_color=bgcwin),
    sg.Graph(GRAPH_SIZE, (0, 0), GRAPH_SIZE, key='-GRAPHP-', background_color=bgcwin)
]

col_1 = sg.Column([
    sg.Frame("Control Inputs", [
        [sg.Button('Reconnect')],
        [sg.Text("Final Height:"), sg.Stretch(),
         sg.InputText("101.31", justification='center', key="final_height", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="height_dependency", default=True, enable_events=True)],
        [sg.Text("Final Pressure:"), sg.Stretch(),
         sg.InputText("105.2", justification='center', disabled=True, key="final_pressure", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="pressure_dependency", disabled=True)],
        [sg.Text("Size:"), sg.Stretch(),
         sg.InputText("4", justification='center', key="-SIZE-", size=(8, 1), enable_events=True),
         sg.Radio("", "DEPENDENCY", key="radiosize", disabled=False)]
    ], border_width=2, element_justification='stretch'),
    sg.Frame('Motor Power', [
        [sg.Text('11', key='-MOTOR_VAL-', size=(10, 10), expand_y=True, font=('Tahoma', 48, 'bold'), justification='center', pad=(0, 40), background_color=bgcwin)]
    ], size=(200, 200), background_color=bgcwin, key='MOTOR_FRAME', element_justification='center', border_width=5, relief='raised'),
], element_justification='center')

col_2 = sg.Column([
    [sg.Slider(range=(0, 100), orientation='v', font=('Helvetica 20'), size=(12, 15), key='DUTY_SLIDER', change_submits=True, enable_events=True)],
], element_justification='center')

layout_control = [
    [sg.Button('Drain', key='DRAIN', button_color=('yellow', 'magenta'), size=(10, 2), disabled=True),
     sg.Button('Pause', key='PAUSE', button_color=('brown', 'orange'), size=(10, 2), disabled=True, enable_events=True, change_submits=True),
     sg.Button('+', key='PUMP', button_color=('yellow', 'blue'), size=(10, 2), disabled=True)],
    [sg.Button('Stop', key='STOP', button_color=('yellow', 'red'), size=(10, 2), disabled=True),
     sg.Button('Run', key='RUN', button_color=('yellow', 'green'), size=(10, 2), disabled=True)],
    [sg.Button('Pump ON', key='PUMPON', button_color=('olive', 'blue'), size=(10, 2), disabled=True)]
]

log_layout = [
    [sg.Multiline(size=(50, 20), key='-OUTPUT-', visible=False)]
]

layout = [[sg.Menu(menu_def, tearoff=False)],
          layout_progress_graph,
          [sg.HorizontalSeparator()],
          col_1,
          [sg.HorizontalSeparator()],
          layout_control,
          [sg.HorizontalSeparator()],
          log_layout]

scrollable_layout = [[sg.Column(layout, scrollable=True, vertical_scroll_only=True, size=(600, 800), key='-SCROLLABLE-', background_color=bgcwin)]]

# Create the window
window = sg.Window('Arduino Sensor Values and Control', scrollable_layout, finalize=True, element_justification='center',
                   location=(100, 100), background_color=bgcwin, size=(600, 800), resizable=True, sbar_frame_color='gray')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
