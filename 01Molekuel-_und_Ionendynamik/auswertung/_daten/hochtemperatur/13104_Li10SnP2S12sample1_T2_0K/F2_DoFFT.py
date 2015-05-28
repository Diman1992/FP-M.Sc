
from DoFFT import *  # die Dortmunder FFT
import pylab as plt  # zum plotten der Daten
import numpy as np
import shutil
np.set_printoptions(precision = 4, linewidth = 150)

# setzt manuell den Kanal der Verschiebung
echo_max_channel = 29
#berechnet den offsert Wert mit xx prozent des hinteren Zeitsignals
ts_offset_percent = 50
# berechnet eine gauss apodisations kurve fuer das Zeitsignal (in Hz)
apo_width = 300
#Anzahl der Datenpunkte fuer die FFT
zero_fill = 10000
#phasenanpassung des Spektrums (0. Ordnung)
phase = 43
#Maximum der Satelliten im ersten Spek
freq_eval = 5500
#Breite ueber die die Satelliten gemittelt werden sollen in Hz
freq_eval_width = 1400
#offresonanz; Position der Zentrallinie in Hz im Spektrum
off_res = -0
#Breite ueber die die zentrallinie gemittelt werden soll in Hz
freq_eval_central_width = 1200

#ob Spektren gespeichert werden sollen
save_spec = False
#echo Zeitpunkt an dem das Zeitsignal ausgelesen wird
echo_val = 0e-6
#Breite ueber die gemittelt werden soll
echo_width = 3e-6


#amplituden links und rechts, auf die normiert wird; fig 4
amp_left = 1.00*1.
amp_right = 1.00*1.
#offsets links und rechts, die abgezogen werden; fig 4
off_left = -0
off_right = 0


def read_dir(string = "*", subdir='.'):   # update self.file and self.directory
    contents=os.listdir(subdir) #contents of the current directory
    files =[]
    directory=[]
    for i in contents:
        i = "./"+i
        if os.path.isfile(i) == True:
            if i.endswith(string):
                files.append(i)
        elif os.path.isdir(i) == True :
            directory.append(i)

    print "files in directory"
    print "Number of files: %s" %(len(files))
    print files
    return files

header=read_dir(".info")[0]
dat_file=read_dir(".dat.nmr")[0]
ts_files=read_dir(".ts")
print ts_files
ts_files=sorted(ts_files, key=lambda m_file: int(m_file.split("_")[-1][:-3]))
print ts_files

tm_values=[]
m_file1=open(dat_file,"r")
test_string = m_file1.readline()
while test_string != "":
    tm_values.append([float(x.strip()) for x in test_string.split()])
    test_string = m_file1.readline()
tm_values=np.array(tm_values)
m_file1.close()

print tm_values

data_values=[]

fig1=plt.figure(1)
fig2=plt.figure(2)

