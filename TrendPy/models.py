# -*- coding: utf-8 -*-

from . import methods as mt
import numpy as np

class Trends:
    """ Trends Class
    
    """    
    

    def __init__(self, x,
                       y,
                       ansatz,
                       deg = None,
                       ):
        self.x = x
        self.y = y
        self.ansatz = ansatz
        self.deg = deg
        self.coef = self.coef()
        self.r2 = self.r2()
        
    
    def coef(self):
    
        if self.ansatz == 'linReg':
            
            coef = mt.linReg(self.x, self.y)
            
        if self.ansatz == 'polReg':
            
            coef = mt.polReg(self.x, self.y, deg = self.deg)            
    
        return coef
    
    
    def pred(self, x):
        
        values = np.poly1d(self.coef)(x)     
        
    
        return  values      
    
    def r2(self):
        wert=mt.r2(self.y, self.pred(self.x))
        return round(wert, 3)    