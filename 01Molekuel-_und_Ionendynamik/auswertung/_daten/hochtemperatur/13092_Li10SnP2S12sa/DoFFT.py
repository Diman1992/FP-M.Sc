#!/usr/bin/env python 
"""FirstPlot.py

September 2010
Opens a data file and shows it in a plot
updated April 2011
"""
import sys
import os
# import pprint
import random
import wx
import numpy
import scipy
import math
import matplotlib
from read_files import *
import re
import scipy.integrate as integrate
#import pygtk
#import gtk

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#



def calculate_offset(timesignal, ts_offset_percent):
    offset_value=0
    #print "Calculating offset value..."
    num_channels = len(timesignal)
    #print "Overall %s channels" %num_channels
    num_offset = int(num_channels * ts_offset_percent /100)
    #print "Taking last %s channels" %num_offset
    for i in range(num_offset):
        offset_value = offset_value + timesignal[num_channels-i-1]
    offset_value = offset_value / num_offset
    #print "Offset = %s" %offset_value
    return offset_value

def sign(value):
    if value>0.0:
        return 1
    elif value<0.0:
        return -1
    else:
        return 0
    
def rot_spec(spec_real, spec_imaginary, rotangle):
    rotangle=rotangle*math.pi/180.0
    spec_real2=[None]*len(spec_real)
    spec_imaginary2=[None]*len(spec_real)
    for i in range(len(spec_real)):
        spec_real2[i]=spec_real[i]*math.cos(rotangle)-spec_imaginary[i]*math.sin(rotangle)
        spec_imaginary2[i]=spec_real[i]*math.sin(rotangle)+spec_imaginary[i]*math.cos(rotangle)
    return [spec_real2, spec_imaginary2]
        
def rot_ts(ts_real, ts_imaginary, rotangle):
    rotangle=rotangle*math.pi/180.0
    ts_real2=[None]*len(ts_real)
    ts_imaginary2=[None]*len(ts_real)
    for i in range(len(ts_real)):
        ts_real2[i]=ts_real[i]*math.cos(rotangle)-ts_imaginary[i]*math.sin(rotangle)
        ts_imaginary2[i]=ts_real[i]*math.sin(rotangle)+ts_imaginary[i]*math.cos(rotangle)
    return [ts_real2, ts_imaginary2]


