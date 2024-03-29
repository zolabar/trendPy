# -*- coding: utf-8 -*-

from . import methods as mt


class Trend:
    """ 
    Trends Class. Initialization of Trend with training input, training output,
    ansatz (string) and deg (if polynomial ansatz). The following ansatz
    are supported 'linReg', 'polReg', 'expReg', 'trigReg', 'freeReg'.
    
    Examples
    ========

    >>> from trendpy2 import models as tpm
    >>> x = np.array([1, 2, 3])
    >>> y = np.array([1, 1.5, 3.5])
    >>> lin = tpm.Trend(x, y, 'linReg')
    
    """    
    

    def __init__(self, x,
                       y,
                       ansatz,
                       deg = None,
                       freeRegAnsatz=None,
                       ):

        self.x = x
        self.y = y
        self.ansatz = ansatz
        self.deg = deg
        self.freeRegAnsatz = freeRegAnsatz
        self.coef = self.coef()
        self.coefs = self.coef
        self.r2 = self.r2()
        
    
    def coef(self):
        '''
        Computes coefficients of corresponding ansatz-
        
        Examples
        ========
    
   
        >>> lin.coef
        >>> [1.25, -0.5]
        
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
        '''
        Computes the predction for input x and the computed corresponding
        coefficients.
        
        Examples
        ========
      
        >>> lin.pred(3)
        >>> 3.25        
        ''' 
        
        values = mt.pred(self.ansatz, self.coef, x, freeRegAnsatz=self.freeRegAnsatz)            
        
    
        return  values 
    

    def predict(self, x):
        '''
        The same as pred.
        ''' 
    
        return self.pred(x)     
    
    def r2(self):
        '''
        Computes the coefficient of determination for the training input.
        
        Examples
        ========
     
        >>> lin.r2
        >>> 0.893          
        ''' 
        wert=mt.r2(self.y, self.pred(self.x))
        return round(wert, 3)    