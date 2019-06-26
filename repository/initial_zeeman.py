from artiq.experiment import *
import numpy as np

class Initial_Zeeman(EnvExperiment):
    """Initial for Zeeman"""
    def build(self):
    
        self.setattr_argument("ZEEMAN_FREQUENCY_start", NumberValue(0, scale=1,unit="MHz",step=1))
        self.setattr_argument("ZEEMAN_FREQUENCY_end", NumberValue(10, scale=1,unit="MHz",step=1))
        self.setattr_argument("ZEEMAN_FREQUENCY_step", NumberValue(5, scale=1,unit="kHz",step=100))
        self.setattr_argument("round", NumberValue(100, scale=1,unit="次",step=10))
        self.setattr_argument("DPL_time", NumberValue(3, scale=1,unit="ms",step=10))
        self.setattr_argument("SIDE_BAND_time", NumberValue(5, scale=1,unit="ms",step=10))
        self.setattr_argument("DETECTION_time", NumberValue(5, scale=1,unit="ms",step=10))
        self.setattr_argument("DELAY_time", NumberValue(5, scale=1,unit="ms",step=10))
        
        
    def run(self):
        self.set_dataset("Run_Unit.Round", self.round, broadcast=True)
        self.set_dataset("X", [0,1,2,3], broadcast=True)
        self.set_dataset("Y", [0,1,2,3], broadcast=True)
        
        self.set_dataset("Run_Unit.DPL_time", self.DPL_time, broadcast=True)
        self.set_dataset("Run_Unit.SIDE_BAND_time", self.SIDE_BAND_time, broadcast=True)
        
        self.set_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_start", self.ZEEMAN_FREQUENCY_start*10**3, broadcast=True)
        self.set_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_end", self.ZEEMAN_FREQUENCY_end*10**3, broadcast=True)
        self.set_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_step", self.ZEEMAN_FREQUENCY_step, broadcast=True)
        self.set_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_final", self.ZEEMAN_FREQUENCY_start*10**3, broadcast=True)
        
        self.set_dataset("Run_Unit.DETECTION_time", self.DETECTION_time, broadcast=True)
        self.set_dataset("Run_Unit.DELAY_time", self.DELAY_time, broadcast=True)
        
        self.set_dataset("Count_Num", 0, broadcast=True)

        
        
        
        