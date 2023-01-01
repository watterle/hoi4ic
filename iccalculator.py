import re
import numpy as np
import matplotlib.pyplot as plt


majors=["\"GER\"","\"SOV\"","\"ENG\"","\"JAP\"","\"ITA\"","\"USA\"","\"FRA\""]
alliedminors=["\"RAJ\"", "\"CAN\"", "\"AST\"", "\"SAF\""]
axisminors=["\"HUN\"", "\"ROM\"", "\"BUL\"","\"SLO\""]
minors=alliedminors+axisminors

inputtag=["\"GER\"","\"SOV\""]

tags=["\"ENG\"", "\"USA\"", "\"FRA\"", "\"RAJ\"", "\"CAN\"", "\"AST\"", "\"SAF\"", "\"NZL\"", "\"SOV\"", "\"GER\"", "\"ITA\"", "\"HUN\"", "\"ROM\"", "\"BUL\"", "\"VIC\"", "\"JAP\"", "\"MAN\"", "\"FIN\"", "\"SLO\"", "\"SPR\"", "\"LAT\"", "\"YUG\"", "\"GRE\"", "\"ALB\"", "\"NOR\"", "\"POR\"", "\"IRE\"", "\"ETH\"", "\"IRQ\"", "\"SIA\"", "\"VEN\"", "\"MON\"", "\"TAN\"", "\"PAR\"", "\"PRC\"", "\"BEL\"", "\"INS\"", "\"AUS\"", "\"POL\"", "\"CZE\"", "\"HOL\""]
folderpath="C:\\Users\\cero\\Documents\\Paradox Interactive\\savefilecheck\\save\\"
nautosaves=73 #- number of saves
tagic=[ [0]*len(inputtag) for i in range(nautosaves+1)] #monthly IC in columns, 1st row Tags
tagic[0]=inputtag


def listidx(L, obj):
    if obj in L:
        return L.index(obj)
    return -1

def print2d(values):
    lines = []
    for row in values:
        lines.append(' '.join(str(x) for x in row))
    print('\n'.join(lines))       


def monthlyic(fullpath,row):
    with open(fullpath, 'r', encoding="utf8") as fp:
        flag_found=0
        content = fp.read()
        indices_object = re.finditer(pattern='military_lines={', string=content)
        indices = [index.start() for index in indices_object]
        countryic=[]
        icsum=0
        for x in indices:
                idx=content.find('speed=', x, x+200 )
                idx3=content.find('production_licenses', x-1000, x )
                idx4=content.find('owned_license={', x-1000,x)
                if idx3!=-1 or idx4!=-1:
                    countryic.append(icsum)
                    for jj in tagic[0]:
                        my_regex = r"sender="+jj+r"\n\t\t\t\t\treceiver="+jj+r"\n\t\t\t\t\tconvoys_owner="+jj
                        country=re.search(my_regex, content[x-50000:x])
                        my_regex2 = r"owner="+jj
                        country2=re.search(my_regex2, content[x-1000:x])
                        if country or country2:
                            countryic.append(jj)
                            flag_found=1
                    if flag_found!=1:
                        countryic.append("UNKOWN")
                    icsum=0
                    flag_found=0
                if idx!=-1:
                    idx2=content.find('\n', idx, idx+30)
                    icsum=icsum+float(content[idx+6:idx2])
        countryic.pop(0)
        #print(countryic)
        for count,value in enumerate(tagic[0]):
            position=listidx(countryic,value)
            if position!=-1:
                tagic[row][count]=round(countryic[position+1],3)
            else:
                tagic[row][count]=0


#test=[49,50];
#for i in test:
for i in range(nautosaves):
    filename=folderpath+"save"+str(i+1)+".hoi4"
    print(filename)
    monthlyic(filename,i+1)



#print2d(np.array(tagic))
dat = np.array(tagic[1:])*30
dat = np.around(dat, decimals=3)
result = np.cumsum(dat, axis=0)
result = np.around(result, decimals=3)

with open('matrix.txt', 'w') as testfile:
    for row in dat:
        testfile.write(','.join([str(a) for a in row]) + '\n')
with open('matrixcum.txt', 'w') as testfile:
    for row in result:
        testfile.write(','.join([str(a) for a in row]) + '\n')



plt.figure("Cumulative IC")
plt.title("Cumulative IC") 
plt.xlabel("Months") 
plt.ylabel("Total IC") 
plt.plot(result) 
plt.legend(tagic[0])
xcoords = [12, 24, 36, 48, 60, 72]
for xc in xcoords:
    plt.axvline(x=xc, color='k', ls=':', linewidth=1)



plt.figure("Monthly IC")
plt.title("Monthly IC") 
plt.xlabel("Months") 
plt.ylabel("Monthly IC") 
plt.plot(dat) 
plt.legend(tagic[0])
xcoords = [12, 24, 36, 48, 60, 72]
for xc in xcoords:
    plt.axvline(x=xc, color='k', ls=':', linewidth=1)


plt.show()

