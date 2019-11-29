from artiq.experiment import *
import numpy as np

class Run_Rabi(EnvExperiment):
    """Run As Rabi"""
    def build(self):
        #输出端
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")
        self.setattr_device("ttl3")
        self.setattr_device("urukul1_ch0")
        #输入端
        self.setattr_device("ttl4")

    def prepare(self):
        self.Rabi_time=self.get_dataset("Run_Unit.RABI.RABI_TIME_start")
        self.Rabi_time_end=self.get_dataset("Run_Unit.RABI.RABI_TIME_end")
        self.Rabi_time_step=self.get_dataset("Run_Unit.RABI.RABI_TIME_step")
        self.Round=self.get_dataset("Run_Unit.Round")
        self.DPL_time=self.get_dataset("Run_Unit.DPL_time")
        self.SIDE_BAND_time=self.get_dataset("Run_Unit.SIDE_BAND_time")
        self.DETECTION_time=self.get_dataset("Run_Unit.DETECTION_time")
        self.delay_time=self.get_dataset("Run_Unit.DELAY_time")
        self.ZEEMAN_FREQUENCY_final=self.get_dataset("Run_Unit.ZEEMAN.ZEEMAN_FREQUENCY_final")
        
    @kernel
    def run(self):
        #设置dds的振幅，频率
        self.core.reset()
        delay(10*ms)
        self.urukul1_ch0.sw.on()
        self.urukul1_ch0.set_att(0)
        delay(10*ms)
        self.urukul1_ch0.set(self.ZEEMAN_FREQUENCY_final*kHz)
        delay(10*ms)
        
        #开始运行
        try:
            while self.Rabi_time< self.Rabi_time_end:
                
                for i in range(self.Round):
                    
                    #Dopplor_cooling
                    self.ttl0.on()
                    self.ttl1.on()
                    self.ttl2.on()
                    delay(self.DPL_time*ms)
                    self.ttl0.off()
                    self.ttl1.off()
                    
                    #Side_band_cooling
                    self.ttl3.on()
                    delay(self.SIDE_BAND_time*ms)
                    self.ttl2.off()
                    self.ttl3.off()
                    
                    #控制Rabi时长
                    self.ttl3.on()
                    delay(self.Rabi_time*us)
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
                    
                self.Rabi_time+=self.Rabi_step
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
