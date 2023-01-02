import re
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.integrate as sci
import sys

tags=["\"ENG\"", "\"USA\"", "\"FRA\"", "\"RAJ\"", "\"CAN\"", "\"AST\"", "\"SAF\"", "\"NZL\"", "\"SOV\"", "\"GER\"", "\"ITA\"", "\"HUN\"", "\"ROM\"", "\"BUL\"", "\"VIC\"", "\"JAP\"", "\"MAN\"", "\"FIN\"", "\"SLO\"", "\"SPR\"", "\"LAT\"", "\"YUG\"", "\"GRE\"", "\"ALB\"", "\"NOR\"", "\"POR\"", "\"IRE\"", "\"ETH\"", "\"IRQ\"", "\"SIA\"", "\"VEN\"", "\"MON\"", "\"TAN\"", "\"PAR\"", "\"PRC\"", "\"BEL\"", "\"INS\"", "\"AUS\"", "\"POL\"", "\"CZE\"", "\"HOL\""]
majors=["\"GER\"","\"SOV\"","\"ENG\"","\"JAP\"","\"ITA\"","\"USA\""]
alliedminors=["\"RAJ\"", "\"CAN\"", "\"AST\"", "\"SAF\""]
axisminors=["\"HUN\"", "\"ROM\"", "\"BUL\"","\"SPR\""]
minors=alliedminors+axisminors


#Sets which countries to analyze
inputtag=majors
#Sets "save" folder path
absolute_path = os.path.dirname(__file__)
relative_path = "save\\"
folderpath = os.path.join(absolute_path, relative_path)
nautosaves=len([entry for entry in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath, entry))])


tagic=[ [0]*len(inputtag) for i in range(nautosaves+1)] #monthly IC in columns
tagic[0]=inputtag  #tags


def listidx(L, obj):
    if obj in L:
        return L.index(obj)
    return -1

def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

def print_progress_bar(index, total, label):
    n_bar = 50  
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()

def print2d(values):
    lines = []
    for row in values:
        lines.append(' '.join(str(x) for x in row))
    print('\n'.join(lines))       


def monthlyic(fullpath,row): #ic calculator
    with open(fullpath, 'r', encoding="utf8") as fp:
        flag_found=0
        content = fp.read()
        indices_object = re.finditer(pattern='military_lines={', string=content) #looks for military factory production lines
        indices = [index.start() for index in indices_object]
        countryic=[]
        icsum=0
        for x in indices:
                idx=content.find('speed=', x, x+200 )  #Literally the line's daily IC
                idx3=content.find('production_licenses', x-1000, x ) #Is present at the first line for every country
                idx4=content.find('owned_license={', x-1000,x) #same as before, check needed if country has many licenses
                if idx3!=-1 or idx4!=-1:
                    countryic.append(icsum)
                    for jj in tagic[0]:
                        my_regex = r"sender="+jj+r"\n\t\t\t\t\treceiver="+jj+r"\n\t\t\t\t\tconvoys_owner="+jj #Finds the country using the factories. Might break if no resources and units in country
                        country=re.search(my_regex, content[x-50000:x])
                        my_regex2 = r"owner="+jj
                        country2=re.search(my_regex2, content[x-1000:x]) #convoy owner
                        if country or country2:
                            countryic.append(jj)
                            flag_found=1
                    if flag_found!=1:
                        countryic.append("UNKOWN")
                    icsum=0
                    flag_found=0
                if idx!=-1:
                    idx2=content.find('\n', idx, idx+30) #registers the line's daily IC
                    icsum=icsum+float(content[idx+6:idx2])
        countryic.pop(0)
        for count,value in enumerate(tagic[0]): #build output table with ICs
            position=listidx(countryic,value)
            if position!=-1:
                tagic[row][count]=round(countryic[position+1],3)
            else:
                tagic[row][count]=0

#calculates monthlyic for every file in /save. Edit this if you haven't saved your files as save1, save2,...
for i in range(nautosaves):  
    filename=folderpath+"save"+str(i+1)+".hoi4"
    print_progress_bar(i+1, nautosaves, "Wait...")
    monthlyic(filename,i+1)


#apply moving average for instant ic and integrates for cumulative ic
dat = np.array(tagic[1:])*30
for i in range(len(inputtag)):
    dat[1:nautosaves-1,i]=moving_avg(dat[:,i],3)
result = sci.cumtrapz(dat, axis=0, dx=1)
dat = np.around(dat, decimals=3)
result = np.around(result, decimals=3)

#saves results on txt files
with open('matrix.txt', 'w') as testfile:
    for row in dat:
        testfile.write(','.join([str(a) for a in row]) + '\n')
with open('matrixcum.txt', 'w') as testfile:
    for row in result:
        testfile.write(','.join([str(a) for a in row]) + '\n')


x=range(1,nautosaves)
x_ticks = [0, 12, 24, 36, 48, 60, 72]
x_labels = ['1936', '1937', '1938', '1939', '1940', '1941', '1942']
#plots results
plt.figure("Cumulative Produced IC")
plt.title("Cumulative Produced IC") 
plt.xlabel("Years") 
plt.ylabel("Total Produced IC") 
plt.plot(x,result) 
plt.xticks(x_ticks, x_labels)
plt.legend(tagic[0])
plt.grid( linestyle = '--', linewidth = 0.5)


x=range(0,nautosaves)
plt.figure("Monthly Produced IC")
plt.title("Monthly Produced IC") 
plt.xlabel("Year") 
plt.ylabel("Monthly Produced IC") 
plt.plot(x,dat) 
plt.grid( linestyle = '--', linewidth = 0.5)
plt.xticks(x_ticks, x_labels)
plt.legend(tagic[0])

plt.show()