for filename in ts_files[:]:
    # name der Datei im gleichen Verzeichnis
    #filename="DMS_O2_F2_325K_10571_1.ts"
    
    
    # classe DoFFT() aufrufen
    meine_fft=DoFFT()
    
    # classen funktionen werden per zugewiesener classenanem.xx(Parameter) aufgerufen
    # zum Beispiel die about-funktion, die in der Konsole die Version ausgibt
    
    meine_fft.about()
    
    # oeffnet die Datei mit dem Zeitsignal
    meine_fft.open_ts(filename)
    
    #berechnet den offsert Wert mit xx prozent des hinteren Zeitsignals
    meine_fft.calc_offset_percent(ts_offset_percent)
    
    # zieht des Offset wert ab
    meine_fft.ts_offset()
    
    # setzt manuel den Kanal der verschiebung
    meine_fft.set_echomax_value(echo_max_channel)
    
    # gibt von der gefundenen Stelle den Kanal
    print "Echomax Channel f. FFT: %s" %(meine_fft.get_echomax_channel())
    # sowie die zeit aus
    print "Echomax Time f. FFT: %s" %(meine_fft.get_echomax_time())
    
    # verschiebt beide (Real u. Imag.) Zeitsignale um den vorher ausgerechntet wert
    meine_fft.ts_shift_left()
    
    
    # berechnet eine gauss apodisations kurve  fuer das Zeitsignal
    meine_fft.apo_gauss(apo_width)
    
    # apodisiert das Zeitsignal
    meine_fft.do_apo()
    
    # beruesichtig bei der FFT die Halbierung der ersten Datenpunktes
    meine_fft.set_first_dp(True)
    
    # fueht die eigentlich FFT aus   mit 12000 datenpunkten aus (zerofilling)
    zerofilling=zero_fill
    meine_fft.fft(zerofilling)
    
    # automatische phasenanpassung des Spektrums (0. Ordnung)
    #meine_fft.auto_phase()
    meine_fft.set_phase(phase)
    
    
    
    #----------------------------
    # nur fuers zeichnen
    #----------------------------
    
    # gibt die zeitachse aus 
    zeit=meine_fft.get_time()
    
    #gibt die Zeitsignale  real: ts[0]  imag ts[1]
    ts=np.array([meine_fft.ts_real2,meine_fft.ts_imaginary2])
    
    # gibt die apo funktion aus
    apo=meine_fft.get_apo_real()
    
    # zeichnet  Real und Imag. Zeitsignale sowie Apo funktion
    plt.figure(1)
    plt.plot(zeit,ts[0],"b-")
    plt.plot(zeit,ts[1],"r-")
    plt.plot(zeit,apo,"g--")
    #----------------------------
    
    #gibt die Frequenz achse aus
    freq=meine_fft.get_freq()
    
    #gibt  das Spektrum aus :  real  xx[0]  imag. xx [1] 
    spectrum=np.array(meine_fft.get_spec())
    
    # gibt die FFT der apo funktion wieder  True : normiert aus real spektrum
    meine_fft.apo_gauss(apo_width)
    apo_spectrum =meine_fft.get_apo_spec(True)
    
    # zeichnet  Real und Imag. Spektren sowie Apo funktion
    plt.figure(2)
    plt.plot(freq,spectrum[0],"b-")
    plt.plot(freq,spectrum[1],"r-")
    plt.plot(freq,apo_spectrum,"g--")
    #----------------------------
    #speichert das Spektrum sowie header inforationen in einer neuen Datei
    if save_spec:
        filename_spec=filename+".ts.spec.nmr"
        meine_fft.save_spectrum(filename_spec)
    #----------------------------
    #auslesen der Frequenzwerte und der Amplituden
    #Zeitsignal:
    ts_indices = np.searchsorted(zeit,[echo_val-echo_width/2.0,echo_val+echo_width/2.0])
    ts_mean_val=np.mean(ts[:,ts_indices[0]:ts_indices[1]],axis=-1)
    ts_std_val=np.std(ts[:,ts_indices[0]:ts_indices[1]],axis=-1)
    #Spektrum:
    freq_indices = np.searchsorted(freq,[-freq_eval+off_res-freq_eval_width/2.0,-freq_eval+off_res+freq_eval_width/2.0,freq_eval+off_res-freq_eval_width/2.0,freq_eval+off_res+freq_eval_width/2.0,-freq_eval_central_width/2,freq_eval_central_width/2])
    spec_mean_val_left=np.mean(spectrum[:,freq_indices[0]:freq_indices[1]],axis=-1)
    spec_mean_val_right=np.mean(spectrum[:,freq_indices[2]:freq_indices[3]],axis=-1)
    spec_mean_val=np.mean(np.hstack([spectrum[:,freq_indices[0]:freq_indices[1]],spectrum[:,freq_indices[2]:freq_indices[3]]]),axis=-1)
    spec_mean_val_central=np.mean(spectrum[:,freq_indices[4]:freq_indices[5]],axis=-1)
    spec_std_val_left=np.std(spectrum[:,freq_indices[0]:freq_indices[1]],axis=-1)
    spec_std_val_right=np.std(spectrum[:,freq_indices[2]:freq_indices[3]],axis=-1)
    spec_std_val=np.std(np.hstack([spectrum[:,freq_indices[0]:freq_indices[1]],spectrum[:,freq_indices[2]:freq_indices[3]]]),axis=-1)
    spec_std_val_central=np.std(spectrum[:,freq_indices[4]:freq_indices[5]],axis=-1)
    data_values.append(np.hstack([np.hstack(zip(ts_mean_val,ts_std_val)),np.hstack(zip(spec_mean_val,spec_std_val)),np.hstack(zip(spec_mean_val_left,spec_std_val_left)),np.hstack(zip(spec_mean_val_right,spec_std_val_right)),np.hstack(zip(spec_mean_val_central,spec_std_val_central))]))
    #~ print ts
    #~ print np.shape(ts)
    #~ print ts_mean_val
    #~ print ts_std_val
    #~ print spec_mean_val
    #~ print spec_std_val
    #~ print data_values[-1]
