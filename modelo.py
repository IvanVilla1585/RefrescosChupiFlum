# -*- coding: 850 -*-
from eralchemy import render_er
import getpass
import psycopg2

salida = False

while not salida :
   print 'Entre las credenciales del servidor--->'
   servidor = raw_input("Entre servidor : ")
   puerto = raw_input("Entre el puerto : ")
   basedatos = raw_input("Entre el la base de datos: ")
   usuario = raw_input("Entre el usuario: ")
   contrasena = getpass.getpass('Password')
   try:
       cadena = 'postgresql+psycopg2://'+usuario+':'+contrasena+'@'+servidor+':'+puerto+'/'+basedatos
       render_er(cadena, 'salida.png')
       print 'El modelo se encuentra en el archivo salida.png'
       salida=True
   except Exception, e:
       print u'Verifique los parametros de conexión'
       print str(e)
