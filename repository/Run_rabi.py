from artiq.experiment import *

import numpy as np



class Run_Rabi(EnvExperiment):

    """Run As Rabi"""

    def build(self):
        
        self.setattr_device("core")

        self.setattr_device("ttl4")#397

        self.setattr_device("ttl6")#866

        self.setattr_device("ttl8")#854

        self.setattr_device("ttl10")#729
        
        self.setattr_device("ttl1")#计数上升沿

        self.setattr_device("urukul0_ch0")
        
        self.setattr_device("urukul0_ch1")

        self.setattr_device("urukul0_ch2")
        
        self.setattr_device("urukul0_cpld")






    def prepare(self):
        #取出dataset中对应目录的值，赋给全局变量

        self.Rabi_Time=self.get_dataset("Run_Rabi.Rabi_Time_Start")

        self.Rabi_Time_End=self.get_dataset("Run_Rabi.Rabi_Time_End")

        self.Rabi_Time_Step=self.get_dataset("Run_Rabi.Rabi_Time_Step")

        self.Round=self.get_dataset("Run_Unit.Round")

        self.Detection_Time=self.get_dataset("Run_Unit.Detection_Time")

        self.Delay_Time=self.get_dataset("Run_Unit.Delay_Time")

        self.Preparation_Time=self.get_dataset("Run_Unit.Preparation_Time")

        self.DPL_Time=self.get_dataset("Run_Unit.DPL_Time")

        self.SBL_Time=self.get_dataset("Run_Unit.SBL_Time")

        self.Preparation_Frequency=self.get_dataset("Run_Rabi.Preparation_Frequency")

        self.SBL_Frequency=self.get_dataset("Run_Rabi.SBL_Frequency")

        self.Rabi_Frequency=self.get_dataset("Run_Rabi.Rabi_Frequency")
        
    @kernel
    def run(self):
        self.core.reset()
        #刷新时间轴防止报错
        self.urukul0_cpld.init()
        self.urukul0_ch0.init()
        self.urukul0_ch1.init()
        self.urukul0_ch2.init()
        self.urukul0_ch0.sw.on()
        self.urukul0_ch1.sw.on()
        self.urukul0_ch2.sw.on()
        #打开三个dds
        try:
            while self.Rabi_Time<self.Rabi_Time_End:
                #while循环
                self.set_dataset("Run_Rabi.Rabi_Time",self.Rabi_Time,broadcast=True)
                total_count=0
                #总光子数开始时为0
                for i in range(self.Round):
                    #多普勒冷却
                    self.ttl4.on()#打开397
                    self.ttl6.on()#打开866
                    self.ttl8.on()#打开854
                    delay(self.DPL_Time*ms)#持续设置的多普勒冷却时长
                    #态制备
                    self.ttl4.off()#关闭397
                    self.ttl10.on()#打开729
                    self.urukul0_ch0.set(self.Preparation_Frequency*MHz)#设置态制备729频率
                    delay(self.Preparation_Time*us)#持续态制备时长
                    #边带冷却
                    self.urukul0_ch1.set(self.SBL_Frequency*MHz)#设置边带冷却频率
                    delay(self.SBL_Time*ms)#持续边带冷却时长
                    #Rabi扫描
                    self.urukul0_ch2.set(self.Rabi_Frequency)#设置扫Rabi频率
                    self.ttl8.off()#关闭854
                    delay(self.Rabi_Time*ns)#持续Rabi时长
                    self.ttl10.off()#关闭729
                    #态探测
                    with parallel:#同时进行
                        gate_end_mu = self.ttl1.gate_rising(self.Detection_Time*ms)
                        #记录上升沿
                        with sequential:
                            self.ttl4.on()#打开397
                            delay(self.Detection_Time*ms)#持续探测时长
                            self.ttl6.off()#关闭866
                            self.ttl4.off()#关闭397

                    num_rising_edges =self.ttl1.count(gate_end_mu)
                    #上升沿计数
                    self.set_dataset("photon.count", num_rising_edges, broadcast=True)
                    #将上升沿数量显示在dataset中    
                    delay(self.Delay_Time*ms)
                    #持续空转时间
                    total_count+=num_rising_edges
                    #光子计数叠加
                self.set_dataset("photon.count_total", total_count, broadcast=True)
                #将self.Round次内的总光子计数显示在dataset中
                self.Rabi_Time+=self.Rabi_Time_Step
                #Rabi时长按给定步长增加
                   
        except RTIOUnderflow:
            #时间溢出报错时会打印"Error for time"
            print("Error for time")
