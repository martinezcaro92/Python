# Author: Jose Manuel Martinez Caro
# Technical University of Cartagena
# Automatizally generates a config .ini/.ned
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math
import random


SF_v = [7, 8, 9, 10, 11, 12]
TP_v = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
#TP_v = [6, 7, 8, 9, 10, 11, 12, 13, 14]
num_SF = len(SF_v)
num_TP = len(TP_v)


samplePeriod = input("Sample Period (s) - default 200s: ")
if samplePeriod == '':
    samplePeriod = '200s'

while True:
    env_sit = input("Simulation environment (rural, subur, urban): ")
    if (env_sit=="rural"):
        position = pd.read_csv('C:/omnetpp-5.2.1/workbench/flora/simulations/estacionesRural.csv', encoding='utf-8')
        num_nodes = input("Número de nodos (type 'All' for all file): ")
        if num_nodes == 'All':
            num_nodes = position.shape[0]
        num_nodes_i = int(num_nodes)
        position3 = position[0:num_nodes_i]
        position2 = position3
        print(position2)
        break
    elif(env_sit=="subur"):
        position = pd.read_csv('C:/omnetpp-5.2.1/workbench/flora/simulations/estacionesSuburban.csv', encoding='utf-8')
        num_nodes = input("Número de nodos (type 'All' for all file): ")
        if num_nodes == 'All':
            num_nodes = position.shape[0]
        num_nodes_i = int(num_nodes)
        position3 = position[0:num_nodes_i]
        position2 = position3

        break
    elif(env_sit=="urban"):
        position = pd.read_csv('C:/omnetpp-5.2.1/workbench/flora/simulations/estacionesUrban.csv', encoding='utf-8')
        num_nodes = input("Número de nodos (type 'All' for all file): ")
        if num_nodes == 'All':
            num_nodes = position.shape[0]
        num_nodes_i = int(num_nodes)
        position3 = position[0:num_nodes_i]
        position2 = position3

        break
    else:
        print("The simulation environment has not been inserted correctly, try again...")



## CALCULATE GRID
if num_nodes_i <15:
    gridX = 2
    gridY = 2
elif num_nodes_i <30:
    gridX = 3
    gridY = 3
elif num_nodes_i <= 45:
    gridX = 4
    gridY = 4
elif num_nodes_i <= 57:
    gridX = 5
    gridY = 5


lista = list(range(0, num_nodes_i))
SF_assigned = list(range(0, num_nodes_i))
TP_assigned = list(range(0, num_nodes_i))

LATGrid = (position2['Latitude'][0:num_nodes_i].max() + 100)/gridX
LONGrid = (position2['Longitude'][0:num_nodes_i].max() + 100)/gridY

GX = position2['Latitude'][0:num_nodes_i]//LATGrid
GY = position2['Longitude'][0:num_nodes_i]//LONGrid
print(list(GX))
print(list(GY))

NodesGrid = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
#NodesGrid[4][4] = 100
for z in range(0,len(GX)):
    NodesGrid[int(GX[z])][int(GY[z])] = NodesGrid[int(GX[z])][int(GY[z])] + 1

print(NodesGrid)


# INI FILE GENERATION
file = open("C:/omnetpp-5.2.1/workbench/flora/simulations/IoT.ini", "w")

file.write("# ---------- Autogenerated file with Python -------- #\n")
file.write("[General]\n")
file.write("network = IoT\n")
file.write('#rng-class = "cMersenneTwister"\n\n')



file.write("#  ***** Number of LoRa Gateways (default = 1) ***** #\n")
file.write("**.numberOfGateways = 1\n")
file.write("#  ** Number of LoRa Nodes ** \n")
file.write("**.numberOfNodes = "+str(num_nodes_i)+"\n")


file.write("#  **** DEVICES PARAMETERS *****  #\n")
file.write("#  ** LoRaGW[0] - parameters **  #\n")
file.write("**.loRaGW[0].numUdpApps = 1\n")
file.write("**.loRaGW[0].packetForwarder.localPort = 2000\n")
file.write("**.loRaGW[0].packetForwarder.destPort = 1000\n")
file.write('**.loRaGW[0].packetForwarder.destAddresses = "backbone.networkServer1"\n')
file.write("#**.loRaGW[0].packetForwarder.indexNumber = 0\n\n")

file.write("#  ** networkServer - parameters **  #\n")
file.write("**.networkServer1.numUdpApps = 1\n")
file.write("**.networkServer1.**.evaluateADRinServer = false\n")
file.write('**.networkServer1.udpApp[0].typename = "NetworkServerApp"\n')
file.write('**.networkServer1.**.destAddr = "loRaGW[0]"\n')
file.write("**.networkServer1.**.destPort = 2000\n")
file.write("**.networkServer1.**.localPort = 1000\n")
file.write("**.networkServer1.samplePeriod = "+samplePeriod+"s\n")
file.write('#**.networkServer1.udpApp[0].adrMethod = ${"avg"}\n\n')

