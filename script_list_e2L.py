#!/usr/bin/env python
from numpy import genfromtxt
import csv
import os
import e2L
import unidecode
import time
import webbrowser
import numpy as np

# Define function used later
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


# download ll of hotspot for region
import requests
response = requests.request("GET", "https://ebird.org/ws2.0/ref/hotspot/KE", headers={'X-eBirdApiToken': 'vcs68p4j67pt'}, params={"fmt":"csv"})
file = open("KE/KE.csv", "w")
file.write(response.text)
file.close()

# Dowanload data
import json
response = requests.request("GET", "https://ebird.org/ws2.0/ref/hotspot/KE", headers={'X-eBirdApiToken': 'vcs68p4j67pt'}, params={"fmt":"json"})
data  = json.loads(response.text)

for d in data:
	url = 'http://ebird.org/ebird/barchartData?r={code_loc}&bmo={bmonth}&emo={emonth}&byr={byear}&eyr={eyear}&fmt=json'.format(
		code_loc=d['locId'], byear=1900, eyear=2020, bmonth=1, emonth=12)
	r = requests.get(url)
	f = open('KE/barchart_'+d['locId']+'.json', 'wb')
	f.write(r.content)
	f.close()


# read file
listhotspots=[]
with open('listCode_loc.csv', mode='r') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    for rows in reader:
        d={}
        for i in range(len(rows)):
            d[header[i]] = rows[i]
        listhotspots.append(d)








urld={'condition': ["['season'][3]", '0.0001', '0.0001'], 'spacing': ['1'], 'byear': ['1900'], 'col': ['lang,EN,0', 'freq,year,0', 'freq,season,3', 'freq,month,11'], 'cat': ['species'], 'family': ['false'], 'emonth': ['12'], 'eyear': ['2017'], 'bmonth': ['01'], 'code_loc': ['ZA-'], 'project_name': ['Checkll of South Africa'], 'format': ['a4paper,margin=10mm,twocolumn']}
for idx,val in enumerate(urld['col']):
    urld['col'][idx] = val.split(',')

lang = [col[1] for col in urld['col'] if col[0]=='lang'] # a single language, or ll of several language en,en_US,de,en_AE,en_AU,en_IN,en_NZ,en_UK,en_ZA,es,es_AR,es_CL,es_CU, es_DO,es_ES,es_MX,es_PA,es_PR,fi,fr,fr_HT,ht_HT,in,is,pt_BR,pt_PT,tr,zh http://help.ebird.org/customer/portal/articles/1596582-common-name-translations-in-ebird
cat = urld['cat'] # domestic,form,hybrid,intergrade,issf,slash,species,spuh
byear = int(urld['byear'][0])
eyear = int(urld['eyear'][0])
bmonth = int(urld['bmonth'][0])
emonth = int(urld['emonth'][0])
cond_time = urld['condition'][0]
cond_rare = urld['condition'][1]
cond_tableau = urld['condition'][2]
format = urld['format'][0]
spacing = urld['spacing'][0]
family = urld['family'][0]

condition_tableau = ['Main table display only non-hybrid birds with occurence >1\\%.'," ( bird['freq']"+cond_time+" >= "+cond_rare+")"]
condition_rare = ['\\footnotesize{<.1\\%}'," (bird['freq']"+cond_time+" < "+cond_rare+") and (bird['freq']"+cond_time+" > "+cond_tableau+")"]


for l in listhotspots:
    if l['code_loc']:
        time.sleep(5)
        code_loc = l['code_loc']
        projet_name = l['eBird name']
        filename = unidecode.unidecode(projet_name).replace(' ','_').replace("'",'').replace('.','')
        info, bird_ll = e2L.bird_creator(code_loc, lang, cat, byear, eyear, bmonth, emonth)
        try:
            os.rename('_barchart.tsv','barchart/'+code_loc+'.tsv')
        except WindowsError:
            os.remove('barchart/'+code_loc+'.tsv')
            os.rename('_barchart.tsv','barchart/'+code_loc+'.tsv')
        col = []
        for urld_col in urld['col']:
            col.append(e2L.TableInput(info,urld_col[0],urld_col[1],urld_col[2]))
        e2L.write_to_latex(projet_name,filename,bird_ll,col,condition_tableau, condition_rare, family, format, spacing, info)
        os.chdir('latex')
        topline=l['#']+' (Route '+l['route']+') rating: '+l['star']+'\\\\'
        replace_line(filename+'.tex', 42, topline)
        os.system('pdflatex '+ filename + '.tex')
        os.chdir('..')















# Display 5 best location
specie='Short-clawed Lark'
files = os.listdir('barchart/')
freq=[]

for f in files:
    with open('barchart/'+f) as fp:  
        for line in fp:
            if line.startswith('Sample Size:'):
                n_week = [int(float(i)) for i in line.replace("Sample Size:","").split()]
            if line.startswith(specie):
                comName, linee = line.split('\t',1)
                f_w = [float(i) for i in linee.split()]
                freq.append(sum(np.array(n_week) * np.array(f_w)) / sum(n_week))


freq_s = sorted(freq, key=lambda k: k['year']) 
freq_s[len(freq_s)-1]['id'].split('.')[0]

webbrowser.open('https://ebird.org/hotspot/'+freq_s[len(freq_s)-1]['id'].split('.')[0])
webbrowser.open('https://ebird.org/hotspot/'+freq_s[len(freq_s)-2]['id'].split('.')[0])
webbrowser.open('https://ebird.org/hotspot/'+freq_s[len(freq_s)-3]['id'].split('.')[0])
webbrowser.open('https://ebird.org/hotspot/'+freq_s[len(freq_s)-4]['id'].split('.')[0])
webbrowser.open('https://ebird.org/hotspot/'+freq_s[len(freq_s)-5]['id'].split('.')[0])




















# Build table for all species.

files = os.listdir('barchart/')
data=[]
for l in listhotspots:
    if l['code_loc']:
        with open('barchart/'+ l['code_loc'] +'.tsv') as fp:
            n_week=0
            d=l;
            d['freq']=[]
            d['name']=[]
            for line in fp:
                if not line:
                    pass
                if line.startswith('\n'):
                    pass
                elif "Frequency of observations in the selected location(s).:" in line:
                    pass
                elif "Number of taxa" in line:
                    pass
                elif line.startswith("\tJan\t"):
                    pass
                elif line.startswith('Sample Size:'):
                    n_week = np.array([int(float(i)) for i in line.replace("Sample Size:", "").split()])
                    d['n']=sum(n_week)
                else:
                    comName, linee = line.split('\t',1)
                    f_w = np.array([float(i) for i in linee.split()])
                    d['freq'].append(round(sum(n_week * f_w)))
                    d['name'].append(comName)
            data.append(d)

# get list of bird
bird_list = set()
for d in data:
    for b in d['name']:
        bird_list.add(b)

# search the best place for each species
csv_str=[]
for bird in bird_list:
    tmp=[bird]
    for d in data:
        if bird in d['name']:
            tmp.append(d['freq'][d['name'].index(bird)])
        else:
            tmp.append(0)
    csv_str.append(tmp)


csv_header=[]
for d in data:
    d.pop('freq', None)
    d.pop('name', None)
    csv_header.append(list(d.values()))

csv_header = list(map(list, zip(*([list(d.keys())]+csv_header))))

csv_str2 = csv_header+csv_str


with open('listspecieWinter.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile)
    for col in csv_str2:
        wr.writerow(col)


