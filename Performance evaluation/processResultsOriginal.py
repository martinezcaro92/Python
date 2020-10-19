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

data = pd.read_json('C:/omnetpp-5.2.1/workbench/flora/simulations/results/Scenario1-urban.json')
print(data)
#var = 'General-0-20190404-15:18:59-7180'; #Scenario1-urban
var = 'General-0-20190408-12:16:24-8920';
columns = len(data[var]['vectors'])
df = pd.DataFrame()

df[0] = data[var]['vectors'][0]['time']
nombres = ["time"]
print(df)



for i in range(0, columns):
    df[i+1] = data[var]['vectors'][i]['value']
    nombres.append(data[var]['vectors'][i]['attributes']['source'])
    #print(df.to_string())

    #print(data['General-0-20190312-14:52:27-7232']['vectors'][1])
df.columns = nombres
print(df.to_string())


data = pd.read_json('C:/omnetpp-5.2.1/workbench/flora/simulations/results/Scenario1-urban-EC.json')
#print(data)
#nombres = ["time"]; df.columns = nombres
columns = len(data[var]['vectors'])
processing_period = 500

varii = 0; nombres_f = ['time_t']

for k in range(0, columns):
#for k in range(0, 5):
    #print("iteration: "+str(i))
    nomb = []
    NodeCP = data[var]['vectors'][k]['module'][14:16]
    if NodeCP[1] == "]":
        NodeCP = NodeCP[0:1]

    #print('node: ' + str(NodeCP))
    nombres_f.append(str(NodeCP))

print(nombres_f)

for i in range(0, columns):
#for i in range(0, 5):
    print("iteration: "+str(i))
    df2 = pd.DataFrame()

    df2[0] = data[var]['vectors'][i]['time']
    df2[1] = data[var]['vectors'][i]['value']


    proc_block = df2[0] // processing_period
    sumato = 0; hist = 0; pc_node = [];
    mincol = proc_block[len(proc_block)-1]
    if varii == 0:
        time_t = list(np.linspace(processing_period,mincol*processing_period,mincol))
        varii = varii+1
        pc = pd.DataFrame(columns=nombres_f)
        pc['time_t'] = time_t
        print("Entro aquí ---")


    for j in range(0, len(proc_block)):
        if proc_block[j] == hist:
            sumato = sumato + df2[1][j]
        else:
            pc_node.append(sumato)
            hist = hist + 1
            sumato = df2[1][j]

    if len(pc_node) < mincol:
        tmp = mincol - len(pc_node);
        #print("Entré")
        for j in range(0, int(tmp)):
            pc_node.append(0)

    #print(str(i)+" | len(pc_node): " + str(len(pc_node)))
    #print(pc_node)


    pc[nombres_f[i+1]] = pc_node;
#pc.columns = nombres_f
#print("len(pc.columns): "+str(len(pc.columns))+" | len(nombres_f): "+str(len(nombres_f)))
#print(pc.head())

print("Inicio proceso de suma...")
suma = pc[nombres_f[1:]].sum()
#print(suma)

pc['suma'] = pc[nombres_f[1:]].sum(axis=1)
#print(pc)

min = 9999999
QC = []
for m in range(0,len(pc['suma'])):
    if (pc['suma'][m] < min):
        QC.append(1)
        min = pc['suma'][m]
    else:
        QC.append(min/pc['suma'][m])

#print(QC)
pc['QC'] = QC

