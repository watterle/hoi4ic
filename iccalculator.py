import re
import numpy as np
import os
import scipy.integrate as sci
import sys
import tkinter as tk
from tkinter import filedialog 
from tkinter import ttk 
import threading
import matplotlib.pyplot as plt

tags=["\"ENG\"", "\"USA\"", "\"FRA\"", "\"RAJ\"", "\"MAN\"", "\"EFR\"", "\"CAN\"", "\"AST\"", "\"CHI\"", "\"RCC\"", "\"SAF\"","\"PER\"", "\"NZL\"", "\"SOV\"", "\"GER\"", "\"ITA\"", "\"HUN\"", "\"ROM\"", "\"BUL\"", "\"VIC\"", "\"JAP\"", "\"MAN\"", "\"FIN\"", "\"SLO\"", "\"SPR\"", "\"LAT\"", "\"YUG\"", "\"GRE\"", "\"ALB\"", "\"NOR\"", "\"POR\"", "\"IRE\"", "\"ETH\"", "\"IRQ\"", "\"SIA\"", "\"VEN\"", "\"MON\"", "\"TAN\"", "\"PAR\"", "\"PRC\"", "\"BEL\"", "\"INS\"", "\"AUS\"", "\"POL\"", "\"CZE\"", "\"HOL\""]
majors=["\"GER\"","\"SOV\"","\"ENG\"","\"JAP\"","\"USA\"","\"ITA\"","\"FRA\""]
alliedminors=["\"RAJ\"", "\"CAN\"", "\"AST\"", "\"SAF\"", "\"NZL\"", "\"POL\"", "\"CHI\""]
axisminors=["\"HUN\"", "\"ROM\"", "\"BUL\"","\"SPR\"","\"SLO\"","\"MAN\"","\"RCC\""]
minors=alliedminors+axisminors
all=minors+majors
loop = {"majors" : majors,
        "allies" : alliedminors,
        "axis" : axisminors,
        "faction" : all
        }

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

def rindex(lst, value):
    return len(lst) - lst[::-1].index(value) - 1

def monthlyic(fullpath,row,tagic,navtagic): #ic calculator
    with open(fullpath, 'r', encoding="utf8") as fp:
        flag_found=0
        content = fp.read()
        custom_regex=r'military_lines={|naval_lines={|railway_gun_lines|ship_refit_lines={'
        indices_object = re.finditer(custom_regex, string=content) #looks for military factory production lines
        indices = [index.start() for index in indices_object]
        countryic=[]
        navcountryic=[]
        icsum=0
        navicsum=0
        for x in indices:
                idx=content.find('speed=', x, x+400 )  #Literally the line's daily IC
                idx3=content.find('production_licenses', x-500, x ) #Is present at the first line for every country
                idx4=content.find('owned_license={', x-500,x) #same as before, check needed if country has many licenses
                idx5=content.find('naval_lines={', x-20, x+20 )
                idx6=content.find('ship_refit_lines={', x-20, x+20 )
                if (idx3!=-1 or idx4!=-1):
                    countryic.append(icsum)
                    navcountryic.append(navicsum)
                    for jj in tags:
                        my_regex = r"sender="+jj+r"\n\t\t\t\t\treceiver="+jj+r"\n\t\t\t\t\tconvoys_owner="+jj #Finds the country using the factories. Might break if no resources and units in country
                        country=re.search(my_regex, content[x-50000:x])
                        my_regex2 = r"owner="+jj
                        country2=re.search(my_regex2, content[x-1000:x]) #convoy owner
                        if country or country2 and idx5==-1:
                            if jj=="\"CZE\"": 
                                jj="\"SLO\""
                            countryic.append(jj)
                            navcountryic.append(jj)
                            flag_found=1
                    if flag_found!=1 :
                        countryic.append("UNKNOWN")
                        navcountryic.append("UNKNOWN")
                    icsum=0
                    navicsum=0
                    flag_found=0
                if idx!=-1:
                    idx2=content.find('\n', idx, idx+30) #registers the line's daily IC
                    if idx5==-1 and idx6==-1:
                        icsum=icsum+float(content[idx+6:idx2])
                    else:
                        navicsum=navicsum+float(content[idx+6:idx2])
        for country in tagic[0]:
            if country not in countryic:
                countryic.append(country)
                countryic.append(0)
            if country not in navcountryic:
                navcountryic.append(country)
                navcountryic.append(0)
        countryic.pop(0)
        navcountryic.pop(0)
        #print(countryic)
        for count,value in enumerate(tagic[0]): #build output table with ICs
            position=rindex(countryic,value)
            if (position!=-1) and ((position+1)<len(countryic)):
                tagic[row][count]=round(countryic[position+1],3)
            else:
                tagic[row][count]=0
        for count,value in enumerate(navtagic[0]): #build output table with ICs
            position=rindex(navcountryic,value)
            if position!=-1:
                if (position+1)<len(navcountryic):
                    navtagic[row][count]=round(navcountryic[position+1],3)
                else:
                    navtagic[row][count]=0
            else:
                navtagic[row][count]=0




