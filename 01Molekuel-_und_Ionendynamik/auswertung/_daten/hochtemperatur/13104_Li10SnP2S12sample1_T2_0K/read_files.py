
import os
import glob
import string



def read_dir():   # update self.file and self.directory
    contents=os.listdir('.') #contents of the current directory
    files =[]
    directory=[]
    for i in contents:
        if os.path.isfile(i) == True:
            files.append(i)
        elif os.path.isdir(i) == True :
            directory.append(i)

    print "files in directory"
    print files

    return files



def get_length(data_file):  # return a int
    file_length=-1
    test_string="test"
    while test_string != "":
        test_string=data_file.readline()
        file_length=file_length+1
            
    #print "File has %s lines."%(file_length)
    data_file.seek(0) # jump to the beginning of the file


    
    return file_length
        

def get_header(data_file,headerchar): # returns a string
    if headerchar=="":
        # searches for first free line
        h_length=-1
        testword="test"
        header=[]
        while testword!="":
            testword = data_file.readline()          
            h_length=h_length+1


    elif headerchar=="hinze":
        h_length=-1
        testword="test"
        header=[]
        while testword!="-----":
            #print testword
            teststring = data_file.readline()
            testword=teststring[0:5]            
            h_length=h_length+1
        h_length=h_length+1

    elif headerchar=="simpson":
        h_length=-1
        testword="test"
        header=[]
        while testword!="DATA":
            #print testword
            teststring = data_file.readline()
            testword=teststring[0:4]            
            h_length=h_length+1
        h_length=h_length+1


    else:
        # searches for lines beginning with the headerchar
        h_length=-1
        headerword=headerchar
        header=[]
        while headerword==headerchar:
            headstring = data_file.readline()
            headerword=headstring[0]
            h_length=h_length+1    
             
    # print "The header has %s lines."%(h_length)
    data_file.seek(0) # jump to the beginning of the file
   
    for k in range(h_length):
        line=data_file.readline()
        if headerchar!="" and headerchar!="hinze" and headerchar!="simpson":
            #print headerchar
            # delete the first letter in line
            line=line[1:len(line)]
            #print line
        line.lstrip()
        header.append(line)    #=header+ line
    data_file.seek(0)
   
    return header





def get_col_num(data_file,header_length=0):
    # returns the number of columns in the data file
    num=0
    for k in range(header_length):
        line=data_file.readline()
    
    line=data_file.readline()
    parts=line.split()
    num=len(parts)
    data_file.seek(0)

    #print "The dataset has %s columns."%(num)
    return num


def get_col_name(header,num):
    if header==[]:
        print "Sorry, no header infomations."
        return []
    elif header[len(header)-1][0:5]=="-----":
        print "Sorry, no col names"
    elif header[len(header)-1][0:4]=="DATA":
        print "Sorry, no col names"
        
        return []
    else:
      
        names=[]
        parts=header[len(header)-1].split()

        for n in range(len(parts)):
            names.append(str(parts[n]))
        if num==len(names):
            return names
        else:
            names=[]
            print "Column nummber and Header number are incorrect"
            return names
            


def read_data(data_file,col_number,file_length,h_length):

    dataset=[None]*col_number
    for i in range(col_number):
        dataset[i]=[None]*(file_length-h_length)
    # hat die form : dataset=[[],[],[],.....] 
  
    # jump over header
    for j in range(h_length):
        line=data_file.readline()

    
    # reading data lines    
    for k in range(file_length-h_length):
        line=data_file.readline()
        parts=line.split()
        
        # for .ts signals
        #----------------------------
        for j in range(col_number):
            if parts[j]=="nan":
                parts[j]="0.0"
            # replace all commas with dots
            if "," in parts[j]:
                parts[j]=parts[j].replace(",",".")
    
        #-----------
        
       
        
        for i in range(col_number):
            try:
                dataset[i][k]=(float(parts[i]))
            except:
                print "dataset has a worng format! No float nummbers!"
                return dataset
            #print  "col nummber : %s" %i
            #print parts[i]
            #dataset[i].append(float(parts[i]))
            #print dataset[i]
            #print dataset
           
        #if k==6:
        #    print dataset
        #    blap
            
    return dataset
        




def S_openfile(filename="",header_char="!",debug=False):
    try:
        data_file=open(filename,"r")
        print "\n\nOpen data_file %s and create list with the data!!\n" %(filename)
    except IOError, error:
        print'Error opening file\n' + str(error)
        return
        
    except UnicodeDecodeError, error:
        print 'Error! file not found\n' + str(error)
        return
       

        #print "Error! File not found!"
        #   return 
     
    length=get_length(data_file)
    
    if header_char=="simpson":
        length=length-1
    
    if debug:
        print "File has %s lines.\n"%length

    header_list=get_header(data_file,header_char)
    if debug:
        print "Header information (char=%s):\n"%header_char
        print "%s \n"%header_list


    col_num=get_col_num(data_file,len(header_list))
    if debug:
        print "Number of columns: %s\n"%col_num

    data_names=get_col_name(header_list,col_num)
    if debug:
        print "Found column names: %s \n"%data_names
    
        if data_names !=[]:
            for i in range(col_num):
                print "Name of Col %s :%s"%(i,data_names[i])
    
    datas=read_data(data_file,col_num,length,len(header_list))
    data_file.close()
    
    return datas



def S_read_header(filename="",header_char=""):
    try:
        data_file=open(filename,"r")
        #print "\n\nOpen data_file %s and read out the header!!\n" %(filename) 
    except IOError, error:
        print'Error opening file\n' + str(error)
        return ""
        
    except UnicodeDecodeError, error:
        print 'Error! file not found\n' + str(error)
        return ""
    header_str=""
    header_list=get_header(data_file,header_char)
    
    for line in header_list:
        line.lstrip()
        header_str=header_str+"!"+line
        
    data_file.close()
    #print header_list
    return header_str
     
    

        