'''plt.style.use('classic')
fig, ax = plt.subplots()
ax.plot(df['time'], df['Hum_S'], color='#000000', linewidth=3)#, linestyle='-')
ax.plot(df['time'], df['NO2_S'], color='#800000', linewidth=3)#, linestyle='--')
ax.plot(df['time'], df['NO_S'], color='#6A0888', linewidth=3)#, linestyle=':')
ax.plot(df['time'], df['NOX_S'], color='#0000FF', linewidth=3)#, linestyle='-.')
ax.plot(df['time'], df['O3_S'], color='#01DF01', linewidth=3)#, linestyle='-')
ax.plot(df['time'], df['PM10_S'], color='#FF0000', linewidth=3)#, linestyle='--')
ax.plot(df['time'], df['PM25_S'], color='#848484', linewidth=3)#, linestyle=':')
ax.plot(df['time'], df['SO2_S'], color='#FF8000', linewidth=3)#, linestyle='-.')
ax.plot(df['time'], df['Temp_S'], 'g', linewidth=3)#, linestyle='-')
ax.plot(df['time'], df['Ws_S'], color='#B40486', linewidth=3)#, linestyle='--')
#ax.plot(df['time'],df['Press_S'],color='#B40486',linewidth=3)#, linestyle='--')
#ax.plot(df['time'],df['Wd_S'],color='#B40486',linewidth=3)#, linestyle='--')
#ax.plot(df['time'],df['RF_S'],color='#8000FF')
ax.legend(loc='upper center', shadow=True, ncol=5)
plt.title('Dataset Variables')
ax.set_xlabel('Simulation time (s)')
ax.set_ylabel('Value')
plt.xlim([0.0, df['time'].max()])'''

#plt.show()

'''fig2, ax2 = plt.subplots()
ax2.plot(df['time'], df['validity_S'], color='#848484', linewidth=1, label='Validity')#, linestyle='-')
ax2.plot(df['time'], df['timeliness_S2'], color='#800000', linewidth=1, label='Timeliness')#, linestyle='--')
ax2.plot(df['time'], df['recall_S2'], color='#6A0888', linewidth=1, label='Recall')#, linestyle=':')
ax2.plot(df['time'], df['precision_S2'], color='#0000FF', linewidth=1, label='Precision')#, linestyle='-')
ax2.plot(df['time'], df['detail_S'], color='#FF0000', linewidth=1, label='Detail')#, linestyle='--')
ax2.plot(df['time'], df['quantity_S'], color='#ff8700', linewidth=1, label='Quantity')#, linestyle='-.')
ax2.plot(df['time'], df['QoI_S'], color='#000000', linewidth=1, label='QoI')#, linestyle='--')
ax2.plot(df['time'], df['QoI_S2'], color='#93C572', linewidth=1, label='QoI2')#, linestyle='--')
plt.xlim([0.0, df['time'].max()])
plt.ylim([0.0, 1.05])
#ax2.plot(df['time'],df['accuracy_S'],color='#848484',linewidth=3, label='Accuracy')#, linestyle=':')
box = ax2.get_position()
ax2.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
# Put a legend below current axis
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)
#ax2.legend(loc='center right', shadow=True, ncol=1)
plt.title('QoI Parameters (*)')
ax2.set_xlabel('Simulation time (s)')
ax2.set_ylabel('Value')'''

'''fig3,ax3 = plt.subplots()
ax3.plot(df['time'], df['Jitter_S'], color='#93C572', linewidth=1, label='Jitter')#, linestyle='-')
ax3.plot(df['time'], df['GWAv_S'], color='#566573', linewidth=1, label='GW Availability')#, linestyle='--')
ax3.plot(df['time'], df['Delay_S'], color='#ff0000', linewidth=1, label='Delay')#, linestyle='--')
ax3.plot(df['time'], df['QoE_S2'], color='#000000', linewidth=1, label='QoE2')
ax3.plot(df['time'], df['PDR_S'], color='#e96bc9', linewidth=1, label='Packet Delivery Rate')#, linestyle='--')
ax3.plot(df['time'], df['QoE_S'], color='#0000FF', linewidth=1, label='QoE')#, linestyle='--')
ax3.plot(df['time'], df['ThBps_S'], color='#ff8700', linewidth=1, label='Throughput Bits/s')#, linestyle='--')
box = ax3.get_position()
ax3.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)
plt.title('QoE Parameters')
ax3.set_xlabel('Simulation time (s)')
ax3.set_ylabel('Value')
plt.xlim([0.0, df['time'].max()])
plt.ylim([0.0, 1.05])'''


