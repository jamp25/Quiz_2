#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script: ejer18.py
Versión: 1.0
Fecha: 22-10-2020
Autor: Gustavo Acosta
Descripción: después de envíar un comando de conversión
al micocotroladro Arduino se recibe el código de conversión asocida a la temperatura. Se calcula el error a partir de la rerencia ingresada por teclado y la medida -
de temperatura. Poseriormente se establecen los valores de pertenencia y se actualiza la gráfica de temperatura

"""
import time
import serial
import numpy as np
import skfuzzy as fz
import matplotlib.pyplot as plt

#-- definiciones asociadas a la conv. ADC --#
R = 4.88
Ks = 10.0
flag_ctrl = 'k'
nT = 0.5
#-- abre y configura puerto serial --#
uart = serial.Serial('/dev/ttyUSB0', 115200)
#-- universo del discurso y conjuntos difusos --#
U = np.arange(-45.0,45.0,0.01)
etmn = fz.trapmf(U,[-45,-45,-30,-20])
etne = fz.trapmf(U,[-30,-20,-10,0])
etze = fz.trimf(U,[-10,0,10])
etpo = fz.trapmf(U,[0,10,20,30])
etmp = fz.trapmf(U,[20,30,40,45])
#-- se ingresa referencia --#
r = float(input('Ingrese referencia de temp. (25 a 55): '))
#-- inicializaciones asociadas a la graficación --#
x_lim = 500
y_lim = 50
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim([0, x_lim])
ax.set_ylim([0, y_lim])
plt.title('Sensor de Temperatura LM35')
plt.ylabel('Temperatura [C]')
plt.xlabel('Tiempo, nT = n*0.5 [s]')
xdata = []
ydata = []
t = 0.0
while (True):
time.sleep(nT) # T de muestreo, fs = 1/nT
uart.write(flag_ctrl) # comando de conv. ADC
code = int(uart.readline()) # lee y conv. a entero
Tm = (R * code)/Ks # calcula temperatura
e = r - Tm # calcula error
#-- calcula valores de pertenencia a cada conjunto difuso --#
u_etmn = fz.interp_membership(U,etmn,e)
u_etne = fz.interp_membership(U,etne,e)
u_etze = fz.interp_membership(U,etze,e)
u_etpo = fz.interp_membership(U,etpo,e)
u_etmp = fz.interp_membership(U,etmp,e)
#-- imprime resultados --#
print 'Tm = %.1f' % (Tm), u"\u2103"#, '\n'
print 'e = r - Tm = %.2f' % (e), u"\u2103"#, '\n'
print 'Valores de pertenencia:'
print ' -----------------'
print ' | u_etmn = %.2f | ' % (u_etmn)
print ' | u_etne = %.2f | ' % (u_etne)
print ' | u_etze = %.2f | ' % (u_etze)
print ' | u_etpo = %.2f | ' % (u_etpo)
print ' | u_etmp = %.2f | ' % (u_etmp)
print ' -----------------'
#-- actualiza vectores y grafica --#
t = t + nT
xdata.append(t)
ydata.append(Tm)
line.set_data(xdata, ydata)
plt.pause(0.001)