def calculator():
    for category, taglist in loop.items():
        inputtag = taglist
        #Sets which countries to analyze
        #Sets "save" folder path
        absolute_path = os.path.dirname(__file__)
        relative_path = "save\\"
        relative_path_images = "output\\"+category+"\\"
        folderpath = os.path.join(absolute_path, relative_path)
        folderpathimages = os.path.join(absolute_path, relative_path_images)
        if save_directory != None:
            folderpath = save_directory+"/"
        if image_directory != None:
            folderpathimages = image_directory+"/"+category+"/"
        if not os.path.exists(folderpathimages):
            os.makedirs(folderpathimages)
        nautosaves=len([entry for entry in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath, entry))])


        tagic=[ [0]*len(inputtag) for i in range(nautosaves+1)] #monthly IC in columns
        tagic[0]=inputtag  #tags
        navtagic=[ [0]*len(inputtag) for i in range(nautosaves+1)] #monthly IC in columns
        navtagic[0]=inputtag  #tags
        contractic=[ [0]*len(inputtag) for i in range(nautosaves+1)] #monthly IC in columns
        contractic[0]=inputtag  #tags
        #calculates monthlyic for every file in /save. Edit this if you haven't saved your files as save1, save2,...
        for i in range(nautosaves):  
            filename=folderpath+"autosave_"+str(nautosaves-i)+".hoi4"
            print_progress_bar(i+1, nautosaves, "Wait...")
            progressbar.step(25/nautosaves)
            monthlyic(filename,i+1,tagic,navtagic)



        #apply moving average for instant ic and integrates for cumulative ic
        dat = np.array(tagic[1:])*30
        for i in range(len(inputtag)):
            dat[1:nautosaves-1,i]=moving_avg(dat[:,i],3)
        result = sci.cumtrapz(dat, axis=0, dx=1)
        dat = np.around(dat, decimals=3)
        result = np.around(result, decimals=3)

        navdat = np.array(navtagic[1:])*30
        for i in range(len(inputtag)):
            navdat[1:nautosaves-1,i]=moving_avg(navdat[:,i],3)
        navresult = sci.cumtrapz(navdat, axis=0, dx=1)
        navdat = np.around(navdat, decimals=3)
        navresult = np.around(navresult, decimals=3)



        x=range(1,nautosaves)
        x_ticks = [0, 12, 24, 36, 48, 60, 72, 84, 96]
        x_labels = ['1936', '1937', '1938', '1939', '1940', '1941', '1942', '1943', '1944']
        if inputtag != all:
            #plots results
            plt.rcParams.update({'font.size': 15})
            plt.figure("Produced MIL IC")
            plt.title("Produced MIL IC") 
            plt.xlabel("Years") 
            plt.ylabel("Produced MIL IC") 
            plt.plot(x,result) 
            plt.xticks(x_ticks, x_labels)
            plt.legend(tagic[0])
            plt.grid( linestyle = '--', linewidth = 0.5)
            filename=folderpathimages+"ProducedLandIC.png"
            plt.savefig(filename, dpi=600, bbox_inches='tight' )
            plt.clf()
            x=range(0,nautosaves)
            plt.figure("Monthly MIL IC")
            plt.title("Monthly MIL IC") 
            plt.xlabel("Year") 
            plt.ylabel("Monthly MIL IC") 
            plt.plot(x,dat) 
            plt.grid( linestyle = '--', linewidth = 0.5)
            plt.xticks(x_ticks, x_labels)
            plt.legend(tagic[0])
            filename=folderpathimages+"MonthlyLandIC.png"
            plt.savefig(filename, dpi=600, bbox_inches='tight' )
            plt.clf()
            x=range(1,nautosaves)
        if inputtag == majors:
            #plots results
            plt.figure("Cumulative NAV IC")
            plt.title("Cumulative NAV IC") 
            plt.xlabel("Years") 
            plt.ylabel("Cumulative NAV IC") 
            plt.plot(x,navresult) 
            plt.xticks(x_ticks, x_labels)
            plt.legend(navtagic[0])
            plt.grid( linestyle = '--', linewidth = 0.5)
            filename=folderpathimages+"CumulativeNavalIC.png"
            plt.savefig(filename, dpi=600, bbox_inches='tight' )
            plt.clf()
            x=range(0,nautosaves)
            plt.figure("Monthly Naval IC")
            plt.title("Monthly Naval IC") 
            plt.xlabel("Year") 
            plt.ylabel("Monthly Naval IC") 
            plt.plot(x,navdat) 
            plt.grid( linestyle = '--', linewidth = 0.5)
            plt.xticks(x_ticks, x_labels)
            plt.legend(navtagic[0])
            filename=folderpathimages+"MonthlyNavalIC.png"
            plt.savefig(filename, dpi=600, bbox_inches='tight' )
            plt.clf()
        if inputtag == all:
            factions=["ALLIES", "AXIS", "COMINTERN","GEACPS"]
            factionmap =	{
            "\"GER\"":1,"\"SOV\"":2,"\"ENG\"":0,"\"JAP\"":3,"\"USA\"":0,"\"ITA\"":1,"\"FRA\"":0,
            "\"RAJ\"":0, "\"CAN\"":0, "\"AST\"":0, "\"SAF\"":0, "\"NZL\"":0, "\"POL\"":0, "\"CHI\"":0,
            "\"HUN\"":1, "\"ROM\"":1, "\"BUL\"":1,"\"SPR\"":1,"\"SLO\"":1,"\"MAN\"":3, "\"RCC\"":3,
            }
            factionic=[ [0]*len(factions) for i in range(nautosaves+1)] #monthly IC in columns
            factionic[0]=factions  #tags

            for rowindex, rows in enumerate(tagic): 
                for columnindex, column in enumerate(rows): 
                    if rowindex>0:
                        factionic[rowindex][factionmap[tagic[0][columnindex]]] += tagic[rowindex][columnindex]

            factiondat = np.array(factionic[1:])*30
            for i in range(len(factions)):
                factiondat[1:nautosaves-1,i]=moving_avg(factiondat[:,i],3)
            factionresult = sci.cumtrapz(factiondat, axis=0, dx=1)
            factiondat = np.around(factiondat, decimals=3)
            factionresult = np.around(factionresult, decimals=3)

            x=range(1,nautosaves)
            x_ticks = [0, 12, 24, 36, 48, 60, 72, 84, 96]
            x_labels = ['1936', '1937', '1938', '1939', '1940', '1941', '1942', '1943', '1944']

            #plots results
            plt.rcParams.update({'font.size': 15})
            plt.figure("Produced MIL IC")
            plt.title("Produced MIL IC") 
            plt.xlabel("Years") 
            plt.ylabel("Produced MIL IC") 
            plt.plot(x,factionresult) 
            plt.xticks(x_ticks, x_labels)
            plt.legend(factionic[0])
            plt.grid( linestyle = '--', linewidth = 0.5)
            filename=folderpathimages+"ProducedLandIC.png"
            plt.savefig(filename, dpi=600, bbox_inches='tight' )
            plt.clf()
            x=range(0,nautosaves)
            plt.figure("Monthly MIL IC")
            plt.title("Monthly MIL IC") 
            plt.xlabel("Year") 
            plt.ylabel("Monthly MIL IC") 
            plt.plot(x,factiondat) 
            plt.grid( linestyle = '--', linewidth = 0.5)
            plt.xticks(x_ticks, x_labels)
            plt.legend(factionic[0])
            filename=folderpathimages+"MonthlyLandIC.png"
            plt.savefig(filename, dpi=600, bbox_inches='tight' )
            plt.clf()



