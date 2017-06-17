# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 21:18:06 2017

@author: Corey
"""
import math
import Tkinter as tk
import csv
import os
import os.path
ScriptDir = os.path.dirname(__file__)


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

def sscalc(Tmin,Tmax,Tsub,RH):
    '''
    This will calculate the average supersaturation given the following variables
    Tmin is the lower bound of the ambient temperature
    Tmax is the upper bound of the ambient temperature
    Tsub is the temperature of the substrate
    RH is the relative humidity of the environment, aka the humidity chamber
    '''
    
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
    
    def pinf(SP, SS):
        '''
        This calculates the ambient pressure from the substrate's
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

def tsubcalc(Tmin,Tmax,RH,SS):
    '''
    This will calculate the necessary RH given the following variables
    Tmin is the lower bound of the ambient temperature
    Tmax is the upper bound of the ambient temperature
    RH is the relative humidity
    SS is the supersaturation
    '''    
    Tguess = -50.0
    SSguess = -100
    while(abs(SSguess-SS) > 0.01):
        SSguess = sscalc(Tmin, Tmax, Tguess, RH)
        Tguess = Tguess + 0.005
        if(Tguess > 60):
            break
    
    return Tguess

class MainWindow:
    def __init__(self, master):        
        # The following are the variable declarations for the GUI
        self.RHbox = tk.IntVar()
        self.SSbox = tk.IntVar()
        self.Tsubbox = tk.IntVar()
        self.Tmax = tk.DoubleVar()
        self.Tmin = tk.DoubleVar()
        self.Tsub = tk.DoubleVar()
        self.RH = tk.DoubleVar()
        self.SS = tk.DoubleVar()
        self.Result = tk.DoubleVar()
        
        # This gets the values that were 
        PreviousSettingsPath = 'Files/PreviousSettings.csv'
        PreviousSettingsPath = os.path.join(ScriptDir, PreviousSettingsPath)
        PreviousSettings = []
        with open(PreviousSettingsPath) as f:
            reader = csv.reader(f)
            PreviousSettings = next(reader)
        self.RHbox.set(PreviousSettings[0])
        self.SSbox.set(PreviousSettings[1])
        self.Tsubbox.set(PreviousSettings[2])
        self.Tmax.set(PreviousSettings[3])
        self.Tmin.set(PreviousSettings[4])
        self.Tsub.set(PreviousSettings[5])
        self.RH.set(PreviousSettings[6])
        self.SS.set(PreviousSettings[7])
        

        # Create the checkboxes to decide what to compute
        self.RHcalcButton = tk.Checkbutton(master, text='Calculate RH',
                                           variable = self.RHbox, command=self.rhUpdate)
        self.SScalcButton = tk.Checkbutton(master, text='Calculate SS',
                                           variable = self.SSbox, command=self.ssUpdate)
        self.TsubcalcButton = tk.Checkbutton(master, text='Calculate Tsub',
                                           variable = self.Tsubbox, command=self.tsubUpdate)

        # Create the 'labels', aka the text
        self.TmaxLabel = tk.Label(master, text='Max ambient temperature',anchor=tk.E,width=20)
        self.TminLabel = tk.Label(master, text='Min ambient temperature',anchor=tk.E,width=20)
        self.TsubLabel = tk.Label(master, text='Substrate temperature',anchor=tk.E,width=20)
        self.RHLabel = tk.Label(master, text='Relative humidity',anchor=tk.E,width=20)
        self.SSLabel = tk.Label(master, text='Supersaturation',anchor=tk.E,width=20)

        # Create the entry boxes
        self.TmaxEntry = tk.Entry(master, textvariable=self.Tmax,width=20)
        self.TminEntry = tk.Entry(master, textvariable=self.Tmin,width=20)
        self.TsubEntry = tk.Entry(master, textvariable=self.Tsub,width=20)
        self.RHEntry = tk.Entry(master, textvariable=self.RH,width=20)
        self.SSEntry = tk.Entry(master, textvariable=self.SS,width=20)
        
        # Create the calculation button
        self.ComputeButton = tk.Button(master, text='Calculate',
                                       command = self.calculate, width=40)
        self.ResultLabel = tk.Label(master, text='')
        self.ResultNumLabel = tk.Label(master, text='Nothing yet')
        self.ResultNumLabel.configure(font=('Segoe UI', 15))
        
        # Place the checkboxes
        self.RHcalcButton.grid(row=0, column=0)
        self.SScalcButton.grid(row=0, column=1)
        self.TsubcalcButton.grid(row=0, column=2)
        
        # These place the labels in the GUI
        self.TmaxLabel.grid(row=1, column=0)
        self.TminLabel.grid(row=2, column=0)
        self.TsubLabel.grid(row=3, column=0)

        # These place the entries in the GUI
        self.TmaxEntry.grid(row=1, column=1)
        self.TminEntry.grid(row=2, column=1)
        self.TsubEntry.grid(row=3, column=1)
        
        
        if(self.RHbox.get()==1 and self.SSbox.get()==0 and self.Tsubbox.get()==0):
            self.rhUpdate()
        elif(self.RHbox.get()==0 and self.SSbox.get()==1 and self.Tsubbox.get()==0):
            self.ssUpdate()
        elif(self.RHbox.get()==0 and self.SSbox.get()==0 and self.Tsubbox.get()==1):
            self.tsubUpdate()
        
        self.ComputeButton.grid(row=6, columnspan=2)
        self.ResultLabel.grid(row=7,column=0)
        self.ResultNumLabel.grid(row=7,column=1)
        
        master.protocol("WM_DELETE_WINDOW",self.saveValues)
        
    def calculate(self):
        '''
        Calculates the value desired when the compute button is pressed
        '''
        if(self.RHbox.get() == 1):
            RH = rhcalc(self.Tmin.get(), self.Tmax.get(), self.Tsub.get(), self.SS.get())
            Result = RH
        elif(self.SSbox.get() == 1):
            SS = sscalc(self.Tmin.get(),self.Tmax.get(),self.Tsub.get(),self.RH.get())
            Result = SS
        elif(self.Tsubbox.get() == 1):
            Tsub = tsubcalc(self.Tmin.get(),self.Tmax.get(),self.RH.get(), self.SS.get())
            Result = Tsub
        else:
            top = tk.Toplevel()
            topLabel = tk.Label(top, text='Nothing is selected dummy.')
            topLabel.pack()
        roundedResult = str(round(Result,3))
        self.ResultNumLabel.configure(text=roundedResult)
        
    def rhUpdate(self):
        '''
        Show the proper fields when solving for RH
        '''
        self.SSLabel.grid(row=5, column=0)
        self.SSEntry.grid(row=5, column=1)
        self.TsubLabel.grid(row=3, column=0)
        self.TsubEntry.grid(row=3, column=1)
        self.RHLabel.grid_forget()
        self.RHEntry.grid_forget()
        self.SSbox.set(0)
        self.Tsubbox.set(0)
        self.ComputeButton.config(text='Calculate relative humidity')
        self.ResultLabel.config(text='The relative humidity is')
        
        
    def ssUpdate(self):
        '''
        Show the proper fields when solving for SS
        '''
        self.RHLabel.grid(row=4, column=0)
        self.RHEntry.grid(row=4, column=1)
        self.TsubLabel.grid(row=3, column=0)
        self.TsubEntry.grid(row=3, column=1)
        self.SSLabel.grid_forget()
        self.SSEntry.grid_forget()
        self.RHbox.set(0)
        self.Tsubbox.set(0)
        self.ComputeButton.config(text='Calculate supersaturation')
        self.ResultLabel.config(text='The supersaturation is')
        
    def tsubUpdate(self):
        '''
        Show the proper fields when solving for SS
        '''
        self.RHLabel.grid(row=4, column=0)
        self.RHEntry.grid(row=4, column=1)
        self.SSLabel.grid(row=5, column=0)
        self.SSEntry.grid(row=5, column=1)
        self.TsubLabel.grid_forget()
        self.TsubEntry.grid_forget()
        self.RHbox.set(0)
        self.SSbox.set(0)
        self.ComputeButton.config(text='Calculate substrate temperature')
        self.ResultLabel.config(text='The temperature is')
    
    def quitWindow(self):
        root.destroy()
    
    def saveValues(self):
        SavePath = 'Files/PreviousSettings.csv'
        SavePath = os.path.join(ScriptDir, SavePath)
        Settings = [self.RHbox.get(),self.SSbox.get(),self.Tsubbox.get(),self.Tmax.get(),self.Tmin.get(),
                    self.Tsub.get(),self.RH.get(),self.SS.get()]
        with open(SavePath, "w") as f:
            writer = csv.writer(f)
            writer.writerow(Settings)
        self.quitWindow()
    
root = tk.Tk()
gui = MainWindow(root)
root.mainloop()