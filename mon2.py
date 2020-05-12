#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#54.3836864,86.115688
#54°36'36.864"N 86°11'56.88"E
#54.6435846&lng=86.1989354
#http://narodmon.ru/api/sensorsNearby?lat=54.65&lng=86.18&radius=50&uuid=6ce5e6b78477f27084cc524599fc5930&api_key=09XImZqvP6g6U&lang=ru
import math
import json
import time
import re
import warnings
import requests
import datetime
import ephem
from pprint import pprint
from datetime import date
from math import radians as rad, degrees as deg
from grab import Grab

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 '
                   'Firefox/14.0.1'),
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':
    'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding':
    'gzip, deflate',
    'Connection':
    'keep-alive',
    'DNT':
    '1'
}
warnings.filterwarnings("ignore")
localtime = time.localtime(time.time())
z = str(localtime[3])
y = str(localtime[4])

cmd = 'sensorsNearby'
uuid = '6ce5e6b78477f27084cc524599fc5930'  # narodmon
api_key = '09XImZqvP6g6U'  # narodmon
# Ленинск-Кузнецкий     lat=54&lon=86
lat = '54.65'  # Home 9  86.184826%2C54.681399
lng = '86.18'  # Home 9  lat=54.643689&lon=86.199094
#    lon : 86.17,   lat : 54.67
# Орел
lato = '53.0'
lngo = '36'

lang = 'ru'
radius = 50
types = '1,2'
appid = 'c7a1cf340957cc2f610b91e2993f3d2a'

#getapiuri = 'http://narodmon.ru/api/sensorsNearby?lat=54.65&lng=86.18&radius=50&types=1,2&uuid=6ce5e6b78477f27084cc524599fc5930&api_key=09XImZqvP6g6U&lang=ru'
geturi = f'http://narodmon.ru/api/sensorsNearby?lat={lat}&lng={lng}&radius={radius}&uuid={uuid}&api_key={api_key}&lang={lang}'
wing = Grab(timeout=300)
wing.go("https://yandex.ru/pogoda/leninsk-kuznetskiy/details")
#wing.go("https://yandex.ru/pogoda/leninsk-kuznetskiy")
oblak = Grab(timeout=300)
oblak.go("https://yandex.ru/pogoda/leninsk-kuznetskiy")

WeHtm = requests.post(geturi, headers=headers).text
#print (f'http://narodmon.ru/api/sensorsNearby?lat={lat}&lng={lng}&radius={radius}&uuid={uuid}&api_key={api_key}&lang={lang}')

devd = 2
devt = -1
tra = 0
senst = 0
sensd = 1
fact = json.loads(WeHtm)
unit = fact['devices'][devt]['sensors'][senst]['unit']
#print (fact['devices'][devt]['sensors'][send]['unit'])
#unit = "%"
#print (fact['devices'][-1]['sensors'])
if unit == '°':
    tra = 0
else:
    tra = 1
#print (unit, tra)
temp1 = fact['devices'][devt]['sensors'][tra]['value']
#temp1 = 99
#print (devt,temp1)
if temp1 > 40:
    devt = 3
    temp1 = fact['devices'][devt]['sensors'][tra]['value']
    #print (devt, temp1, "раз")
if temp1 > 40:
    devt = 2
    #print (devt, temp1, "два")
    temp1 = fact['devices'][devt]['sensors'][tra]['value']
if temp1 > 40:
    devt = 1
    #print (devt, temp1, "три")
if temp1 > 40:
    devt = 0
    #print (devt, temp1, "четыре")
temp1 = fact['devices'][devt]['sensors'][tra]['value']
nam = fact['devices'][devt]['sensors'][tra]['name']
#print (nam)

try:
    davl1 = fact['devices'][devd]['sensors'][sensd]['value']
    #print ("Датчик", devd)
except IndexError:
    devd = 0
    davl1 = fact['devices'][devd]['sensors'][sensd]['value']
    #print ("Датчик", devd)
except IndexError:
    devd = 1
    davl1 = fact['devices'][devd]['sensors'][sensd]['value']
    #print ("Датчик", devd)
except IndexError:
    devd = 2
    davl1 = fact['devices'][devd]['sensors'][sensd]['value']
    #print ("Датчик", devd)


#temp2 = fact['devices'][2]['sensors'][0]['value']
temp3 = fact['devices'][devt]['location']
unit = fact['devices'][devd]['sensors'][sensd]['unit']
sredn = round(temp1)
addr = fact['devices'][devt]['location']
addr = re.sub(r', Кемеровская обл.|, Россия', '', addr)
addr = nam # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
pres = json.loads(WeHtm)
#---------------------------------------------------------
try:
    veter = wing.xpath_text('//*[@class=" icon-abbr"]')
    #print ("Датчик 4")
except IndexError:
    veter = "Штиль"
    #print ("cyka 3")
#veter = wing.xpath_text('//*[@class=" icon-abbr"]')
try:
    speed = wing.xpath_text('//*[@class="wind-speed"]')
    speed = re.sub(r',', '.', speed)
    speed = round(int(float(speed)), 0)

