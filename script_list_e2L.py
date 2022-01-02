#!/usr/bin/env python
import os
import e2L
import json

with open('auth.json') as f:
  auth = json.load(f)

session = e2L.auth(auth['username'], auth['password'])


# https://api.ebird.org/v2/ref/hotspot/PR
# listHotspot = ['L358880','L323780','L323787','L293471','L802780','L323797','L341846','L323795','L343336','L294049','L293340','L420854','L323805','L323786','L323799','L293226','L293474','L550396','L682838','L341215','L323798','L293452','L527077','L682443','L323789','L323796','L323792','L813486','L340971']
# listHospotName = ['Cabo Rojo NWR','Hacienda La Esperanza','Reserva Natural Laguna Cartagena','Cabo Rojo - Salt Flats','La Parguera--town and nearest environs','Refugio de Vida Silvestre de Boqueron','Reserva Natural Punta Guaniquilla','Reserva Natural de Humacao','Salinas de Cabo Rojo','Viejo San Juan','Laguna Cartegena - West End','Refugio Vida Silvestre de Boqueron','Reserva Natural Ca√±o Tiburones','Bosque Estatal de Ganica','Faro de Rincon','Punta Algarrobo','Cabo Rojo--Mangrove Flats','Palmas Altas','La Boca, Barceloneta','Charca Salobre Los Amadores','Faro de Cabo Rojo','Laguna Cartegena--Tower','Jagueyes-Jobos Bay','Cabo Rojo NWR--Cambate access','Reserva Natural Laguna Tortuguero','Bosque Estatal de Pinones','Parque Central de San Juan','Bosque Nacional El Yunque','Parque Nacional Cerro Gordo']

listHotspot = ['L9601623','L323784','L323788','L4564353','L4081868','L323783','L323782','L682870','L738824','L682859','L5944654']
listHospotName = ['ANP El Conuco Sierra Bermeja','Bosque Estatal de Maricao','Bosque Estatal de Susúa','Reserva Natural Finca Nolla','Reserva Natural Cano Tiburones extremo oeste','Bosque Estatal de Rio Abajo','Bosque Estatal de Guajataca','Cerro Jayuya','Charcas Ponce','Escolar Superior Sabana Plain Pigeon spot','Rooselvelt Roads, Ceiba, PR']

lang = ['EN']
cat = ['species']
byear = 1900
eyear = 2050
bmonth = 1
emonth = 12
target_loc = "world"
target_time = "life"

format='letterpaper,margin=.3in,twocolumn'
family = False
spacing = '.95'
condition_tableau = ['Main table display only non-hybrid birds with occurence >1\\%.'," ( bird['freq']['year'] >= 0.01)"]
condition_rare = ['\\footnotesize{>.1\\%}'," (bird['freq']['year'] < .00) and (bird['freq']['year'] > 0.001)"]

for i,h in enumerate(listHotspot):
    projet_name = listHospotName[i]
    filename = projet_name.replace(' ','_').replace("'",'').replace('.','')
    code_loc = h 
    info, bird_list = e2L.bird_creator(session, code_loc, lang, cat, byear, eyear, bmonth, emonth)
    bird_list = e2L.statusInList('target-world',bird_list,session,target_loc,target_time)
    bird_list = e2L.statusInList('target-PR',bird_list,session,code_loc,target_time)
    bird_list = e2L.statusAvibase(['endemic-PR','introduce-PR'],bird_list, 'PR')
    col = []
    col.append(e2L.TableInput(info,'checkbox',1))
    statusTable = [['endemic-PR','bold'], ['introduce-PR','color-violet'],['target-world','sym-*']]
    col.append(e2L.TableInput(info,'lang','EN',statusTable))
    #col.append(e2L.TableInput(info,'freq','year',0))
    #col.append(e2L.TableInput(info,'freq','season',0))
    col.append(e2L.TableInput(info,'freq','month',0))
    e2L.write_to_latex(projet_name,filename,bird_list,col,condition_tableau, condition_rare, family, format, spacing, info)
    os.system('pdflatex -output-directory=./latex/ ./latex/'+ filename + '.tex ')
    input()
