import numpy as np
from artiq.experiment import *


class Photon_Detction(EnvExperiment):
    """Photon_Detction"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl4")
        self.setattr_device("ttl6")

    #假设gate_rising语法和delay语法作用一样，则可以成功
    @kernel
    def run(self):
        self.core.reset()
        delay(10*ms)

        with parallel:
            self.ttl0.gate_rising(300*ms)
            
            for i in range(120):
                self.ttl4.on()
                delay(1*ms)
                self.ttl4.off()
                delay(1*ms)
        self.ttl4.off()
        self.ttl6.off()               
        count = self.ttl0.count()
        print(count)