file.write("#  ** LoRaNodes[*] - parameters **  #\n")
file.write("**.loRaNodes[*].**.initFromDisplayString = false\n")
file.write("**.loRaNodes[*].**.evaluateADRinNode = false\n")
file.write("**.loRaNodes[*].gatewayX = "+str(int(position2['Latitude'].mean()))+"\n")
file.write("**.loRaNodes[*].gatewayY = "+str(int(position2['Longitude'].mean()))+"\n")
file.write('**.loRaNodes[*].**.initialLoRaBW = 125 kHz\n')
file.write("**.loRaNodes[*].**.initialLoRaCR = 4\n\n")


file.write("#  **** GENERAL PARAMETERS ***** #\n")
file.write("#  ** Number of Packet to Send **  #\n")
file.write("**.numberOfPacketsToSend = 0 #0 means infinite number of packets\n")
file.write("#  ** Simulation time (limit) **  #\n")
file.write("sim-time-limit = 7d\n")
file.write("#  ** Warm-up period (NO AT THE MOMENT) ** #\n")
file.write("#warmup-period = 1d\n")
file.write("#  ** Simulation time resolution **  #\n")
file.write("simtime-resolution = -11\n\n")

file.write("#  ** Simulation start-time **  #\n")
file.write("**.timeToFirstPacket = exponential(100s)\n")
file.write("#  ** Next Packet Period **  #\n")
file.write("**.timeToNextPacket = exponential(100s)\n")
file.write("#  ** ¿Aloha Channel Model? **  #\n")
file.write("**.alohaChannelModel = false\n\n")

file.write("#  **** NODE LOCALIZATION ***** #\n")

for i in range(0,int(num_nodes)):
    file.write("#  ** Node: "+str(position['Description'][i])+" **  #\n")
    file.write("**.loRaNodes["+str(i)+"].**.initialX = "+str(position2['Latitude'][i])+"m \n")
    file.write("**.loRaNodes["+str(i)+"].**.initialY = "+str(position2['Longitude'][i])+"m \n")
    file.write('**.loRaNodes[' + str(i) + '].name = "' + str(position2['Description'][i]) + '"\n')
    file.write("# Distance to GW: "+str(math.sqrt((int(position2['Latitude'][0:num_nodes_i].mean())-position2['Latitude'][i])**2+(int(position2['Longitude'][0:num_nodes_i].mean())-position2['Longitude'][i])**2))+"m \n\n")
    lista[i] = math.sqrt((int(position2['Latitude'].mean())-position2['Latitude'][i])**2+(int(position2['Longitude'][0:num_nodes_i].mean())-position2['Longitude'][i])**2);

print("distancia media a GW: "+str(sum(lista)/len(lista)))
print("distancia maxima a GW: "+str(max(lista)))
print("distancia minima a GW: "+str(min(lista)))

print(lista)
listaPD = pd.DataFrame({'distance':lista})
file.write("#  ** LoRa: SF y TP PARAMETERS  **  #\n")
for i in range(0,num_nodes_i):
    file.write("#  ** loRaNodes["+str(i)+"]   **  #\n")
    for j in range(1,num_SF+1):
        if listaPD['distance'][i] <= listaPD['distance'].quantile((j/num_SF)):
            SF_assigned[i] = SF_v[j-1]
            break
    file.write("**.loRaNodes[" + str(i) + "].**.initialLoRaSF = " + str(SF_assigned[i]) + "\n")
    for j in range(1,num_TP+1):
        if listaPD['distance'][i] <= listaPD['distance'].quantile((j/num_TP)):
            TP_assigned[i] = TP_v[j-1]
            break
    file.write("**.loRaNodes[" + str(i) + "].**.initialLoRaTP = " + str(TP_assigned[i]) + "dBm\n")
print(SF_assigned)
print(TP_assigned)


file.write("\n#  ** GW: LoRaGW  **  #\n")
file.write("**.LoRaGWNic.radio.iAmGateway = true\n")
file.write("**.loRaGW[*].**.initFromDisplayString = false\n")
file.write("**.loRaGW[0].**.initialX = "+str(int(position2['Latitude'][0:num_nodes_i].mean()))+"m \n")
file.write("**.loRaGW[0].**.initialY = "+str(int(position2['Longitude'][0:num_nodes_i].mean()))+"m \n\n")