except IndexError:
    speed = 0


try:
    pole = wing.xpath_list('//*[@class="forecast-fields__value"]')[1].text_content()
except IndexError:
    pole = "Нет данных"

#maps-widget-fact__title
#0x7fa1f686da90
#0x7f3a7d060b30

#print (pole)
if speed > 7:
    veter_color = "${color red}"
else:
    veter_color = "${color cyan}"

#print (w)
if veter == "С":
    veter = "Северный"
elif veter == "СВ":
    veter = "Северо-восточный"
elif veter == "В":
    veter = "Восточный"
elif veter == "ЮВ":
    veter = "Юго-восточный"
elif veter == "Ю":
    veter = "Южный"
elif veter == "ЮЗ":
    veter = "Юго-западный"
elif veter == "З":
    veter = "Западный"
elif veter == "СЗ":
    veter = "Северо-западный"
#print (veter)
oblak = oblak.xpath_text('//*[@class="link__feelings fact__feelings"]')
#print (type(oblak))
oblak = re.sub(r"Ощущается как.*", "", oblak)
#print (oblak)
if oblak == "Ясно":
    ocol = "${color yellow}"
elif oblak == "Пасмурно":
    ocol = "${color #999999}"
elif oblak == "Облачно с прояснениями":
    ocol = "${color #FFFFFF}"
elif oblak == "Малооблачно":
    ocol = "${color #FFFFFF}"
elif oblak == "Небольшой снег":
    ocol = "${color #999999}"
elif oblak == "Снег":
    ocol = "${color #999999}"
elif oblak == "Небольшой дождь":
    ocol = "${color #cyan}"
elif oblak == "Дождь":
    ocol = "${color #cyan}"
else:
    ocol = "${color #cyan}"
#---------------------------------------------------------
obs = ephem.Observer()
sun = ephem.Sun()
obs.lat = lat
obs.long = lng
obs.date = datetime.datetime.today()
rise_time = obs.next_rising(sun)
set_time = obs.next_setting(sun)
sunrise = ephem.localtime(rise_time).strftime('%H:%M')
sunset = ephem.localtime(set_time).strftime('%H:%M')
moon = ephem.Moon()
m_rise_time = obs.next_rising(moon)
m_set_time = obs.next_setting(moon)
moonrise = ephem.localtime(m_rise_time).strftime('%H:%M')
moonset = ephem.localtime(m_set_time).strftime('%H:%M')
'''if int(sredn) > 0:
    temp = "+" + str(sredn)
else:
    temp = str(sredn)'''

if int(sredn) > 0.1:
    temp = "+" + str(sredn)
    temp_color = "${color red}"
else:
    temp = str(sredn)
    temp_color = "${color cyan}"
davl = round(davl1)
g = ephem.Observer()
g.name = 'Somewhere'
g.lat = rad(54.6436)  # lat/long in decimal degrees
g.long = rad(86.1988)

m = ephem.Moon()
############################################################
g.date = date.today()
g.date -= ephem.hour
for i in range(1):
    m.compute(g)

    nnm = ephem.next_new_moon(g.date)
    pnm = ephem.previous_new_moon(g.date)
    lunation = (g.date - pnm) / (nnm - pnm)
    symbol = lunation * 26

    if symbol < 0.2 or symbol > 25.8:
        symbol = '1'  # neveter moon
    else:
        symbol = chr(ord('a') + int(symbol + 0.5) - 1)

    #print(ephem.localtime(g.date).time(), deg(m.alt),deg(m.az), ephem.localtime(g.date).time().strftime("%H%M"),  m.phase,symbol)
    mp = str(round(m.phase)) + "%"
    print("${color #AAAAAA}${font Moon Phases:size=44:bold}${alignc -75}${voffset 8}" + symbol, "${font Ubuntu:size=36:bold}${offset -50}${voffset -10}" + mp)  
    g.date += ephem.minute*15

print ("${color yellow}${voffset -75}${font Ubuntu:size=26}Восход${alignr}${color cyan}Закат")
print ("${voffset -3}${color yellow}" + sunrise + "${alignr}${color cyan}" + sunset)
print ("${color aaaaaa}${voffset -3}Луна${alignr}Луна")
print ("${voffset -3}" + moonrise + "${alignr}" + moonset)
print (temp_color + "${font zekton:size=64:bold}${alignc}${voffset -120}" + f"{temp}" + '°')
print (veter_color + '${voffset -90}${font Droid Sans:size=22}${alignc}' + str(speed) + " м/с " + veter + "\n${alignc}" + ocol + oblak)
print ('${color #cc00cc}${font Droid Sans:size=22}${alignc}' + pole)
print ('${color #99FF2F}${alignc}' + str(davl1) + ' м.р.c.\n${alignc}${voffset -5}' + addr)
#print ("${image /home/fil/icon.png -p 60,735 -s 90x90 -f 1800}")
#print (addr)

#print (oblak)