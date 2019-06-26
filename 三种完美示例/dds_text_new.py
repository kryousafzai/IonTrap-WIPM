from artiq.experiment import *
import numpy as np

class Test_dds(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul1_ch0")
        
    @kernel
    def run(self):
        self.core.reset()
        delay(10*ms)
        # self.ttl4.output()
        self.urukul1_ch0.sw.on()
        self.urukul1_ch0.set_att(5.0)
        delay(100*ms)
        try:
            self.urukul1_ch0.set(200*kHz)
            delay(3000*ms)
            self.urukul1_ch0.set(500*kHz)
            delay(3000*ms)
            self.urukul1_ch0.set(1000*kHz)
            delay(3000*ms)

            self.urukul1_ch0.sw.off()
            
        except RTIOUnderflow:
            print("Error for time")
    