file.write("#  ** backbone  **  #\n")
file.write("**.backboneX = "+str(int(position2['Latitude'][0:num_nodes_i].mean()))+" \n")
file.write("**.backboneY = "+str(int(position2['Longitude'][0:num_nodes_i].mean()))+" \n\n")

file.write("#  ** LoRaMedium  **  #\n")
file.write("**.mediumX = "+str(int(position2['Latitude'][0:num_nodes_i].max()*0.2))+" \n")
file.write("**.mediumY = "+str(int(position2['Longitude'][0:num_nodes_i].max()*0.2))+" \n\n")

file.write("#  ** Configurator  **  #\n")
file.write("**.configX = "+str(int(position2['Latitude'][0:num_nodes_i].max()*0.2))+" \n")
file.write("**.configY = "+str(int(position2['Longitude'][0:num_nodes_i].max()*0.45))+" \n\n")


file.write("#  ** Energy Consumption Model **  #\n")
file.write('**.loRaNodes[*].LoRaNic.radio.energyConsumerType = "LoRaEnergyConsumer"\n')
file.write("#  ** Energy Source Module ** #\n")
file.write('**.loRaNodes[*].**.energySourceModule = "IdealEpEnergyStorage"\n')
file.write("#  ** Energy Consumption Parameters **  #\n")
file.write('**.loRaNodes[*].LoRaNic.radio.energyConsumer.configFile = xmldoc("energyConsumptionParameters.xml")\n\n')
file.write("#  ** Defining Working Area **  #\n")
file.write('**.constraintAreaMinX = 0m\n')
file.write('**.constraintAreaMinY = 0m\n')
file.write('**.constraintAreaMinZ = 0m\n')
file.write('**.constraintAreaMaxX = '+str(position2['Latitude'].max() + 100)+'m # 100 is margin\n')     # 100 is margin
file.write('**.constraintAreaMaxY = '+str(position2['Longitude'].max() + 100)+'m # 100 is margin\n')    # 100 is margin
file.write('**.constraintAreaMaxZ = 0m\n\n')

file.write("#  ** Network Size Parameters **  #\n")
file.write('**.networkSizeX = '+str(int(position2['Latitude'][0:num_nodes_i].max()) + 100)+' # 100 is margin\n')    # 100 is margin
file.write('**.networkSizeY = '+str(int(position2['Longitude'][0:num_nodes_i].max()) + 100)+' # 100 is margin\n\n') # 100 is margin

file.write("#  ** Grid Numbers **  #\n")
file.write('**.processing.gridX = '+str(gridX)+'\n')
file.write('**.processing.gridY = '+str(gridY)+'\n\n')

file.write("#  ** Separate TX/RX Parts (COMMENTED)**  #\n")
file.write('# LoRaNetworkTest.**.radio.separateTransmissionParts = false\n')
file.write('# LoRaNetworkTest.**.radio.separateReceptionParts = false\n\n')

file.write("#  ** PATH LOSS PARAMETERS **  #\n")
file.write("#  ** LoRaLogNormalShadow **  #\n")
file.write("#  ** $\sigma **  #\n")
file.write('**.sigma = 0\n')
file.write("#  ** $\alpha **  #\n")
file.write('**.alpha = 2\n')
file.write("#  ** $\gamma **  #\n")
file.write('**.gamma = 2.08\n')
file.write("#  ** $\d0 **  #\n")
file.write('**.d0 = 40m\n\n')

file.write("#  ** Okumura-Hata - DEVELOPED**  #\n")
file.write("#  ** h_m **  #\n")
file.write('**.h_m = 4\n')
file.write("#  ** h_b **  #\n")
file.write('**.h_b = 49\n')
file.write("#  ** a_T **  #\n")
file.write('**.a_T = "'+str(env_sit)+'"\n\n')

file.write("#  ** Delay config **  #\n")
file.write('**.delayer.config = xmldoc("cloudDelays.xml")\n')
file.write("#  ** Radio Medium Module Parameters **  #\n")
file.write('**.radio.radioMediumModule = "LoRaMedium"\n')
file.write("#  ** Path-Loss Method **  #\n")
file.write('**.LoRaMedium.pathLossType = "LoRaOH"\n')
file.write("#  ** Minimum Interface Time **  #\n")
file.write('**.minInterferenceTime = 0s\n')
file.write("#  ** Display Interface Adresses **  #\n")
file.write('**.displayAddresses = false\n\n')

file.write("#  RANDOM SEEDS **  #\n")

for v in range(10,20):
    #file.write("[Config SC2SEED-"+str(v)+"-"+env_sit+"]\n")
    file.write("[Config "+env_sit+"-SC1SEED-"+str(v)+"-]\n")
    file.write("seed-set = "+str(v)+"\n\n")






file.close()


