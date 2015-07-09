# Script to create the file
from functools import reduce
from Bird_creator import *
from WriteToLatex import *
from TableInput import *

import subprocess

import os
from functools import reduce
#os.chdir('C:\\Users\\Raphaël Nussbaumer\\Dropbox\\oiseau\\ebirdtolatex-checklist-generator')
os.chdir('C:\\Users\\Raphael\\Dropbox\\oiseau\\ebirdtolatex-checklist-generator')

Projet_name="Corsica"
Ebirdfile = 'BarChart_Corsica.txt'
print('Start Project: '+ Projet_name)

## Load Birdlist
if 'Birdlist' in locals() or 1:
    print('Load Birdlist from :'+Ebirdfile)
    Birdlist, info = Read_BarChart_file('BarChart/'+Ebirdfile)
    AddLanguage(Birdlist,'DataBase/Multiling_IOC_5.1_lighter_modif.csv','French_modif')
    AddInfo(Birdlist,'DataBase/eBird_Taxonomy_v1.55.csv')
    AddLanguage(Birdlist,'DataBase/Multiling_IOC_5.1_lighter_modif.csv','Scientific_name_modif')
    Birdlist.sort()
    

## Define column et Condition
if 1:
    print('define column and condition')
    Col=[]
    Col.append(TableInput('Checkbox',1))
    #Col.append(TableInput('Tiret',5,'8ex')) # number of tiret , length
    Col.append(TableInput('Language','EN'))
    Col.append(TableInput('Language','FR'))
    Col.append(TableInput('Language','LA'))
    #Col.append(TableInput('Freq','Year',0,info))
    Col.append(TableInput('Freq','Season',1,info))
    #Col.append(TableInput('Freq','Season',1,info))
    #Col.append(TableInput('Freq','Season',2,info))
    #Col.append(TableInput('Freq','Season',3,info))
    Col.append(TableInput('Freq','Month',6,info))
    #Col.append(TableInput('Note','4cm')) # lenght of note

    condition ="(('(hybrid)' not in bird.Name_En) and ('/' not in bird.Name_En) "
    condition_tableau = ['Main table display only non-hybrid birds with occurence >1\\%.',condition + "and (bird.Freq_month[5:7]>=0.01))"]
    condition_rare = ['\\footnotesize{>.1\\%}',condition + "and (bird.Freq_month[6]<.01) and (bird.Freq_month[6]>0.001) )"]


## Write To LateX
print('Write to latex')
WriteToLatex(Projet_name,Birdlist,'Latex/'+Projet_name+'.tex',Col,condition_tableau,condition_rare, info)

os.chdir('Latex'); os.system(Projet_name+'.tex');os.chdir('..')


## Run Latex
#print('Run pdflatex and open')
#os.chdir('Latex')
#os.system('"pdflatex '+ Projet_name + '.tex"')
#os.system('"start '+ Projet_name + '.pdf"')
#os.chdir('..')

