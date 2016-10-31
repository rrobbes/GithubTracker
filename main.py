#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time

import Utilities.Login as Login
from Utilities import all_commits, tracker
from reports import eventReport, contribReport

start=time.time()
# Cargamos la configuración de config.json
login = Login.Login()
# Se lee el archivo de config
print "Leyendo configuración..."
config = json.load(open('config.json'))
# Se consigue el usuario correspondiente
print "Iniciando Sesión en Github..."
manager = login.get_user()
# Se realiza el tracking
print "Realizando el tracking con la cuenta de github..."
tracker.track(config, manager)

# Ahora se consiguen los commits desde los repo
print "Buscando información de commits desde los repos locales..."
all_commits.get(config)
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