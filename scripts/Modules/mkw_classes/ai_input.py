from . import InputMgr

class AiInput:
    class AiController:
        def __init__(self, kart_idx=0, addr=None):
            self.addr = addr if addr else AiInput.AiController.chain(kart_idx)

            self.controller = self.inst_controller
            self.race_input_state = self.inst_race_input_state

        @staticmethod
        def chain(kart_idx=0) -> int:
            return AiInput.ai_controller(kart_idx)
        
        @staticmethod
        def controller(kart_idx=0) -> int:
            ai_controller_ref = AiInput.AiController.chain(kart_idx)
            controller_ref = ai_controller_ref + 0x0
            return controller_ref
        
        def inst_controller(self) -> int:
            controller_ref = self.addr + 0x0
            return controller_ref
        
        @staticmethod
        def race_input_state(kart_idx=0) -> int:
            ai_controller_ref = AiInput.AiController.chain(kart_idx)
            race_input_state_ref = ai_controller_ref + 0x90
            return race_input_state_ref
        
        def inst_race_input_state(self) -> int:
            race_input_state_ref = self.addr + 0x90
            return race_input_state_ref
    
    def __init__(self, kart_idx=0, addr=None):
        assert(0 <= kart_idx < 12)
        self.addr = addr if addr else AiInput.chain(kart_idx)

        self.kart_input = self.inst_kart_input
        self.ai_controller = self.inst_ai_controller

    @staticmethod
    def chain(kart_idx=0) -> int:
        return InputMgr.ai_kart_input(kart_idx)

    @staticmethod
    def kart_input(kart_idx=0) -> int:
        ai_input_ref = AiInput.chain(kart_idx)
        kart_input_ref = ai_input_ref + 0x0
        return kart_input_ref
    
    def inst_kart_input(self) -> int:
        kart_input_ref = self.addr + 0x0
        return kart_input_ref
    
    @staticmethod
    def ai_controller(kart_idx=0) -> int:
        ai_input_ref = AiInput.chain(kart_idx)
        ai_controller_ref = ai_input_ref + 0xD8
        return ai_controller_ref
    
    def inst_ai_controller(self) -> int:
        ai_controller_ref = self.addr + 0xD8
        return ai_controller_ref