class DoFFT():
    """ The main programm for the FFT
    """
    title = 'Dortmunder FFT for NMR-data'
    
    def __init__(self):
               
        self.filename = ""
        self.header= ""
        self.header_dict={}
        self.dwelltime = 1.0
        self.aquisitionfrequency = 1.0
        self.tslength = 1
        self.ts_time = []
        self.ts_real = []
        self.ts_imaginary = []
        self.ts_real2 = []
        self.ts_imaginary2 = []
        self.ts_real_backup = []
        self.ts_imaginary_backup = []
        self.ts_offset_percent = 10
        self.ts_real_offset = 0
        self.ts_imaginary_offset = 0

        self.apo_real=[]
        self.apo_imaginary=[]
        self.apo_width=0.0
        self.used_apo=False
        self.apo_spec_real=[]
        self.apo_spec_ana=[]
        
        self.ts_maxchannel = 0
        self.ts_maxchannel_time = [0]
        self.ts_maxchannel_real = [0]
        
        self.first_dp=True
        

        self.zero_fill=0
        self.summe=0.0
        
        self.spec_freq = []
        self.spec_real = []
        self.spec_imaginary = []
        self.spec_real_backup = []
        self.spec_imaginary_backup = []


        self.pulse_cor_real =[]
        self.pulse_cor_imag =[]
        self.used_pulse_cor=False
        self.pulse_length=0.0
        
        self.spec_phase = 0.0
        
        self.fwhm = 0.0
        self.maxfreq = 0.0
        self.meanfreq = 0.0
        self.sec_moment = 0.0
        self.skewness = 0.0
        self.kurtosis = 0.0
        
             
    def undo(self):
        #  ts  recover
        for i in range(len(self.ts_time)):
            self.ts_real[i]=self.ts_real_backup[i]
            self.ts_imaginary[i]=self.ts_imaginary_backup[i]
        # calc off set again
        self.ts_real_offset = calculate_offset(self.ts_real, self.ts_offset_percent)
        self.ts_imaginary_offset = calculate_offset(self.ts_imaginary, self.ts_offset_percent)

        # spec delete
        self.spec_freq = []
        self.spec_real = []
        self.spec_imaginary = []
        self.spec_phase=0.0
        
        print "Backup loaded!"
        return True

    def set_first_dp(self,checked=False):
        if checked==True:
            self.first_dp=True
        elif checked==False:
            self.first_dp=False
         

    def get_first_dp(self):
        return self.first_dp

    def get_zero_fill(self):
        return self.zero_fill
            
       
        
    def fft(self,zero_points=None):
        fdp_real_backup=self.ts_real[0]
        fdp_imaginary_backup=self.ts_imaginary[0]
        if self.first_dp:
            self.ts_real[0]=self.ts_real[0]/2.0
            self.ts_imaginary[0]=self.ts_imaginary[0]/2.0
            #print "Use half frist data point!"
        else:
            print "Use full frist data point!"
            
        realdata = numpy.array(self.ts_real)
        imdata = numpy.array(self.ts_imaginary)
        data = realdata + 1j*imdata
        if zero_points==None:
            points = len(self.ts_real)
            self.zero_fill=0
        else:
            if len(self.ts_real)>zero_points:
                points=len(self.ts_real)
                self.zero_fill=0
            else:
                points=zero_points
                self.zero_fill=points


        #check for sinx faltung
        self.calc_offset_percent(5)
        if self.ts_real_offset/float(max(self.ts_real))>0.001:
            print "Your offset is maybe to large!\n A box / sinc function might cover your spectra!"

       
        fftdata = numpy.fft.fftshift(numpy.fft.fft(data, points))
        # create our x axis
        n = fftdata.size
        self.spec_freq = numpy.fft.fftshift(numpy.fft.fftfreq(n, 1.0/self.aquisitionfrequency))
        self.spec_real = fftdata.real
        self.spec_imaginary = fftdata.imag

        self.spec_real_backup =  self.spec_real[:]
        self.spec_imaginary_backup = self.spec_imaginary[:]
        
        self.ts_real[0]=fdp_real_backup
        self.ts_imaginary[0]=fdp_imaginary_backup
        self.set_phase(self.get_phase())
        
        return True



    def get_header(self):
        return self.header

    def create_header_dict(self):
        head_elements = self.header.splitlines()
        head_elements = [re.split('[=:]', element,1) for element in head_elements]
        head_elements = [ [l.strip('[! ]') for l in element] for element in head_elements]
        for l in head_elements[:]:
            if len(l)!=2:
                print "removed element from header dictionary: " + str(head_elements[head_elements.index(l)])
                head_elements.remove(l)
        #convert to dictionary:
        self.header_dict = dict(head_elements)
        
        return True
    
    def get_header_dict(self):
        return self.header_dict

    def get_ts(self):
        return [self.ts_real[:],self.ts_imaginary[:]]

    def get_ts_backup(self):
        return [self.ts_real_backup[:],self.ts_imaginary_backup[:]]

    def get_time(self):
        return self.ts_time[:]

    def get_freq(self):
        return self.spec_freq[:]

    def get_spec(self):
        return [self.spec_real[:],self.spec_imaginary[:]]


    #  def get_norm_apo(self):
    #       return [self.apo_real[:],self.apo_real[:]]

    def get_apo_real(self):
        if len(self.ts_real)>0:
             return[self.ts_real[0]*x for x in self.apo_real][:]
        else:
            return self.apo_real[:]

    def get_apo_imaginary(self):
        if len(self.ts_real)>0:
             return[self.ts_real[0]*x for x in self.apo_real][:]
        else:
            return self.apo_real[:]

    def calc_FWHM(self, freq_range_left=-90e3,freq_range_right=90e3):
        if len(self.spec_freq)>0:
            delta_nu=(self.spec_freq[1]-self.spec_freq[0])
            max_freq_index = min(len(self.spec_freq)-1, int(numpy.rint(len(self.spec_freq)/2+(freq_range_right)/delta_nu)-1))
            min_freq_index = max(0, int(numpy.rint(len(self.spec_freq)/2+(freq_range_left)/delta_nu)+1))
            maximum = max(self.spec_real[min_freq_index:max_freq_index])
            maxposition = numpy.argmax(self.spec_real[min_freq_index:max_freq_index])+min_freq_index
            print "Found maximum at: %s Hz Amplitude: %s" %(self.spec_freq[maxposition], maximum)
            upperindex = 0
            lowerindex = 0
            while self.spec_real[maxposition+upperindex] > maximum/2.0:
                upperindex += 1
            upperfreq = ((maximum/2.0-self.spec_real[maxposition+upperindex-1])/(self.spec_real[maxposition+upperindex]-self.spec_real[maxposition+upperindex-1])+upperindex-1)*(self.spec_freq[1]-self.spec_freq[0])
            while self.spec_real[maxposition-lowerindex] >= maximum/2.0:
                lowerindex += 1
            lowerfreq = ((maximum/2.0-self.spec_real[maxposition-lowerindex+1])/(self.spec_real[maxposition-lowerindex]-self.spec_real[maxposition-lowerindex+1])+lowerindex-1)*(self.spec_freq[1]-self.spec_freq[0])
            #self.fwhm = (lowerindex+upperindex)*(self.spec_freq[1]-self.spec_freq[0])
            self.maxfreq = self.spec_freq[maxposition]
            self.fwhm = upperfreq+lowerfreq
            print "upper frequency: %s lower frequency: %s FWHM:%sHz" %(upperfreq,lowerfreq,upperfreq+lowerfreq)
            return upperfreq+lowerfreq#(lowerindex+upperindex)*(self.spec_freq[1]-self.spec_freq[0])
    
    def calc_secMoment(self,freq_range_left=-90e3,freq_range_right=90e3):
        delta_nu=(self.spec_freq[1]-self.spec_freq[0])
        max_freq_index = min(len(self.spec_freq)-1, int(numpy.rint(len(self.spec_freq)/2+(freq_range_right)/delta_nu)-1))
        min_freq_index = max(0, int(numpy.rint(len(self.spec_freq)/2+(freq_range_left)/delta_nu)+1))
        print "Calculate mean frequency and second moment in range %s to %s" %(self.spec_freq[min_freq_index], self.spec_freq[max_freq_index])
        
        if self.calc_sum()!=True:
            self.summe=1.0
            print "Integral of spectrum is not possible and ignored!"
            norm = 1.0
            return self
        else:
            norm = integrate.simps(self.spec_real[min_freq_index:max_freq_index],self.spec_freq[min_freq_index:max_freq_index])
        
        self.meanfreq = integrate.simps( numpy.array(self.spec_freq[min_freq_index:max_freq_index])*numpy.array(self.spec_real[min_freq_index:max_freq_index]),numpy.array(self.spec_freq[min_freq_index:max_freq_index]))/norm
        self.sec_moment = integrate.simps( (numpy.array(self.spec_freq[min_freq_index:max_freq_index])-self.meanfreq)**2*numpy.array(self.spec_real[min_freq_index:max_freq_index]),numpy.array(self.spec_freq[min_freq_index:max_freq_index]))/norm
        self.skewness = integrate.simps( (numpy.array(self.spec_freq[min_freq_index:max_freq_index])-self.meanfreq)**3*numpy.array(self.spec_real[min_freq_index:max_freq_index]),numpy.array(self.spec_freq[min_freq_index:max_freq_index]))/norm/self.sec_moment**1.5
        self.kurtosis = integrate.simps( (numpy.array(self.spec_freq[min_freq_index:max_freq_index])-self.meanfreq)**4*numpy.array(self.spec_real[min_freq_index:max_freq_index]),numpy.array(self.spec_freq[min_freq_index:max_freq_index]))/norm/self.sec_moment**2-3.0#Fisher definition
        print "mean: %s" %(self.meanfreq)
        print "second moment: %s" %(self.sec_moment)
        print "skewness: %s" %(self.skewness)
        print "kurtosis: %s" %(self.kurtosis)
        return self.sec_moment

    def get_apo_spec(self,norm=False):
        if len(self.ts_real)>0 and len(self.spec_freq)>0:
            if norm:
                maximum=max(self.spec_real)/max(self.apo_spec_real)
               
                return [x*maximum for x in self.apo_spec_real][:]
            else:
                return self.apo_spec_real[:]

    """
    zu test zwecken
    def get_apo_spec_ana(self,norm=False):
        if len(self.ts_real)>0 and len(self.spec_freq)>0:
            if norm:
                maximum=max(self.spec_real)/max(self.apo_spec_ana)
               
                return [x*maximum for x in self.apo_spec_ana][:]
            else:
                return self.apo_spec_ana[:]
    """


    def get_pulse_cor_real(self):
        if len(self.spec_real)>0:
            ratio=max(self.spec_real)/max(self.pulse_cor)
            return[ratio*x for x in self.pulse_cor][:]
        else:
            return self.pulse_cor[:]

    def get_pulse_cor_imaginary(self):
        if len(self.spec_real)>0:
             ratio=max(self.spec_imaginary)/max(self.pulse_cor)
             return[ratio*x for x in self.pulse_cor][:]
        else:
            return self.pulse_cor[:]

        
        

     

    def set_phase(self,newphase):
        self.spec_real=rot_spec(self.spec_real_backup, self.spec_imaginary_backup, newphase)[0]
        self.spec_imaginary=rot_spec(self.spec_real_backup, self.spec_imaginary_backup, newphase)[1]
        
        self.ts_real2=rot_ts(self.ts_real, self.ts_imaginary, newphase)[0]
        self.ts_imaginary2=rot_ts(self.ts_real, self.ts_imaginary, newphase)[1]
        
        self.spec_phase=newphase
        
        return True


    def undo_phase(self):
        self.spec_real=self.spec_real_backup[:]
        self.spec_imaginary=self.spec_imaginary_backup[:]
        
        self.ts_real=self.ts_real_backup[:]
        self.ts_imaginary=self.ts_imaginary_backup[:]
        
        self.spec_phase=0
        
        return True
        
    
    def auto_phase(self):


        #first guess for phase:
        imagsum=numpy.trapz(self.spec_imaginary,self.spec_freq)
        realsum=numpy.trapz(self.spec_real,self.spec_freq)
        angle=numpy.arctan(-imagsum/realsum)
        print "angle wrong by: %f\n" %(angle*180.0/numpy.pi)
        if (realsum*numpy.cos(angle)-imagsum*numpy.sin(angle) < 0):
            angle+=numpy.pi
            print "Shifted by 180 degree\n"
        angle=((angle*180.0/numpy.pi)+360.0+self.spec_phase)%360
        print "phase: %f\n" %self.spec_phase
        print "Guess Angle: %f\n" %angle
        #set to guessed angle:
        self.set_phase(angle)
        print self.spec_phase

   

        
        # Phasecorrection taken from old matlab program phauto.m
        spec_real2=[None]*len(self.spec_real)
        spec_imaginary2=[None]*len(self.spec_real)
            
        sum_i=[0.0, 0.0, 0.0]
        phase=0.0
        s_phase=self.spec_phase   #0.0
        d_phase=10.0
        phase_list=[0.0, 0.0, 0.0]
        sum_i[2]=numpy.trapz(self.spec_imaginary,self.spec_freq) #sum(self.spec_imaginary)
        
        i=0
        while sum_i[0]*sum_i[1]>=0 and i<37:
            print s_phase
            i=i+1
            phase_list[0]=s_phase-d_phase
            spec_imaginary2=rot_spec(self.spec_real, self.spec_imaginary, phase_list[0])[1]
            sum_i[0]=sum(spec_imaginary2)#numpy.trapz(spec_imaginary2,self.spec_freq)#sum(spec_imaginary2)
            
            phase_list[1]=s_phase+d_phase
            spec_imaginary2=rot_spec(self.spec_real, self.spec_imaginary, phase_list[1])[1]
            sum_i[1]=sum(spec_imaginary2)#numpy.trapz(spec_imaginary2,self.spec_freq)#sum(spec_imaginary2)
            print i
            print phase_list
            print sum_i
            if sum_i[2]<1E-3:
                break
            s_phase=s_phase+d_phase*sign((sum_i[1]-sum_i[0]))
            
        i=0
        
        while abs(sum_i[2])>1e-7 and i<20:
            print "2.te schleife"
            i=i+1
            
           
           
            gewicht=abs(sum_i[0])/(abs(sum_i[0])+abs(sum_i[1]))
            phase_list[2]=phase_list[0]+((phase_list[1]-phase_list[0])*gewicht)
            spec_imaginary2=rot_spec(self.spec_real, self.spec_imaginary, phase_list[2])[1]
            sum_i[2]=sum(spec_imaginary2)   #numpy.trapz(spec_imaginary2,self.spec_freq)#s
            if sum_i[2]/sum_i[1]>0.0:
                phase_list[1]=phase_list[2]
                sum_i[1]=sum_i[2]
            else:
                phase_list[0]=phase_list[1]
                phase_list[1]=phase_list[2]
                sum_i[0]=sum_i[1]
                sum_i[1]=sum_i[2]
            print i
            print phase_list
            print sum_i

        spec_real2=rot_spec(self.spec_real, self.spec_imaginary, phase_list[2])[0]
        spec_imaginary2=rot_spec(self.spec_real, self.spec_imaginary, phase_list[2])[1]

        self.spec_real=spec_real2[:]
        self.spec_imaginary=spec_imaginary2[:]
       
        self.spec_phase=(phase_list[2]+360)%360
        self.set_phase(self.spec_phase)
        
        print self.spec_phase

        return True

        
    def get_phase(self):
        return self.spec_phase

    
        
        
        
    def calc_offset_percent(self, percent_value="10"):
        if len(self.ts_real)>0:
            self.ts_offset_percent=percent_value
            self.ts_real_offset = calculate_offset(self.ts_real, self.ts_offset_percent)
            self.ts_imaginary_offset = calculate_offset(self.ts_imaginary, self.ts_offset_percent)
            return True
        else:
            return False

    def get_offset_values(self):
        return [self.ts_real_offset,self.ts_imaginary_offset]

    def ts_offset(self):
        if len(self.ts_real)>0:
            for i in range(len(self.ts_real)):
                self.ts_real[i]=self.ts_real[i]-self.ts_real_offset
                self.ts_imaginary[i]=self.ts_imaginary[i]-self.ts_imaginary_offset
            self.ts_real_offset = calculate_offset(self.ts_real, self.ts_offset_percent)
            self.ts_imaginary_offset = calculate_offset(self.ts_imaginary, self.ts_offset_percent)
            return True
        else:
            print "Load a timesignal!"
            return False
       
            
    def find_echomax(self):
        if len(self.ts_real)>0:
            max_value=max(self.ts_real)
            min_value=min(self.ts_real)
            
            if max_value>abs(min_value):
                max_channel=self.ts_real.index(max_value)
            else:
                max_channel=self.ts_real.index(min_value)
            
            self.ts_maxchannel=int(max_channel)
            self.ts_maxchannel_time[0]=self.ts_time[self.ts_maxchannel]
            self.ts_maxchannel_real[0]=self.ts_real[self.ts_maxchannel]
            return True
        else:
            return False

    
    
    def set_echomax_value(self, shift_pos="1"):
       
        echomax=int(shift_pos)
        if echomax<len(self.ts_real) and echomax>=0:
            self.ts_maxchannel=echomax
            self.ts_maxchannel_time[0]=self.ts_time[self.ts_maxchannel]
            self.ts_maxchannel_real[0]=self.ts_real[self.ts_maxchannel]
        else:
            print "Value not allowed"

    def get_echomax_channel(self):
        return int(self.ts_maxchannel)
    
    
    def get_echomax_time(self):
        return float(self.ts_maxchannel*self.dwelltime)

            
    def ts_shift_left(self):
        if len(self.ts_real)>0:
            self.ts_real[:len(self.ts_real)-self.ts_maxchannel]=self.ts_real[self.ts_maxchannel:]
            self.ts_imaginary[:len(self.ts_real)-self.ts_maxchannel]=self.ts_imaginary[self.ts_maxchannel:]
        
            for i in xrange(self.ts_maxchannel):            
                self.ts_real[len(self.ts_real)-self.ts_maxchannel+i]=0
                self.ts_imaginary[len(self.ts_real)-self.ts_maxchannel+i]=0           
       
            return True
        else:
            return False


    def get_sum(self):
        return self.summe


    def calc_sum(self):
        if len(self.spec_freq)>0:
            self.summe=integrate.simps(self.spec_real,self.spec_freq)
            return True
        else:
            return False

        

    def auto_fft(self,off_percent=10,apo_width=5000,fdp=True,zf=10000):
        
        self.undo()
        self.set_first_dp(fdp)
        if self.calc_offset_percent(off_percent)!=True:
            print "Error with offset calculation"
            return False
        if  self.ts_offset()!=True:
            return False
        if self.find_echomax()!= True:
            return False
        
        self.ts_shift_left()
        self.apo_gauss(apo_width)
        self.do_apo()
      
        self.fft(zf)
        self.auto_phase()
        return True
            
   
    
    def open_auto_fft(self,spectrometer,filename="",off_percent=10,apo_width=5000,fdp=True,zf=10000):
        
        self.open_ts(filename,spectrometer)
        self.create_header_dict()
        self.calc_offset_percent(off_percent)
        self.ts_offset()
        self.find_echomax()
        self.ts_shift_left()
        self.apo_gauss(apo_width)
        self.do_apo()
        self.set_first_dp(fdp)
        self.fft(zf)
        self.auto_phase()
        self.save_spectrum(filename+".ts.spec.nmr")
        return True
            
   


            
    def open_ts(self, path="C:\\",spectrometer="damaris"):
        # read in data
       
        if spectrometer=="damaris":
            datas=S_openfile(path,"#")
            self.filename=path
                
            self.ts_time =datas[0][:]       # [:] damit es kopiert wird und nicht nur ein zeigher erstellt
            self.ts_real =datas[1][:]
            self.ts_imaginary = datas[3][:]
            self.ts_real_backup = datas[1][:]
            self.ts_imaginary_backup=datas[3][:]


            try:
                #read in header  "_1.info" file
                pathinfo=path[:path.rfind("_")]+"_1.info"
                self.header=S_read_header(pathinfo,"")
            except IOError, err:
                print "info file not found"
                self.header=S_read_header(path,"#")
                pass

        elif spectrometer=="hinze":
            datas=S_openfile(path,"!")
            self.filename=path

            self.ts_time =datas[0][:]       # [:] damit es kopiert wird und nicht nur ein zeigher erstellt
            self.ts_real =datas[1][:]
            self.ts_imaginary = datas[2][:]
            self.ts_real_backup = datas[1][:]
            self.ts_imaginary_backup=datas[2][:]

                        
            self.header=S_read_header(path,"!")

        elif spectrometer=="old hinze":

            datas=S_openfile(path,"hinze")
            self.filename=path

            self.ts_time =datas[0][:]       # [:] damit es kopiert wird und nicht nur ein zeiger erstellt
            self.ts_real =datas[1][:]
            self.ts_imaginary = datas[2][:]
            self.ts_real_backup = datas[1][:]
            self.ts_imaginary_backup=datas[2][:]

            self.header=S_read_header(path,"hinze")
            
        elif spectrometer=="sim":

            datas=S_openfile(path,"#")
            self.filename=path

            self.ts_time =datas[0][:]       # [:] damit es kopiert wird und nicht nur ein zeiger erstellt
            self.ts_real =datas[1][:]
            self.ts_imaginary = datas[2][:]
            self.ts_real_backup = datas[1][:]
            self.ts_imaginary_backup=datas[2][:]

            self.header=S_read_header(path,"#")

        
        else:
            print "Fehler beim Datei oeffnen"
            return False
            


        self.dwelltime = self.ts_time[1]-self.ts_time[0]
        self.aquisitionfrequency = 1.0/self.dwelltime
        self.tslength = len(self.ts_time)
        self.apo_real=[x for x in self.ts_time]
        self.ts_real2 =self.ts_real[:]
        self.ts_imaginary2 = self.ts_imaginary[:]
        self.create_header_dict()
        return True
            
          
                      
    def save_spectrum(self,path="spectrum_daten.nmr"):
        if len(self.spec_real)>0:
            
            #summe=sum(self.spec_real)
            #print summe
          
            
        
                   
            maximum=max(self.spec_real)
           
            if self.calc_sum()!=True:
                self.summe=1.0
                print "Integral of spectrum is not possible and ignored!"
                return self
            print self.summe            
            
            
            save_file=open(path,"w")
            save_file.write("!File: %s\n"%(self.filename))
            save_file.write("!Dwelltime: %s\n" %(self.dwelltime))
            save_file.write("!Aquisitionfrequency: %s\n" %(self.aquisitionfrequency))
            save_file.write("!Length: %s \n" %(self.tslength))
            save_file.write("!Echo Maximum: Kanal: %s;time %s\n"%(self.ts_maxchannel, self.ts_maxchannel*self.dwelltime))
            save_file.write("!Zero Filling: %s \n" %(self.zero_fill))
            save_file.write("!Header:\n%s"%(self.header))
            save_file.write("!Maximum Value:%s\n"%(maximum))
            save_file.write("!Integrade Value:%s\n"%(self.summe))
            if self.used_apo:
                save_file.write("!Used  Apo width:%s Hz\n"%(self.apo_width))

            if self.used_pulse_cor:
                save_file.write("!Used SE pulse correction for a Pi %s s pulse \n"%(self.pulse_length))
            
            if self.fwhm != 0:
                save_file.write("!FWHM: %.1f Hz\n"%(self.fwhm))
                save_file.write("!frequency peak: %.1f Hz\n"%(self.maxfreq))
            if self.sec_moment != 0:
                save_file.write("!second Moment: %.1f Hz^2\n"%(self.sec_moment))
                save_file.write("!mean frequency: %.1f Hz\n"%(self.meanfreq))
                save_file.write("!skewness: %.3f\n"%(self.skewness))
                save_file.write("!kurtosis: %.3f\n"%(self.kurtosis))

                
            save_file.write("!Used phase correction: %s \n"%(self.spec_phase))
            save_file.write("!Frequenz Real Imag Real_max Real_area\n")
            for i in range(len(self.spec_real)):
                save_file.write("%s %s %s %s %s\n" %(self.spec_freq[i],self.spec_real[i],self.spec_imaginary[i],(self.spec_real[i]/maximum), (self.spec_real[i]/self.summe)))                                                                                                                                              
            save_file.close()
            print "Saving the spectrum is complete!"
            return True
        else:
            return False

        
            
        
    
    def about(self):
        msg= "A DOrtmund- FFT using Python.FFT\n for NMR spectra.\n developed by A. Nowaczyk & S. Schildmann\n ----------------- 2010------------------"
        print msg
        return msg








    def do_2h_pulse_cor(self,freq_range=180e3):
        if len(self.spec_real)== 0 or self.pulse_cor_real==0 or max(self.spec_freq)< freq_range:
            return False
        else:
            min_i=0
            max_i=0
            max_search=False
            min_search=False
            for i in range(len(self.spec_freq)):
                if self.spec_freq[i]>freq_range and max_search==False:
                    max_i=i
                    max_search=True
                if self.spec_freq[i]> -1*freq_range and min_search==False:
                    min_i=i
                    min_search=True

                
            for i in range(min_i,max_i):
                #print i
                self.spec_real[i]=self.spec_real[i]/self.pulse_cor[i]
                self.spec_imaginary[i]=self.spec_imaginary[i]/self.pulse_cor[i]


           
            # alt         
            #for i in range(len(self.spec_real)):
               # self.spec_real[i]=self.spec_real[i]/self.pulse_cor[i]
               # self.spec_imaginary[i]=self.spec_imaginary[i]/self.pulse_cor[i]

            self.used_pulse_cor=True
            return True


    def pulse_correction(self,pulse_length=5e-6):
        pilen=float(pulse_length/2.0)
        self.pulse_cor=[(numpy.pi/2*(math.sin(pilen*math.sqrt((numpy.pi/(2*pilen))**2+0.25*(x*(2*numpy.pi))**2)))/(pilen*math.sqrt((numpy.pi/(2*pilen))**2+0.25*(x*(2*numpy.pi))**2)))**3 for x in self.spec_freq]
        self.pulse_length=pulse_length

        if self.header.find("Solid Echo")==-1:
            print "!!!!!!!!!! This is only for 2H Solid Echo spectra !!!!!!!!!!!"
           
        
        return True

        



    """ 
    Apodization functions:
    * exp_window and gauss_window are S/N enhancing,
    * dexp_window and traf_window are resolution enhancing
    * standard windows [hamming, hanning, bartlett, blackman, kaiser-bessel] are also available 
    self.timepoints     =   time points
            hier   self.tslength = 1
    self.aquisition_time    =   aquisition time (no. samples / sampling_rate)
            self.aquisitionfrequency = 1.0     
    line_broadening     =   line broadening factor (standard = 10 Hz)
    gaussian_multiplicator  =   Gaussian Multiplication Factor for 
            the double exponential apodization 
            function (standard = 0.3)
    """


    def do_apo(self):
        if len(self.apo_real)==0:
            return False
        else:
            for i in range(len(self.ts_real)):
                self.ts_real[i]=self.ts_real[i]*self.apo_real[i]
                self.ts_imaginary[i]=self.ts_imaginary[i]*self.apo_real[i]

            self.used_apo=True
            return True


    def apo_exp(self,width=1.0):
        
        self.apo_real=[numpy.exp(-(x)*width*2*numpy.pi) for x in self.ts_time]
        #print float(self.header_dict['tevo'])
        #self.apo_real=[numpy.exp(-(x+float(self.header_dict['tevo'])+12.1e-6)*width*2*numpy.pi) for x in self.ts_time]
        self.apo_width=width
        
      
        realdata = numpy.array(self.get_apo_real())
        imdata = numpy.zeros_like(realdata)
        data = realdata + 1j*imdata

        if self.zero_fill==0:
            points=len(self.apo_real)
        else:
            points=self.zero_fill
            
        fftdata = numpy.fft.fftshift(numpy.fft.fft(data, points))
              
        self.apo_spec_real = fftdata.real        
        return True
        
    
    def apo_gauss(self,width=1.0):
        
        self.apo_real=[numpy.exp(-0.5*(x*(width*2*numpy.pi))**2) for x in self.ts_time]
      
        #self.apo_spec_ana=[numpy.exp(-0.5*(x/(width))**2) for x in self.spec_freq]
       
    
        
        self.apo_width=width
       
        realdata = numpy.array(self.get_apo_real())
        imdata = numpy.zeros_like(realdata)
        data = realdata + 1j*imdata


        if self.zero_fill==0:
            points=len(self.apo_real)
        else:
            points=self.zero_fill
            
        fftdata = numpy.fft.fftshift(numpy.fft.fft(data, points))
              
        self.apo_spec_real = fftdata.real
        return True


    def apo_traf(self,width=1.0):
        width=width*2*numpy.pi
        self.apo_real=[numpy.exp(-(x*width))**2/(  (numpy.exp(-x*width))**3 + (numpy.exp(-self.ts_time[len(self.ts_time)-1]*width))**3 ) for x in self.ts_time]
        #self.apo_real=[numpy.exp((x+0.000425345+12.1e-6)*width) for x in self.ts_time]
      
        self.apo_width=width

        realdata = numpy.array(self.get_apo_real())
        imdata = numpy.zeros_like(realdata)
        data = realdata + 1j*imdata
        
        if self.zero_fill==0:
            points=len(self.apo_real)
        else:
            points=self.zero_fill
            
        fftdata = numpy.fft.fftshift(numpy.fft.fft(data, points))
           
        self.apo_spec_real = fftdata.real

        return True
        
    def apo_hann(self):
        self.apo_real=[0.5*(1+numpy.cos(numpy.pi*x/self.ts_time[-1])) for x in self.ts_time]
      
        realdata = numpy.array(self.get_apo_real())
        imdata = numpy.zeros_like(realdata)
        data = realdata + 1j*imdata
        
        if self.zero_fill==0:
            points=len(self.apo_real)
        else:
            points=self.zero_fill
            
        fftdata = numpy.fft.fftshift(numpy.fft.fft(data, points))
           
        self.apo_spec_real = fftdata.real

        return True



  
    
    """
    def exp_window(self, line_broadening=10, show=False):
        
        apod = numpy.exp(-self.tslength*line_broadening)

        print
        return
    
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show:
                    return self.the_result
        return self
    
    def gauss_window(self, line_broadening=10, show=0):
        apod = N.exp(-(self.timepoints*line_broadening)**2)
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show == 1 :
            return self.the_result
        return self
    
    def dexp_window(self, line_broadening=10, gaussian_multiplicator=0.3, show=0):
        apod = N.exp(-(self.timepoints*line_broadening - gaussian_multiplicator*self.aquisition_time)**2)
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod 
        if show == 1:
            return self.the_result
        return self
    
    def traf_window(self, line_broadening=10, show=0):
        apod = (N.exp(-self.timepoints*line_broadening))**2 / ( (N.exp(-self.timepoints*line_broadening))**3 
            + (N.exp(-self.aquisition_time*line_broadening))**3  )
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show == 1:
            return self.the_result
        return self
    
    def hanning_window(self, show=0):
        apod = N.hanning(self.data_points)
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show == 1:
            return self.the_result
        return self
    
    def hamming_window(self, show=0):
        apod = N.hamming(self.data_points)
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show == 1:
            return self.the_result
        return self
    
    def blackman_window(self, show=0):
        apod = N.blackman(self.data_points)
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show == 1:
            return self.the_result
        return self
    
    def bartlett_window(self, show=0):
        apod = N.bartlett(self.data_points)
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show == 1:
            return self.the_result
        return self
    
    def kaiser_window(self, beta=4, show=0, use_scipy=None):
        if use_scipy == None:
            # modified Bessel function of zero kind order from somewhere
            def I_0(x):
                i0=0
                fac = lambda n:reduce(lambda a,b:a*(b+1),range(n),1)
                for n in range(20):
                    i0 += ((x/2.0)**n/(fac(n)))**2
                return i0
        
            t = N.arange(self.data_points, type=N.Float) - self.data_points/2.0
            T = self.data_points
            # this is the window function array
            apod = I_0(beta*N.sqrt(1-(2*t/T)**2))/I_0(beta)
        else:
            # alternative method using scipy
            import scipy 
            apod=scipy.kaiser(self.data_points, beta)
        
        for i in range(2):
            self.the_result.y[i] = self.the_result.y[i]*apod
        if show == 1:
            return self.the_result
        return self
    """
  


