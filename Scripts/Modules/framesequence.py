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


class FrameSequence:
    """
    A class representing a sequence of inputs, indexed by frames.

    Attributes:
        frames (list): The sequence of frames.
        filename (str): The name of the CSV file initializing the frame sequence.
    """
    frames: list
    filename: str

    # TODO: Make filename optional and allow for non-CSV frame sequences
    def __init__(self, filename: str):
        self.frames = []
        self.filename = filename

        self.refresh()

    def refresh(self) -> None:
        """
        Loads the CSV into a new frame sequence. Ideally called on savestate load.

        Args: None
        Returns: None
        """
        self.frames = []
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                frame = self.process(row)
                if not frame:
                    # TODO: Handle error
                    pass

                self.frames.append(frame)

    def process(self, raw_frame: List) -> Optional[Frame]:
        """
        Processes a raw frame into an instance of the Frame class. Ideally used internally.

        Args:
            raw_frame (List): Line from the CSV to process.

        Returns:
            A new Frame object initialized with the raw frame, or None if the frame is invalid.
        """
        if len(raw_frame) != 6:
            return None

        frame = Frame(raw_frame)
        if not frame.valid:
            return None

        return frame

    def get_gc_inputs(self, idx: int) -> Optional[dict]:
        """
        Gets the controller inputs for a given frame in the sequence. Compatible with Dolphin's "set_gc_buttons" method.

        Args:
            idx (int): The index for the sequence.

        Returns:
            The controller input dict for the provided frame, or None if the frame is not in the sequence.
        """
        if idx >= len(self.frames):
            return None

        frame = self.frames[idx]
        inputs = dict()

        inputs['A'] = frame.accel
        inputs['R'] = frame.brake
        inputs['L'] = frame.item

        raw_stick_inputs = [0, 60, 70, 80, 90, 100,
                            110, 128, 155, 165, 175, 185, 195, 200, 255]
        inputs['StickX'] = raw_stick_inputs[frame.stick_x + 7]
        inputs['StickY'] = raw_stick_inputs[frame.stick_y + 7]

        inputs['Up'] = frame.dpad_up
        inputs['Down'] = frame.dpad_down
        inputs['Left'] = frame.dpad_left
        inputs['Right'] = frame.dpad_right

        return inputs

    def get_wiimote_inputs(self, idx: int) -> Optional[dict]:
        """
        Gets the controller inputs for a given frame in the sequence. Compatible with Dolphin's "set_wii_buttons" method.

        Args:
            idx (int): The index for the sequence.

        Returns:
            The controller input dict for the provided frame, or None if the frame is not in the sequence.
        """
        if idx >= len(self.frames):
            return None

        frame = self.frames[idx]
        inputs = dict()

        inputs['A'] = frame.accel
        inputs['B'] = frame.brake

        return inputs

    def get_nunchuck_inputs(self, idx: int) -> Optional[dict]:
        """
        Gets the controller inputs for a given frame in the sequence. Compatible with Dolphin's "set_nunchuck_buttons" method.

        Args:
            idx (int): The index for the sequence.

        Returns:
            The controller input dict for the provided frame, or None if the frame is not in the sequence.
        """
        if idx >= len(self.frames):
            return None

        frame = self.frames[idx]
        inputs = dict()

        inputs['Z'] = frame.item

        raw_stick_inputs = [0, 60, 70, 80, 90, 100,
                            110, 128, 155, 165, 175, 185, 195, 200, 255]
        inputs['StickX'] = raw_stick_inputs[frame.stick_x + 7]
        inputs['StickY'] = raw_stick_inputs[frame.stick_y + 7]

        return inputs