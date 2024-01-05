import numpy as np
from scipy.optimize import least_squares, minimize, curve_fit
import sympy as sym
from sympy import atan as arctan
from sympy import sqrt, sin, cos, tan, exp, log, ln
a, b, c, x = sym.symbols('a, b, c, x', real=True)

def linReg(x_in,y):
    '''Time series linear regression. Returns coefs in polynomial descending order.
       Coefs computed analytically.
    '''
    
    a = (np.inner(x_in,y) - (len(x_in) * np.mean(x_in) * np.mean(y))) / (np.inner(x_in,x_in) - (len(x_in) * ((np.mean(x_in))**2)))
    b = np.mean(y) - a * np.mean(x_in)
    return [a,b]

def polReg(x_in,y, deg):
    '''Time series polynomial regression. Returns coefs in polynomial descending order.
       Coefs computed numerically.
    '''
    
    coefs = np.polyfit(x_in, y, deg)
    return coefs

def freeReg(x_in, y_out, ansatz):
    '''Regression with user ansatz. The ansatz is expected to depend on three
       parameters, a, b, and c. The ansatz is expected to be a string with a 
       symbolic formulation. for instance: 'a*arctan(b*x_in+c)'.
    '''    
    test_func = sym.lambdify((x, a, b, c), eval(ansatz))
    
    res = curve_fit(test_func, x_in, y_out)

    return res[0]    


def trigReg(x_in, y):
    '''Time seriessine regression. Returns amplitude, frequency and phase
    '''    
    timestep = x_in[1]-x_in[0]
    x_in = np.fft.fftfreq(len(x_in), timestep)
    Y = np.fft.fft(y)

    index = np.argmax(abs(Y))
    
    amplitude = 2*np.absolute(Y[index])/len(x_in)
    frequenz = abs(x_in[index])
    angle = np.angle(Y[index])    
    
    coefs = np.array([amplitude, frequenz, angle])
    
    return coefs

def expReg(x_in,y):
    '''Time series exponential regression. 
    '''
    coef_first_step = linReg(x_in,np.log(y))
    b = coef_first_step[0]
    a = np.exp(coef_first_step[1])
    return [a,b]

def pred(ansatz, coef, x_in, freeRegAnsatz=None):
    '''Computes the predction for input x_in and the computed corresponding
       coefficients
    ''' 
        
    if ansatz == 'linReg' or ansatz == 'polReg':
        values = np.poly1d(coef)(x_in)     
            
    if ansatz == 'trigReg':
        amplitude, frequenz, angle = coef
        values = amplitude*np.cos(2*np.pi*frequenz*x_in+angle)  
        
    if ansatz == 'expReg':
        values = coef[0]*np.exp(coef[1]*x_in) 
        
    if ansatz == 'freeReg':
        #print(eval(freeRegAnsatz))
        f = eval(freeRegAnsatz).subs(a, coef[0]).subs(b, coef[1]).subs(c, coef[2])
        f_num = sym.lambdify(x, f)       
        values = f_num(x_in)
        
        
    return  values 

def r2(y, y_pred):
        '''Coefficient of determination
        '''
        wert = 1-np.sum((y-y_pred)**2)/np.sum((y-np.mean(y))**2)
        return wert


