from artiq.experiment import *

import numpy as np

class Run_Zeeman(EnvExperiment):
    "Run As Zeeman"
    def build(self):
        self.setattr_device("core")

        self.setattr_device("ttl4")#397

        self.setattr_device("ttl6")#866

        self.setattr_device("ttl8")#854

        self.setattr_device("ttl10")#729

        self.setattr_device("ttl1")#上升沿计数

        self.setattr_device("urukul0_ch0")#控制729dds

        self.setattr_device("urukul0_cpld")

    def prepare(self):

        self.Zeeman_Frequency=self.get_dataset("Run_Zeeman.Zeeman_Frequency_Start")

        self.Zeeman_Frequency_End=self.get_dataset("Run_Zeeman.Zeeman_Frequency_End")

        self.Zeeman_Frequency_Step=self.get_dataset("Run_Zeeman.Zeeman_Frequency_Step")

        self.Round=self.get_dataset("Run_Unit.Round")

        self.DPL_Time=self.get_dataset("Run_Unit.DPL_Time")

        self.Detection_Time=self.get_dataset("Run_Unit.Detection_Time")

        self.Delay_Time=self.get_dataset("Run_Unit.Delay_Time")
       
        self.Preparation_Time=self.get_dataset("Run_Unit.Preparation_Time")

        self.Zeeman_Duration_Time=self.get_dataset("Run_Zeeman.Zeeman_Duration_Time")

    @kernel
    def run(self):
        self.core.reset()
        #加上一句刷新时间轴的代码以防止出现时间溢出类型的报错
        self.urukul0_cpld.init()
        self.urukul0_ch0.init()
        self.urukul0_ch0.sw.on()
        #打开dds
        self.urukul0_ch0.set_att(2.0)
        #设置dds功率为10-2=8dbm
        try:
            while self.Zeeman_Frequency< self.Zeeman_Frequency_End:
                self.urukul0_ch0.set(self.Zeeman_Frequency*kHz)
                #设置729nm激光频率
                total_count=0
                #总光子数初始为0
                for i in range(self.Round):
                    #多普勒冷却
                    self.ttl4.on()#打开397
                    self.ttl6.on()#打开866
                    self.ttl8.on()#打开854
                    delay(self.DPL_Time*ms)#持续多普勒冷却时长
                    #态制备
                    self.ttl4.off()#关闭397
                    self.ttl10.on()#打开729
                    delay(self.Preparation_Time*us)#持续态制备时长
                    #扫描Zeeman
                    self.ttl8.off()#关闭854
                    delay(self.Zeeman_Duration_Time*ms)#持续Zeeman扫描时长
                    #态探测
                    with parallel:#同时运行
                        gate_end_mu = self.ttl1.gate_rising(self.Detection_Time*ms)
                        #记录探测时长内的上升沿
                        with sequential:
                            self.ttl4.on()#打开397
                            self.ttl10.off()#关闭729
                            delay(self.Detection_Time*ms)
                        
                    num_rising_edges =self.ttl1.count(gate_end_mu)
                    #计数上升沿
                    self.set_dataset("photon.count", num_rising_edges, broadcast=True)
                    #将上升沿数据显示在dataset中
                    delay(self.Delay_Time*ms)
                    #持续空转时间
                    total_count+=num_rising_edges
                    #每次光子计数叠加
                self.set_dataset("photon.count_total", total_count, broadcast=True)
                #将self.Round次内总的光子计数显示在dataset中。
                self.Zeeman_Frequency+= self.Zeeman_Frequency_Step
                #扫描频率增加一个步长


        except RTIOUnderflow:
            #时间溢出报错时会打印"Error for time"
            print("Error for time")