data_values=np.array(data_values)

#Zeichen der Ergebnisse
fig3,ax1=plt.subplots()
ax1.set_ylabel("magnitude spectrum", color="b")
plt.plot(tm_values[:len(data_values),0],data_values[:,4],"bo", label="spectrum real")
plt.plot(tm_values[:len(data_values),0],data_values[:,6],"rs", label="spectrum imag")
for tl in ax1.get_yticklabels():
    tl.set_color('b')
plt.legend()
plt.semilogx()
ax2=ax1.twinx()
ax2.set_ylabel("magnitude timesignal", color="g")
plt.plot(tm_values[:len(data_values),0],data_values[:,0],"g^", label="timesignal real")
plt.plot(tm_values[:len(data_values),0],data_values[:,2],"mv", label="timesignal imag")
for tl in ax2.get_yticklabels():
    tl.set_color('g')
plt.legend(loc='center right')
plt.semilogx()
#Zeichen der Ergebnisse fuer linke und rechte Seite
fig4=plt.figure(4)
#~ plt.plot(tm_values[:len(data_values),0],data_values[:,8]/3060.,"bo", label="spectrum real left")
#~ plt.plot(tm_values[:len(data_values),0],data_values[:,10]/9550.,"rs", label="spectrum real right")
plt.plot(tm_values[:len(data_values),0],(data_values[:,8]-off_left)/amp_left,"bo", label="spectrum real left")
plt.plot(tm_values[:len(data_values),0],(data_values[:,12]-off_right)/amp_right,"rs", label="spectrum real right")
plt.plot(tm_values[:len(data_values),0],(data_values[:,16]),"bs", label="spectrum real central")
plt.legend()
plt.semilogx()
plt.show()
#Speichern der Ergebnisse
#spalten: tm, ts re, s(ts re), ts im, s(ts im), spec re, s(spec re), im re, s(im re), T
m_file_2=open(dat_file[:-8]+"_spec.dat.nmr","w")
for i in range(len(data_values)):
    m_file_2.write("%s %s %s %s %s %s %s %s %s %s\n" %(tm_values[i,0], data_values[i,0], data_values[i,1], data_values[i,2], data_values[i,3], data_values[i,4], data_values[i,5], data_values[i,6], data_values[i,7], tm_values[i,9]))
m_file_2.close()
#Kopiere den Header fuer einfache Auswertung mit Origin
shutil.copy2(header, header[:-7]+"_spec_1.info")
m_file_3=open(header[:-7]+"_spec_1.info","a")
m_file_3.write("echomax for FFT: %s\n" %(echo_max_channel))
m_file_3.write("ts_offset_percent: %s\n" %(ts_offset_percent))
m_file_3.write("apo_width in Hz: %s\n" %(apo_width))
m_file_3.write("Zero_filling: %s\n" %(zero_fill))
m_file_3.write("Phase correction: %s\n" %(phase))
m_file_3.write("Timesignal readout: %s\n" %(echo_val))
m_file_3.write("Timesignal readout width: %s\n" %(echo_width))
m_file_3.write("Spectrum readout: %s\n" %(freq_eval))
m_file_3.write("Spectrum readout width: %s\n" %(freq_eval_width))
m_file_3.write("Spectrum Offresonanz: %s\n" %(off_res))
m_file_3.write("Spectrum central readout: %s\n" %(freq_eval_central_width))
m_file_3.close()
#zusaetzliche datei mit daten aus spektren links und rechts: 
#spalten: tm, specleft re, specleft im, specright re, specright im, speccentral re, speccentral im, T 
m_file_4=open(dat_file[:-8]+"_specleftright.dat.nmr","w")
for i in range(len(data_values)):
    m_file_4.write("%s %s %s %s %s %s %s %s\n" %(tm_values[i,0], data_values[i,8], data_values[i,10], data_values[i,12], data_values[i,14], tm_values[i,9], data_values[i,16], data_values[i,18]))
m_file_4.close()
print "All done!"
