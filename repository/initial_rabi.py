from artiq.experiment import *

import numpy as np



class Initial_Rabi(EnvExperiment):

    """Initial for Rabi"""

    def build(self):

        #设置扫rabi的参数
        self.setattr_argument("ROUND", NumberValue(100, ndecimals=0,scale=1,unit="次",step=1))

        self.setattr_argument("RABI_TIME_START", NumberValue(0, ndecimals=0,scale=1,unit="ns",step=1))

        self.setattr_argument("RABI_TIME_END", NumberValue(3000, ndecimals=0,scale=1,unit="ns",step=1))

        self.setattr_argument("RABI_TIME_STEP", NumberValue(10, ndecimals=0,scale=1,unit="ns",step=1))

        self.setattr_argument("DETECTION_TIME", NumberValue(6, scale=1,unit="ms",step=0.1))

        self.setattr_argument("DELAY_TIME",NumberValue(7, ndecimals=0,scale=1,unit="ms",step=1))

        self.setattr_argument("PREPARATION_TIME",NumberValue(500, ndecimals=0,scale=1,unit="us",step=1))

        self.setattr_argument("DPL_TIME",NumberValue(3, ndecimals=0,scale=1,unit="ms",step=1))

        self.setattr_argument("SBL_TIME",NumberValue(20, ndecimals=0,scale=1,unit="ms",step=1))

        self.setattr_argument("PREPARATION_FREQUENCY",NumberValue(200, scale=1,unit="MHz",step=0.0001))

        self.setattr_argument("SBL_FREQUENCY",NumberValue(200, scale=1,unit="MHz",step=0.0001))

        self.setattr_argument("RABI_FREQUENCY",NumberValue(200, scale=1,unit="MHz",step=0.0001))




    
    def run(self):
        #将参数以目录形式显示在dataset中

        self.set_dataset("Run_Unit.Round", self.ROUND, broadcast=True)

        self.set_dataset("Run_Rabi.Rabi_Time_Start", self.RABI_TIME_START, broadcast=True)

        self.set_dataset("Run_Rabi.Rabi_Time_End", self.RABI_TIME_END, broadcast=True)

        self.set_dataset("Run_Rabi.Rabi_Time_Step", self.RABI_TIME_STEP, broadcast=True)

        self.set_dataset("Run_Unit.Detection_Time", self.DETECTION_TIME, broadcast=True)

        self.set_dataset("Run_Unit.Delay_Time", self.DELAY_TIME, broadcast=True)

        self.set_dataset("Run_Unit.Preparation_Time", self.PREPARATION_TIME, broadcast=True)

        self.set_dataset("Run_Unit.DPL_Time", self.DPL_TIME, broadcast=True)

        self.set_dataset("Run_Unit.SBL_Time", self.SBL_TIME, broadcast=True)

        self.set_dataset("Run_Unit.Round", self.ROUND, broadcast=True)

        self.set_dataset("Run_Rabi.Preparation_Frequency", self.PREPARATION_FREQUENCY, broadcast=True)

        self.set_dataset("Run_Rabi.SBL_Frequency", self.SBL_FREQUENCY, broadcast=True)

        self.set_dataset("Run_Rabi.Rabi_Frequency", self.RABI_FREQUENCY, broadcast=True)
        
        
        

        
        
        
