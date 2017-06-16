# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 21:18:06 2017

@author: Corey
"""
import math as math
import Tkinter as tk

def sscalc(Tmin,Tmax,Tsub,RH):
    '''
    This will calculate the average supersaturation given the following variables
    Tmin is the lower bound of the ambient temperature
    Tmax is the upper bound of the ambient temperature
    Tsub is the temperature of the substrate
    RH is the relative humidity of the environment, aka the humidity chamber
    '''
    def kelvin(Temp):
        '''
        Convert the temperatures to kelvin
        '''
        Tkelvin = Temp + 273.15
        return Tkelvin
    
    def spwater(Temp):
        '''
        This calculates the saturation pressure over water for a given temperature.
        '''
        SPwater = math.exp(54.842763-6763.22/Temp-4.21*math.log(Temp)+0.000367*Temp
              +math.tanh(0.0415*(Temp-218.8))*(53.878-1331.22/Temp-9.44523*math.log(Temp)
              +0.014025*Temp))
        return SPwater
    
    def spice(Temp):
        '''
        While it may sound spicy, this actually is meant to calcuate the saturation
        pressure over ice.  It isn't used but I liked the variable name
        '''
        SPice=math.exp(9.550426-5723.265/Temp+3.53068*math.log(Temp)-0.00728332*Temp)
        return SPice
    
    def pinf(SP,RH):
        '''
        This calculates the pressure of the ambient using the saturation pressure
        over water and relative humidity
        '''
        Pinf = (SP*RH)/100
        return Pinf
    
    def supersaturation(pinf, SP):
        '''
        This calculates the supersaturation from a given Pinf and the substrate's
        saturation pressure over water
        '''
        S = pinf / SP
        return S
    
    Tmax = kelvin(Tmax)
    Tmin = kelvin(Tmin)
    Tsub = kelvin(Tsub)
    
    spMax = spwater(Tmax)
    spMin = spwater(Tmin)
    spSub = spwater(Tsub)
    
    pinfMax = pinf(spMax,RH)
    pinfMin = pinf(spMin,RH)
    
    sMax = pinfMax/spSub
    sMin = pinfMin/spSub
    
    SS = (sMax + sMin)/2
    
    return SS


def rhcalc(Tmin,Tmax,Tsub,SS):
    '''
    This will calculate the necessary RH given the following variables
    Tmin is the lower bound of the ambient temperature
    Tmax is the upper bound of the ambient temperature
    Tsub is the temperature of the substrate
    SS is the supersaturation
    '''
    
    def kelvin(Temp):
        '''
        Convert the temperatures to kelvin
        '''
        Tkelvin = Temp + 273.15
        return Tkelvin
    
    def spwater(Temp):
        '''
        This calculates the saturation pressure over water for a given temperature.
        '''
        SPwater = math.exp(54.842763-6763.22/Temp-4.21*math.log(Temp)+0.000367*Temp
              +math.tanh(0.0415*(Temp-218.8))*(53.878-1331.22/Temp-9.44523*math.log(Temp)
              +0.014025*Temp))
        return SPwater
    
    def spice(Temp):
        '''
        While it may sound spicy, this actually is meant to calcuate the saturation
        pressure over ice.  It isn't used but I liked the variable name
        '''
        SPice=math.exp(9.550426-5723.265/Temp+3.53068*math.log(Temp)-0.00728332*Temp)
        return SPice

    def pinf(SP, SS):
        '''
        This calculates the ambient pressure fromthe substrate's
        saturation pressure over water and desired supersaturation
        '''
        pinf = SP * SS
        return pinf
    
    def rh(SP,Pinf):
        '''
        This calculates the pressure of the ambient using the saturation pressure
        over water and relative humidity
        '''
        RH = (Pinf*100)/SP
        return RH
    

    
    Tmax = kelvin(Tmax)
    Tmin = kelvin(Tmin)
    Tsub = kelvin(Tsub)
    
    spMax = spwater(Tmax)
    spMin = spwater(Tmin)
    spSub = spwater(Tsub)
    
    pinf = pinf(spSub,SS)
    
    RHMax = rh(spMax,pinf)
    RHMin = rh(spMin,pinf)
    
    RH = (RHMax + RHMin)/2
    
    return RH

class MainWindow:
    def __init__(self, master):
        
        
        # The following are the variable declarations for the GUI
        self.RHcalc = tk.IntVar()
        self.SScalc = tk.IntVar()
        self.Tmax = tk.DoubleVar()
        self.Tmin = tk.DoubleVar()
        self.Tsub = tk.DoubleVar()
        self.RH = tk.DoubleVar()
        self.SS = tk.DoubleVar()
        self.Result = tk.DoubleVar()
        
        self.RHcalc.set(1)
        
        def calculate(self, RHcalc, SScalc, Tmin, Tmax, Tsub, SS, RH):
            if(RHcalc == 1):
                RH = rhcalc(Tmin, Tmax, Tsub, SS)
                Result = RH
            elif(SScalc == 1):
                SS = sscalc(Tmin,Tmax,Tsub,RH)
                Result = SS
            else:
                top = tk.Toplevel()
                topLabel = tk.Label(top, text='Nothing is selected dummy.')
                topLabel.pack()
            self.Result.set(Result)
            
        
        # Create the checkboxes to decide what to compute
        self.RHcalcButton = tk.Checkbutton(master, text='Calculate RH', variable = self.RHcalc)
        self.SScalcButton = tk.Checkbutton(master, text='Calculate SS', variable = self.SScalc)
        
        # Create the 'labels', aka the text
        self.TmaxLabel = tk.Label(master, text='Max ambient temperature')
        self.TminLabel = tk.Label(master, text='Min ambient temperature')
        self.TsubLabel = tk.Label(master, text='Substrate temperature')
        self.RHLabel = tk.Label(master, text='Minimum ambient temperature')
        self.SSLabel = tk.Label(master, text='Desired supersaturation')

        # Create the entry boxes
        self.TmaxEntry = tk.Entry(master, textvariable=self.Tmax)
        self.TminEntry = tk.Entry(master, textvariable=self.Tmin)
        self.TsubEntry = tk.Entry(master, textvariable=self.Tsub)
        self.RHEntry = tk.Entry(master, textvariable=self.RH)
        self.SSEntry = tk.Entry(master, textvariable=self.SS)
        
        # Create the calculation button
        self.ComputeButton = tk.Button(master, text='Calculate',
                                       command = calculate(self, self.RHcalc.get(), 
                                                           self.SScalc.get(), 
                                                           self.Tmin.get(),
                                                           self.Tmax.get(),
                                                           self.Tsub.get(),
                                                           self.SS.get(),
                                                           self.RH.get()))
        self.ResultLabel = tk.Label(master, textvariable=self.Result)
        
        
        # Place the checkboxes
        self.RHcalcButton.grid(row=0, column=0)
        self.SScalcButton.grid(row=0, column=1)
        
        # These place the labels in the GUI
        self.TmaxLabel.grid(row=1, column=0)
        self.TminLabel.grid(row=2, column=0)
        self.TsubLabel.grid(row=3, column=0)
        self.RHLabel.grid(row=4, column=0)
        self.SSLabel.grid(row=5, column=0)
        
        # These place the entries in the GUI
        self.TmaxEntry.grid(row=1, column=1)
        self.TminEntry.grid(row=2, column=1)
        self.TsubEntry.grid(row=3, column=1)
        self.RHEntry.grid(row=4, column=1)
        self.SSEntry.grid(row=5, column=1)
        
        self.ComputeButton.grid(row=6, columnspan=2)
        self.ResultLabel.grid(row=7,columnspan=2)
        
        

root = tk.Tk()
gui = MainWindow(root)
root.mainloop()