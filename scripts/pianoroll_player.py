from dolphin import controller, event, gui, memory
import csv
import mkw_core as core
import mkw_translations as translate

# setting some static values
base_inputs = {'Left': False, 'Right': False, 'Down': False, 'Up': False, 'Z': False, 'R': False, 'L': False, 'A': True, 'B': False, 'X': False, 'Y': False, 'Start': False, 'StickX': 128, 'StickY': 128, 'CStickX': 128, 'CStickY': 128, 'TriggerLeft': 0, 'TriggerRight': 0, 'AnalogA': 0, 'AnalogB': 0, 'Connected': True}
stick_dict = {-7: 0, -6: 60, -5: 70, -4: 80, -3: 90, -2: 100, -1: 110, 0: 128, 1: 155, 2: 165, 3: 175, 4: 185, 5: 195, 6: 200, 7: 255}
dpad_map = {0: (False, False, False, False), 1: (True, False, False, False), 2: (False, True, False, False), 3: (False, False, True, False), 4: (False, False, False, True) }
    
def load_pianoroll(filepath: str) -> list:
    # Loads the entire CSV as list of lists like so: [row number][row contents]
    pianoroll = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            pianoroll.append([int(val) for val in row])
    return pianoroll

def decode_pianoroll(row: list) -> list:
    #If the row is empty then return imnmediately with a special value str('no inputs')
    #This can be detected by the input sender and it will know not to do anything
    if not row:
        return str('no inputs')

    #Ensure there are exactly 6 integers in our list + warn if bad data detected
    if len(row) != 6 or not all(isinstance(x, int) for x in row):
        gui.add_osd_message(str(f'BAD DATA DETECTED ON FRAME {race_frame}!'), int(2000), int(0xFFFFFF30))
        row = [int(x) if isinstance(x, (int)) else 0 for x in row]
        row = row[:6]
        row += [0] * (6 - len(row))

    #Clamp stick and dpad + warn if illegal input detected
    if not (-7 <= row[3] <= 7) or not (-7 <= row[4] <= 7) or not (0 <= row[5] <= 4): 
        gui.add_osd_message(str(f'ILLEGAL INPUT DETECTED ON FRAME {race_frame}!'), int(2000), int(0xFFFFFF30))
        row[3] = max(-7, min(7, row[3]))
        row[4] = max(-7, min(7, row[4]))
        row[5] = max(0, min(4, row[5]))
    
    # A,B,L are bools
    row[0:2] = [bool(x) for x in row[0:2]]

    # Assign StickX and StickY to their corresponding real stick value
    row[3] = stick_dict.get(row[3], 0)
    row[4] = stick_dict.get(row[4], 0)
    
    # Assign Dpad to 4 different bools (UDLR)
    row[5:9] = dpad_map.get(row[5], (False, False, False, False))

    # Turn the data into a controller state
    inputs = base_inputs.copy()
    inputs['A'] = row[0]
    inputs['R'] = row[1]
    inputs['L'] = row[2]
    inputs['StickX'] = row[3]
    inputs['StickY'] = row[4]
    inputs['Up'] = row[5]
    inputs['Down'] = row[6]
    inputs['Left'] = row[7]
    inputs['Right'] = row[8]

    return inputs

def onFrameAdvance():
    race_frame = core.get_frame_of_input()
    global pianoroll, last_race_frame
    if 0 < race_frame == last_race_frame:
        race_frame += 1
    if last_race_frame > race_frame:
        pianoroll = load_pianoroll(pianoroll_path)
    row_data = pianoroll[race_frame].copy() # read from the row associated with this race frame
    controller_state = decode_pianoroll(row_data) #turn the pianoroll into a set of inputs
    if controller_state != 'no inputs': #If there are inputs on this frame, send the inputs
        controller.set_gc_buttons(0, controller_state)
    last_race_frame = race_frame

def onSavestateLoad(isSlot, slot):
    if (isSlot):
        onFrameAdvance()
        
if __name__ == '__main__':
    # Run on script start
    colour = 0xffffff00
    race_frame = core.get_frame_of_input()
    last_race_frame = race_frame - 1
    pianoroll_path = r'filepath'
    pianoroll = load_pianoroll(pianoroll_path)
    gui.add_osd_message(f"{pianoroll_path} successfully loaded!")
    
    event.on_frameadvance(onFrameAdvance)
    event.on_savestateload(onSavestateLoad)
