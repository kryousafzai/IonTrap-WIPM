from artiq.experiment import *
import numpy as np

class Run_Zeeman(EnvExperiment):
    """Run As Zeeman"""
    def build(self):
        #输出端
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")
        self.setattr_device("ttl3")
        self.setattr_device("urukul1_ch0")


    def prepare(self):
        self.FR=self.get_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_start")
        self.FR_end=self.get_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_end")
        self.FR_step=self.get_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_step")
        
        self.Round=self.get_dataset("Run_Unit.Round")
        self.DPL_time=self.get_dataset("Run_Unit.DPL_time")
        self.SIDE_BAND_time=self.get_dataset("Run_Unit.SIDE_BAND_time")
        self.DETECTION_time=self.get_dataset("Run_Unit.DETECTION_time")
        self.delay_time=self.get_dataset("Run_Unit.DELAY_time")
        
    @kernel
    def run(self):
        #打开DDS信号
        self.core.reset()
        delay(10*ms)
        self.urukul1_ch0.sw.on()
        self.urukul1_ch0.set_att(20)
        delay(10*ms)
        self.urukul1_ch0.set(ZEEMAN_FREQUENCY_final*kHz)
        delay(10*ms)
        
        #开始运行
        try:
            while self.FR< self.FR_end:
                
                #设置扫zeeman的频率
                self.urukul1_ch0.set(self.FR*kHz)
                
                #相同设置条件下重复运行
                for i in range(self.Round):
                
                    #Dopplor_cooling
                    self.ttl0.on()
                    self.ttl1.on()
                    self.ttl2.on()
                    delay(self.DPL_time*ms)
                    self.ttl0.off()
                    self.ttl1.off()
                    
                    #SIDE_BAND_cooling
                    self.ttl3.on()
                    delay(self.SIDE_BAND_time*ms)
                    self.ttl2.off()
                    self.ttl3.off()
                    
                    #光子计数
                    with parallel:
                        self.ttl4.gate_rising(self.DETECTION_time*ms)
                        
                        with sequential:
                            self.ttl0.on()
                            self.ttl1.on()
                            delay(self.DETECTION_time*ms)
                            self.ttl0.off()
                            self.ttl1.off()
                    
                    #输出光子计数结果
                    self.count_t = self.ttl4.count()
                    self.set_dataset("Count_Num_t", self.count_t, broadcast=True)
                    
                    delay(self.delay_time*ms)
                
                self.FR+=self.FR_step
                delay(self.delay_time*ms)
                
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