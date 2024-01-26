# -*- coding: utf-8 -*-

from . import methods as mt
import numpy as np

class Trend:
    """ Trends Class
    
    """    
    

    def __init__(self, x,
                       y,
                       ansatz,
                       deg = None,
                       freeRegAnsatz=None,
                       ):
        '''Initialization of Trend with training input, training output,
           ansatz (string) and deg (if polynomial ansatz)
        '''
        self.x = x
        self.y = y
        self.ansatz = ansatz
        self.deg = deg
        self.freeRegAnsatz = freeRegAnsatz
        self.coef = self.coef()
        self.r2 = self.r2()
        
    
    def coef(self):
        '''Computes coefficients of corresponding ansatz
        '''
    
        if self.ansatz == 'linReg':
            
            coef = mt.linReg(self.x, self.y)
            
        if self.ansatz == 'polReg':
            
            coef = mt.polReg(self.x, self.y, deg = self.deg) 
            
        if self.ansatz == 'trigReg':
            
            coef = mt.trigReg(self.x, self.y)
            
        if self.ansatz == 'expReg':
            
            coef = mt.expReg(self.x, self.y)  
            
        if self.ansatz == 'freeReg':
            
            coef = mt.freeReg(self.x, self.y, self.freeRegAnsatz)             
    
        return coef
    
    
    def pred(self, x):
        '''Computes the predction for input x and the computed corresponding
           coefficients
        ''' 
        
        values = mt.pred(self.ansatz, self.coef, x, freeRegAnsatz=self.freeRegAnsatz)            
        
    
        return  values      
    
    def r2(self):
        '''Computes the coefficient of determination for the training input
        ''' 
        wert=mt.r2(self.y, self.pred(self.x))
        return round(wert, 3)    