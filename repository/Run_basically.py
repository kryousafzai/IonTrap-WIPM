from artiq.experiment import *
import numpy as np

class Run_Basically(EnvExperiment):
    """Run basically"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")
        self.setattr_device("ttl3")

    def prepare(self):
        self.Round=self.get_dataset("Run_Unit.Round")
        self.DPL_time=self.get_dataset("Run_Unit.DPL_time")
        self.SIDE_BAND_time=self.get_dataset("Run_Unit.SIDE_BAND_time")
        self.DETECTION_time=self.get_dataset("Run_Unit.DETECTION_time")
        self.delay_time=self.get_dataset("Run_Unit.DELAY_time")
        
    @kernel
    def run(self):
        self.core.reset()
        #设置dds的振幅，频率
        self.core.reset()
        delay(10*ms)
        self.urukul1_ch0.sw.on()
        self.urukul1_ch0.set_att(0)
        delay(10*ms)
        self.urukul1_ch0.set(self.ZEEMAN_FREQUENCY_final*kHz)
        delay(10*ms)
        
        try:
            for i in range(self.Round):
                self.ttl0.on()
                self.ttl1.on()
                self.ttl2.on()
                
                delay(self.DPL_time*ms)
                
                self.ttl0.off()
                self.ttl1.off()
                self.ttl3.on()
                
                delay(self.SIDE_BAND_time*ms)
                
                self.ttl2.off()
                self.ttl3.off()
                self.ttl0.on()
                self.ttl1.on()
                
                delay(self.DETECTION_time*ms)
                
                self.ttl0.off()
                self.ttl1.off()
                
        except RTIOUnderflow:
            print("Error for time")
    
    def photon_detection(self,Threshould,Signal):
        for num_e in range(len(Threshould)-1):
            if Signal>=Threshould[num_e] and Signal<Threshould[num_e+1]:
                return num_e
            else:
                pass
                
    @kernel
    def DPL_cooling(self):
        ttl1.on()
        ttl2.on()
        ttl3.on()
        
        pause(self.DPL_time*ms)
        
        ttl1.off()
        ttl2.off()
        ttl3.off()
        
    @kernel
    def SIDE_BAND_cooling(self):
        ttl3.on()
        ttl4.on()
        
        pause(self.SIDE_BAND_time*ms)
        
        ttl3.off()
        ttl4.off()
        
    @kernel
    def PHOTON_detection(self):
        ttl1.on()
        ttl3.on()
        
        pause(self.DETECTION_time*ms)
        
        ttl1.off()
        ttl3.off()