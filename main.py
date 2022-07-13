#dulezite importy:
import requests
from bs4 import BeautifulSoup
import os
import csv
import sys
import pprint
from datetime import datetime


def holky_kluci():
    hk = input("Zadej H pro holky, K pro kluky a nebo Hk pro obojí (pomalejší!): ")
    hk = hk.lower()
    hk = hk.title()
    return hk

def ziskat_jmena(hk):
    seznam_jmen = []
    txt = ""
    while txt.lower() != "q" :
        txt = input("Zadej jméno, P pro přednastavená jména, nebo Q pro konec: ")
        txt = txt.title()
        if txt == "P" and hk == "K":
            prednastavena_jmena = ["Špaček Jakub","Řehák Adam","Řehák Daniel", "Vymazal Jakub", "Vymazal Kryštof", "Grulich Josef", "Kojecký Tomáš", "Kojecký Jan", "Spáčil Jan", "Vaněk Tomáš"]
            for x in prednastavena_jmena:
                seznam_jmen.append(x)
        if txt == "P" and hk == "H":
            prednastavena_jmena = ["Ticháčková Eliška", "Prici Terezie", "Šrotová Linda", "Žáčková Nikol"]
            for x in prednastavena_jmena:
                seznam_jmen.append(x)
        if txt == "P" and hk == "Hk":
            prednastavena_jmena = ["Špaček Jakub", "Řehák Adam", "Řehák Daniel", "Vymazal Jakub", "Vymazal Kryštof","Grulich Josef", "Kojecký Tomáš", "Kojecký Jan", "Spáčil Jan", "Vaněk Tomáš","Ticháčková Eliška", "Prici Terezie", "Šrotová Linda", "Žáčková Nikol"]
            for x in prednastavena_jmena:
                seznam_jmen.append(x)
        if txt != "P" and txt != "Q" and txt != "" and txt not in seznam_jmen:
            seznam_jmen.append(txt)
    return seznam_jmen


def ziskat_nazev_csv():
    nazev_CSV = input("Zadej nazev vystupniho CSV souboru: ")
    nazev_CSV += ".csv"
    return nazev_CSV


def ziskat_HTML_stranky(odkaz):
    odpoved_serveru = requests.get(odkaz)
    soup = BeautifulSoup(odpoved_serveru.content, 'html.parser')
    return soup


def najit_udaje(soup,jmeno):
    td = soup.find_all("td")
    slice_1 = -1
    celkove_vysledky = []
    for x in td:
        x = x.string
        if x in jmeno:
            slice_2 = slice_1 + 7
            vysledek = []
            for y in td[slice_1:slice_2]:
                y = y.string
                vysledek.append(y)
            celkove_vysledky.append(vysledek)
        slice_1 += 1
    return celkove_vysledky


def zpracovat_odkaz(jmena, hk):
    vysledky = []
    if hk == "K":
        odkaz_odkaz = 0
        odkaz = ["http://vseprotenis.com/zebricky?kategorie=dorostenci&start=",0]
        while jmena and odkaz[1] < 2000:
            print(f"Prohledávám kluky: {odkaz_odkaz} jmen")
            odkaz_x = odkaz[0] + str(odkaz[1])
            soup = ziskat_HTML_stranky(odkaz_x)
            vysledky_z_internetu = najit_udaje(soup, jmena)
            for x in vysledky_z_internetu:
                if x[1] in jmena:
                    jmena.remove(x[1])
                vysledky.append(x)
            odkaz[1] += 50
            odkaz_odkaz += 50
    if hk == "H":
        odkaz_odkaz = 0
        odkaz = ["http://vseprotenis.com/zebricky?kategorie=dorostenky&start=",0]
        while jmena and odkaz[1] < 2000:
            print(f"Prohledávám holky: {odkaz_odkaz} jmen")
            odkaz_x = odkaz[0] + str(odkaz[1])
            soup = ziskat_HTML_stranky(odkaz_x)
            vysledky_z_internetu = najit_udaje(soup, jmena)
            for x in vysledky_z_internetu:
                if x[1] in jmena:
                    jmena.remove(x[1])
                vysledky.append(x)
            odkaz[1] += 50
            odkaz_odkaz += 50
    if hk == "Hk":
        odkaz = ["http://vseprotenis.com/zebricky?kategorie=dorostenci&start=",0]
        odkaz_odkaz = 0
        while jmena and odkaz[1] < 2000:
            print(f"Prohledávám kluky: {odkaz_odkaz} jmen")
            odkaz_x = odkaz[0] + str(odkaz[1])
            soup = ziskat_HTML_stranky(odkaz_x)
            vysledky_z_internetu = najit_udaje(soup, jmena)
            for x in vysledky_z_internetu:
                if x[1] in jmena:
                    jmena.remove(x[1])
                vysledky.append(x)
            odkaz[1] += 50
            odkaz_odkaz += 50
        odkaz = ["http://vseprotenis.com/zebricky?kategorie=dorostenky&start=",0]
        odkaz_odkaz = 0
        while jmena and odkaz[1] < 2000:
            print(f"Prohledávám holky: {odkaz_odkaz} jmen")
            odkaz_x = odkaz[0] + str(odkaz[1])
            soup = ziskat_HTML_stranky(odkaz_x)
            vysledky_z_internetu = najit_udaje(soup, jmena)
            for x in vysledky_z_internetu:
                if x[1] in jmena:
                    jmena.remove(x[1])
                vysledky.append(x)
            odkaz[1] += 50
            odkaz_odkaz += 50
    if jmena:
        print(f"Nepodařilo se najít: {jmena}")
    return vysledky


def ulozit_jako_csv(data: dict, vystupni_soubor: str) -> None:
    mode = "w" if vystupni_soubor not in os.listdir() else "a"
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(vystupni_soubor, mode, newline="") as csv_file:
        #keys = data[0].keys()
        keys = ["CŽ","Jméno","Body z 8 nej Dvouhry","Body z 8 nej Čtyřhry","Body celkem","BH","rCŽ",dt_string]
        dict_writer = csv.DictWriter(csv_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        csv_file.close()


def z_listu_na_dict(data):
    main_list = []
    #print(data)
    for list in data:
        keys = ["CŽ", "Jméno", "Body z 8 nej Dvouhry", "Body z 8 nej Čtyřhry", "Body celkem", "BH", "rCŽ"]
        dictionary = dict()
        dictionary[keys[0]] = list.pop(0)
        dictionary[keys[1]] = list.pop(0)
        dictionary[keys[2]] = list.pop(0)
        dictionary[keys[3]] = list.pop(0)
        dictionary[keys[4]] = list.pop(0)
        dictionary[keys[5]] = list.pop(0)
        dictionary[keys[6]] = list.pop(0)
        main_list.append(dictionary)
    return main_list



def main():
    nazev_CSV = ziskat_nazev_csv()
    hk = holky_kluci()
    jmena = ziskat_jmena(hk)
    data = zpracovat_odkaz(jmena, hk)
    dict = z_listu_na_dict(data)
    ulozit_jako_csv(dict, nazev_CSV)



main()