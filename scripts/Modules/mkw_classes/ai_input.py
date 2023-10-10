from . import InputMgr

class AiInput:
    class AiController:
        def __init__(self, kartIdx=0, addr=None):
            self.addr = addr if addr else AiInput.AiController.chain(kartIdx)

            self.controller = self.inst_controller
            self.race_input_state = self.inst_race_input_state

        @staticmethod
        def chain(kartIdx=0) -> int:
            return AiInput.ai_controller(kartIdx)
        
        @staticmethod
        def controller(kartIdx=0) -> int:
            ai_controller_ref = AiInput.AiController.chain(kartIdx)
            controller_ref = ai_controller_ref + 0x0
            return controller_ref
        
        def inst_controller(self) -> int:
            controller_ref = self.addr + 0x0
            return controller_ref
        
        @staticmethod
        def race_input_state(kartIdx=0) -> int:
            ai_controller_ref = AiInput.AiController.chain(kartIdx)
            race_input_state_ref = ai_controller_ref + 0x90
            return race_input_state_ref
        
        def inst_race_input_state(self) -> int:
            race_input_state_ref = self.addr + 0x90
            return race_input_state_ref
    
    def __init__(self, kartIdx=0, addr=None):
        assert(0 <= kartIdx < 12)
        self.addr = addr if addr else AiInput.chain(kartIdx)

        self.kart_input = self.inst_kart_input
        self.ai_controller = self.inst_ai_controller

    @staticmethod
    def chain(kartIdx=0) -> int:
        return InputMgr.ai_kart_input(kartIdx)

    @staticmethod
    def kart_input(kartIdx=0) -> int:
        ai_input_ref = AiInput.chain(kartIdx)
        kart_input_ref = ai_input_ref + 0x0
        return kart_input_ref
    
    def inst_kart_input(self) -> int:
        kart_input_ref = self.addr + 0x0
        return kart_input_ref
    
    @staticmethod
    def ai_controller(kartIdx=0) -> int:
        ai_input_ref = AiInput.chain(kartIdx)
        ai_controller_ref = ai_input_ref + 0xD8
        return ai_controller_ref
    
    def inst_ai_controller(self) -> int:
        ai_controller_ref = self.addr + 0xD8
        return ai_controller_ref