from dolphin import memory

from . import Controller, InputMgr

class GhostController(Controller):
    """This can be accessed either via InputMgr->ghostControllers,
       or via RaceManager->RaceManagerPlayer->KartInput->raceController
       if you know that the playerIdx represents the ghost. These two paths
       are guaranteed to refer to the same addr."""
    def __init__(self, addr):
        # Make sure this actually IS a ghost controller
        input_mgr_ref = InputMgr.chain()
        ghost_controller_arr = input_mgr_ref + 0x3E60
        controller_list = [ghost_controller_arr + (idx * 0xA8) for idx in range(0, 4)]
        assert(addr in controller_list)
        self.addr = addr

    def buttons_stream(self, stream_idx=0):
        """stream_idx: 0 -> Face buttons, 1 -> DI, 2 -> Trick"""
        assert(0 <= stream_idx < 3)
        buttons_stream_ptr = self.addr + 0x94 + (stream_idx * 0x4)
        return memory.read_u32(buttons_stream_ptr)
