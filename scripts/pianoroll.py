from dolphin import controller, event, gui, memory
import csv

# setting some static values
base_inputs = {'Left': False, 'Right': False, 'Down': False, 'Up': False, 'Z': False, 'R': False, 'L': False, 'A': True, 'B': False, 'X': False, 'Y': False, 'Start': False, 'StickX': 128, 'StickY': 128, 'CStickX': 128, 'CStickY': 128, 'TriggerLeft': 0, 'TriggerRight': 0, 'AnalogA': 0, 'AnalogB': 0, 'Connected': True}
stick_dict = {-7: 0, -6: 60, -5: 70, -4: 80, -3: 90, -2: 100, -1: 110, 0: 128, 1: 155, 2: 165, 3: 175, 4: 185, 5: 195, 6: 200, 7: 255}
dpad_map = {0: (False, False, False, False), 1: (True, False, False, False), 2: (False, True, False, False), 3: (False, False, True, False), 4: (False, False, False, True) }

def load_pianoroll(filepath: str) -> dict:
    # Loads the entire CSV as a dictionary formatted like so: [row number]:[row contents]
    pianoroll = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            pianoroll[str(i+1)] = [int(val) for val in row]
    return pianoroll

def read_pianoroll(pianoroll: list, row):
    # Reads the given row from the pianoroll
    return pianoroll.get(str(row))

def write_pianoroll(pianoroll: list, row: int, data: list):
    # Replaces the given row in the painoroll
    pianoroll[str(row)] = data

def decode_pianoroll(row: list) -> list:
    #If the row is empty then return imnmediately with a special value str('no inputs')
    #This can be detected by the input sender and it will know not to do anything
    if not row:
        return str('no inputs')

    #Ensure there are exactly 6 integers in our list + warn if bad data detected
    if len(row) != 6 or not all(isinstance(x, int) for x in row):
        add_osd_message(str(f'BAD DATA DETECTED ON FRAME {race_frame}!'), int(2000), int(0xFFFFFF30))
        row = [int(x) if isinstance(x, (int)) else 0 for x in row]
        row = row[:6]
        row += [0] * (6 - len(row))

    #Clamp stick and dpad + warn if illegal input detected
    if not (-7 <= row[3] <= 7) or not (-7 <= row[4] <= 7) or not (0 <= row[5] <= 4): 
        add_osd_message(str(f'ILLEGAL INPUT DETECTED ON FRAME {race_frame}!'), int(2000), int(0xFFFFFF30))
        row[3] = max(-7, min(7, row[3]))
        row[4] = max(-7, min(7, row[4]))
        row[5] = max(0, min(4, row[5]))
    
    # A,B,L are bools
    row[0] = bool(row[0])
    row[1] = bool(row[1])
    row[2] = bool(row[2])

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




# Run on script start
race_frame = memory.read_u32(0x809BF0B8) #hardcoded for NTSCU
last_race_frame = race_frame -1
pianoroll_path = r'' #you have to do this because windows filepaths are cursed
pianoroll = load_pianoroll(pianoroll_path)

## draw information to the screen
colour = 0xffffff00
while True:
    await event.frameadvance()
    race_frame = memory.read_u32(0x809BF0B8) #hardcoded for NTSCU
    if last_race_frame +1 != race_frame:
        pianoroll = load_pianoroll(pianoroll_path)
    row_data = read_pianoroll(pianoroll, race_frame) # read from the row associated with this race frame
    controller_state = decode_pianoroll(row_data) #turn the pianoroll into a set of inputs
    if controller_state != 'no inputs': #If there are inputs on this frame, send the inputs
        controller.set_gc_buttons(0, controller_state)
    gui.draw_text((10, 10) , colour, f"Frame: {race_frame}\ntable row: {row_data}\nDecoded Inputs:{controller_state}")
    last_race_frame = race_frame
