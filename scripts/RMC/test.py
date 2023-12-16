from dolphin import event, gui, utils

def main():
    global counter
    counter = 0

if __name__ == '__main__':
    main()





"""    
@event.on_savestateload
def on_state_load(fromSlot: bool, slot: int):
"""

@event.on_frameadvance
def on_frame_advance():
    global counter
    counter +=1
    print(counter)
    

