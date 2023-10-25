from typing import List, Optional
import csv


class Frame:
    """
    A class representing an input combination on a frame.

    Attributes:
        accel (bool): Whether or not we press 'A' on that frame.
        brake (bool): Whether or not we press 'B' on that frame.
        item (bool): Whether or not we press 'L' on that frame.
        stick_x (int): Horizontal stick input, ranging from -7 to +7.
        stick_y (int): Vertical stick input, ranging from -7 to +7.
        dpad_up (bool): Whether or not we press 'Up' on that frame.
        dpad_down (bool): Whether or not we press 'Down' on that frame.
        dpad_left (bool): Whether or not we press 'Left' on that frame.
        dpad_right (bool): Whether or not we press 'Right' on that frame.
        valid (bool): Whether or not the Frame is valid.
        iter_idx (int): Tracks current iteration across the inputs
    """
    accel: bool
    brake: bool
    item: bool

    stick_x: int
    stick_y: int

    dpad_up: bool
    dpad_down: bool
    dpad_left: bool
    dpad_right: bool

    valid: bool
    
    iter_idx: int

    def __init__(self, raw: List):
        """
        Initializes a Frame object given a CSV line.

        The structure of the list is as follows:
            * raw[0] (str) - A
            * raw[1] (str) - B/R
            * raw[2] (str) - L
            * raw[3] (str) - Horizontal stick
            * raw[4] (str) - Vertical stick
            * raw[5] (str) - Dpad

        Args:
            raw (List): CSV line to be read
        """
        self.valid = True

        self.accel = self.read_button(raw[0])
        self.brake = self.read_button(raw[1])
        self.item = self.read_button(raw[2])
        self.stick_x = self.read_stick(raw[3])
        self.stick_y = self.read_stick(raw[4])
        self.read_dpad(raw[5])
    
    def __iter__(self):
        self.iter_idx = 0
        return self
    
    def __next__(self):
        # If we update to Python 3.10, replace with switch statement
        self.iter_idx += 1
        if (self.iter_idx == 1):
            return int(self.accel)
        if (self.iter_idx == 2):
            return int(self.brake)
        if (self.iter_idx == 3):
            return int(self.item)
        if (self.iter_idx == 4):
            return self.stick_x
        if (self.iter_idx == 5):
            return self.stick_y
        if (self.iter_idx == 6):
            return self.dpad_raw()
        raise StopIteration

    def read_button(self, button: str) -> bool:
        """
        Parses the button input into a boolean. Sets `self.valid` to False if invalid.
        """
        try:
            val = int(button)
        except ValueError:
            self.valid = False
            return False

        if val < 0 or val > 1:
            self.valid = False

        return bool(val)

    def read_stick(self, stick: str) -> int:
        """
        Parses the stick input into an int. Sets `self.valid` to False if invalid.
        """
        try:
            val = int(stick)
        except ValueError:
            self.valid = False
            return 0

        if val < -7 or val > 7:
            self.valid = False

        return val

    def read_dpad(self, dpad: str) -> None:
        """
        Sets dpad members based on dpad input. Sets `self.valid` to False if invalid.
        """
        try:
            val = int(dpad)
        except ValueError:
            self.valid = False
            return

        if val < 0 or val > 4:
            self.valid = False

        self.dpad_up = val == 1
        self.dpad_down = val == 2
        self.dpad_left = val == 3
        self.dpad_right = val == 4
        
    def dpad_raw(self) -> int:
        """
        Converts dpad values back into its raw form, for writing to the csv
        """
        if self.dpad_up:
            return 1
        if self.dpad_down:
            return 2
        if self.dpad_left:
            return 3
        if self.dpad_right:
            return 4
        return 0


class FrameSequence:
    """
    A class representing a sequence of inputs, indexed by frames.

    Attributes:
        frames (list): The sequence of frames.
        filename (str): The name of the CSV file initializing the frame sequence.
    """
    frames: list
    filename: str
    iter_idx: int

    def __init__(self, filename: Optional[str]=None):
        self.frames = []
        self.filename = filename

        if self.filename:
            self.read_from_file()
    
    def __len__(self):
        return len(self.frames)
        
    def __getitem__(self, i):
        if (i < len(self.frames)):
            return self.frames[i]
        return None
        
    def __iter__(self):
        self.iter_idx = -1
        return self
        
    def __next__(self):
        self.iter_idx += 1
        if (self.iter_idx < len(self.frames)):
            return self.frames[self.iter_idx]
        raise StopIteration
        
    def read_from_list(self, inputs: List) -> None:
        """
        Constructs the frames list by using a list instead of a csv
        
        Args:
            input (List): The raw input data we want to store
        Returns: None
        """
        for input in inputs:
            frame = self.process(input)
            if not frame:
                pass
            self.frames.append(frame)
    
    def read_from_file(self) -> None:
        """
        Loads the CSV into a new frame sequence. Ideally called on savestate load.

        Args: None
        Returns: None
        """
        self.frames.clear()
        try:
            with open(self.filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    frame = self.process(row)
                    if not frame:
                        # TODO: Handle error
                        pass

                    self.frames.append(frame)
        except IOError:
            return
                
    def write_to_file(self, filename: str) -> bool:
        """
        Writes the frame sequence to a csv
        
        Args:
            filename (str): The path to the file we wish to write to
        Returns:
            A boolean indicating whether the write was successful
        """
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerows(self.frames)
        except IOError:
            return False
        return True

    def process(self, raw_frame: List) -> Optional[Frame]:
        """
        Processes a raw frame into an instance of
        the Frame class. Ideally used internally.

        Args:
            raw_frame (List): Line from the CSV to process.

        Returns:
            A new Frame object initialized with the raw frame,
            or None if the frame is invalid.
        """
        if len(raw_frame) != 6:
            return None

        frame = Frame(raw_frame)
        if not frame.valid:
            return None

        return frame
