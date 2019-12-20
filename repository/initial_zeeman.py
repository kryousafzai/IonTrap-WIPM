from artiq.experiment import *
import numpy as np



class Initial_Zeeman(EnvExperiment):
    """Initial for Zeeman"""
    def build(self):

        self.setattr_argument("ZEEMAN_FREQUENCY_START", NumberValue(190, scale=1,unit="MHz",step=0.0001))
        self.setattr_argument("ZEEMAN_FREQUENCY_END", NumberValue(210, scale=1,unit="MHz",step=0.0001))
        self.setattr_argument("ZEEMAN_FREQUENCY_STEP", NumberValue(20, scale=1,unit="kHz",step=0.0001))
        self.setattr_argument("ROUND", NumberValue(100, ndecimals=0,scale=1,unit="次",step=1))
        self.setattr_argument("DPL_TIME", NumberValue(4, scale=1,unit="ms",step=1))
        self.setattr_argument("DETECTION_TIME", NumberValue(6, ndecimals=0,scale=1,unit="ms",step=1))
        self.setattr_argument("DELAY_TIME", NumberValue(7, ndecimals=0,scale=1,unit="ms",step=1))
        self.setattr_argument("ZEEMAN_DURATION_TIME",NumberValue(3,scale=1,unit="ms",step=0.1))
        self.setattr_argument("PREPARATION_TIME",NumberValue(500,scale=1,unit="us",step=1))

    def run(self):
        self.set_dataset("Run_Unit.Round", self.ROUND, broadcast=True)
        self.set_dataset("Run_Unit.DPL_Time", self.DPL_TIME, broadcast=True)
        self.set_dataset("Run_Zeeman.Zeeman_Frequency_Start", self.ZEEMAN_FREQUENCY_START*10**3, broadcast=True)
        self.set_dataset("Run_Zeeman.Zeeman_Frequency_End", self.ZEEMAN_FREQUENCY_END*10**3, broadcast=True)
        self.set_dataset("Run_Zeeman.Zeeman_Frequency_Step", self.ZEEMAN_FREQUENCY_STEP, broadcast=True)
        self.set_dataset("Run_Unit.Preparation_Time", self.PREPARATION_TIME, broadcast=True)
        self.set_dataset("Run_Unit.Detection_Time", self.DETECTION_TIME, broadcast=True)
        self.set_dataset("Run_Unit.Delay_Time", self.DELAY_TIME, broadcast=True)
        self.set_dataset("Run_Zeeman.Zeeman_Duration_Time", self.ZEEMAN_DURATION_TIME, broadcast=True)

        
        
        
        
