from Modules import mkw_translations as translate
import calendar

class RKGFileHeader:
    """
    A class representing the header of an RKG.

    Attributes:
        file_id (str): "RKGD" in ASCII. File identifier.
        minutes (int): Minutes field of finishing time.
        seconds (int): Seconds field of finishing time.
        milliseconds (int): Milliseconds field of finishing time.
        track (int): Track ghost was set on.
        vehicle (str): Vehicle ghost used.
        character (str): Character ghost used.
        year (int): Year that the ghost was set, stored relative to the year 2000.
        month (int): Month that the ghost was set.
        day (int): Day that the ghost was set.
        controller (int): Controller ghost was set with.
        compressed (bool): Compressed flag
        ghost_type (str): Ghost type ghost is stored as.
        drift_type (str): Drift type ghost used.
        input_data_length (int): Length of input data when decompressed without padding.
        lap_count (int): Total laps ghost drove.
        lap_split_min (list): Minutes field for each of the 5 lap splits.
        lap_split_sec (list): Seconds field for each of the 5 lap splits.
        lap_split_ms (list): Milliseconds field for each of the 5 lap splits.
        country (str): Country ghost was set in, or 0xFF if sharing location disabled.
        state (int): Raw State code for Town/State/Province ghost was set in.
        location (int): Raw Location code for Location ghost was set in.
        mii_data (list): Raw Mii Data for Mii ghost was set with.
        mii_crc (int): CRC16-CCITT-Xmodem of Mii
    """
    
    file_id: str
    minutes: int
    seconds: int
    milliseconds: int
    track: str
    vehicle: str
    character: str
    year: int
    month: int
    day: int
    controller: str
    compressed: bool
    ghost_type: str
    drift_type: str
    input_data_length: int
    lap_count: int
    lap_split_min: list
    lap_split_sec: list
    lap_split_ms: list
    country: str
    state: int
    location: int
    mii_data: list
    mii_crc: int

    def __init__(self, raw: list):
        """
        Initialises the FileHeader object.
        """
        
        self.file_id = str(''.join([chr(i) for i in raw[0x00:0x03]]))
        self.minutes = raw[0x04] >> 1
        self.seconds = ((raw[0x04] & 0x01) << 6) + (raw[0x05] >> 2)
        self.milliseconds = ((raw[0x05] & 0x03) << 8) + raw[0x06]
        self.track = translate.course(raw[0x07] >> 2)
        self.vehicle = translate.vehicle(raw[0x08] >> 2)
        self.character = translate.character(
            (raw[0x08] & 0x03) << 4) + (raw[0x09] >> 4)
        self.year = ((raw[0x09] & 0x0F) << 3) + (raw[0x0A] >> 5)
        self.month = calendar.month_name[(raw[0x0A] & 0x1E) >> 1]
        self.day = ((raw[0x0A] & 0x01) << 4) + (raw[0x0B] >> 4)
        self.controller = translate.controller(raw[0x0B] & 0x0F)
        self.compressed = ((raw[0x0C] & 0x1000) >> 3) != 0
        self.ghost_type = translate.ghost_type(
            ((raw[0x0C] & 0x01) << 6) + (raw[0x0D] >> 2))
        self.drift_type = translate.drift_type((raw[0x0D] & 0x10) >> 1)
        self.input_data_length = (raw[0x0E] << 8) + raw[0x0F]
        self.lap_count = raw[0x10]
        self.read_lap_splits(raw)
        self.country = str(translate.country(raw[0x34]))
        self.state = raw[0x35]
        self.location = (raw[0x36] << 8) + raw[0x37]
        self.mii_data = raw[0x3C:0x85]
        self.mii_crc = (raw[0x86] << 8) + raw[0x87]

    def read_lap_splits(self, raw: list) -> list:
        """
        Reads Minutes, Seconds, and Milliseconds fields from raw lap splits
        and parses into lists.
        """

        for lap in range(5):
            offset = 0x11 + lap*0x03
            self.lap_split_min.append(raw[offset] >> 1)
            self.lap_split_sec.append(
                ((raw[offset] & 0x01) << 6) + (raw[offset+0x01] >> 2))
            self.lap_split_ms.append(
                ((raw[offset+0x01] & 0x03) << 8) + (raw[offset+0x02]))

class RKGInputDataHeader:
    """
    A class representing the header of the controller input data within the RKG.
    
    Attributes:
        face_button_inputs (int): Count of A, B/R, L button inputs in RKG.
        direction_inputs (int): Count of joystick inputs in RKG.
        trick_inputs (int): Count of D-pad inputs in RKG.
    """
    
    face_button_inputs: int
    direction_inputs: int
    trick_inputs: int

    def __init__(self, raw: list):
        """
        Initialises the InputDataHeader object.
        """
        
        offset = 0x88

        self.face_button_inputs = (raw[offset] << 8) + raw[offset+0x01]
        self.direction_inputs = (raw[offset+0x02] << 8) + raw[offset+0x03]
        self.trick_inputs = (raw[offset+0x04] << 8) + raw[offset+0x05]