window = tk.Tk()
window.title("HOI4 IC calculator")
window.geometry('350x200')
lbl_save = tk.Label(window, text="Default: /internal/save")
lbl_save.grid(column=1, row=0)
lbl_image = tk.Label(window, text="Default: /internal/output")
lbl_image.grid(column=1, row=1)
image_directory = None
save_directory = None

def save_button_clicked():
    global save_directory 
    save_directory = tk.filedialog.askdirectory(parent=window,initialdir=os.path.dirname(__file__),title='Please select the saves directory')
    if save_directory != None:
        lbl_save.configure(text=save_directory)
def image_button_clicked():
    global image_directory 
    image_directory = tk.filedialog.askdirectory(parent=window,initialdir=os.path.dirname(__file__),title='Please select the output directory')
    if image_directory != None:
        lbl_image.configure(text=image_directory)
def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
def run_ic():
    threading.Thread(target=calculator, daemon=True).start()
btn = tk.Button(window, text="Select saves directory", command=save_button_clicked)
btn.grid(column=0, row=0)
btn = tk.Button(window, text="Select image directory", command=image_button_clicked)
btn.grid(column=0, row=1)
btn = tk.Button(window, text="Start calculator", command=run_ic)
btn.grid(column=0, row=2)
progressbar = ttk.Progressbar()
progressbar.place(x=130, y=130)
#progressbar.start()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()