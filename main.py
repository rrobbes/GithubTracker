#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
#import simplejson as json
import time

from unidecode import unidecode
import Utilities.Login as Login
from Utilities import all_commits, tracker
from reports import eventReport, contribReport

import sys
reload(sys)
sys.setdefaultencoding('latin-1')

start=time.time()
# Se lee el archivo de config
# Cargamos la configuración de config.json
print "Leyendo configuración..."
config = json.load(open("config.json"))
#print config
for member in config["projects"][0]["members"]:
    for alias in  member["aliases"]:
        print str(alias)
# Se consigue el usuario correspondiente
print "Iniciando Sesión en Github..."

login = Login.Login(config["user"])
manager = login.get_user()
# Se realiza el tracking
print "Realizando el tracking con la cuenta de github..."
tracker.track(config, manager)

# Ahora se crean los archivos .gitattributes
print "Creando archivos .gitattributes en repos locales..."
for project in config["projects"]:
    for repo in project["repos"]:
        f = open(config["root"]+"/"+repo["name"]+"/.gitattributes","w")
        f.write("*.py diff=python\n*.java diff=java")

# Calcular las métricas extra
print "Calculando métricas..."
eventReport.get(config)
contribReport.get(config)

print "Listo! El archivo con todo lo necesario es 'out_final_missing.csv'"
print "Tiempo de ejecucion completo ",time.time()-start,' segundos '