'''fig4,ax4 = plt.subplots()
ax4.plot(df['time'], df['QoI_S'], color='#000000', linewidth=3, label='QoI')#, linestyle='-')
ax4.plot(df['time'], df['QoI_S2'], color='#93C572', linewidth=3, label='QoI Normalized')#, linestyle='--')
box = ax4.get_position()
ax4.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
# Put a legend below current axis
ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2)
plt.title('QoI (*) vs. QoI (Normalized Method)')
ax4.set_xlabel('Simulation time (s)')
ax4.set_ylabel('Value')
plt.xlim([0.0, df['time'].max()])


fig5,ax5 = plt.subplots()
ax5.plot(df['time'], df['QoE_S'], color='#000000', linewidth=3, label='QoE Product')#, linestyle='-')
ax5.plot(df['time'], df['QoE_S2'], color='#93C572', linewidth=3, label='QoE Mean')#, linestyle='--')
box = ax5.get_position()
ax5.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
# Put a legend below current axis
ax5.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2)
plt.title('QoE (*) vs. QoE2')
ax5.set_xlabel('Simulation time (s)')
ax5.set_ylabel('Value')
plt.xlim([0.0, df['time'].max()])


#df.at[23,'ThPkt_S'] = df['ThPkt_S'].mean()


fig6, ax6 = plt.subplots()
ax6.plot(df['time'], df['QoD_S'], color='#B40486', linewidth=2, label='QoD')#, linestyle='--')
ax6.plot(df['time'], df['QoD_S2'], color='#000000', linewidth=4, label='QoD2')
box = ax6.get_position()
ax6.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax6.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
plt.title('Quality of Data Parameters')
ax6.set_xlabel('Simulation time (s)')
ax6.set_ylabel('Value')
plt.xlim([0.0, df['time'].max()])'''




fig7, ax7 = plt.subplots()
ax7.plot(df['time'], df['QoI_S'], color='#FF0000', linewidth=1, label='QoI')#, linestyle='-')
#ax7.plot(df['time'], df['QoI_S2'], color='#ff8700', linewidth=1, label='QoI2')#, linestyle='--')
ax7.plot(df['time'], df['QoE_S'], color='#93C572', linewidth=1, label='QoE')#, linestyle='--')
#ax7.plot(df['time'], df['QoE_S2'], color='#93C572', linewidth=1, label='QoE2')#, linestyle='--')
ax7.plot(df['time'], df['QoD_S'], color='#000000', linewidth=1, label='QoD')#, linestyle='--')
ax7.plot(pc['time_t'], pc['QC'], color='#0000ff', linewidth=1, label='QC')
box = ax7.get_position()
ax7.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax7.legend(loc='upper center', bbox_to_anchor=(0.8, 0.1), fancybox=True, shadow=True, ncol=4)
plt.title('Quality Components - Urban Environment')
ax7.set_xlabel('Simulation time (s)')
ax7.set_ylabel('Normalized Values')
plt.xlim([0.0, df['time'].max()])
plt.ylim([0.0, 1.0])

'''fig8, ax8 = plt.subplots()
ax8.plot(df['time'], df['Res_S'], color='#ff8700', linewidth=1, label='Resolution')#, linestyle='-')
ax8.plot(df['time'], df['QoD_S2'], color='#000000', linewidth=1, label='QoD2')
ax8.plot(df['time'], df['thruthfullness_S'], color='#FF0000', linewidth=1, label='Thruthfullness')#, linestyle='--')
ax8.plot(df['time'], df['QoD_S'], color='#0000FF', linewidth=1, label='QoD')#, linestyle='--')
ax8.plot(df['time'], df['Comp_S'], color='#00FF00', linewidth=1, label='Completeness')#, linestyle='--')
box = ax8.get_position()
ax8.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax8.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=3)
plt.title('QoD Parameters')
ax8.set_xlabel('Simulation time (s)')
ax8.set_ylabel('Value')
plt.xlim([0.0, df['time'].max()])
plt.ylim([0.0, 1.05])'''



plt.show()