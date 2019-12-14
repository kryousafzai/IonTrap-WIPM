# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\QC\Desktop\GUI\rabi.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from artiq.experiment import *
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import os
import sys

class GUI_Reveal(EnvExperiment,object):
    """GUI_Parallel_Test"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")
        self.setattr_device("ttl3")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("ttl4")
        
        #设置初始值，这些值可以随意设置，其目的是防止报错
        self.DPL_time=30
        self.SIDE_BAND_time=30
        self.Rabi_time=30
        self.DETECTION_time=100
        self.delay_time=100
        
        self.set_dataset("para", 1, broadcast=True)
        
    def pepare(self):
        pass
    
    @kernel
    def run(self):     
        
        while True:
        self.para=self.get_dataset("Para")
        delay(3*ms)
        if self.para==1:
                
            delay(3*ms)
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
            self.ttl0.on()
            self.ttl1.on()
            delay(self.DETECTION_time*ms)
            self.ttl0.off()
            self.ttl1.off()
        else:
            delay(3*ms)
            self.ttl0.off()
            self.ttl1.off()
            self.ttl2.off()
            self.ttl3.off()
                
        delay(100*ms)
                
