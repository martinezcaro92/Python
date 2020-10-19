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

os.chdir('D:/OneDrive - Universidad Politécnica de Cartagena/OMNeT++/workbench2/flora/simulations/results/json/Scenario1/urban/NQ')
files_list = os.listdir();
print("files_list: "+str(files_list))
var = ['urban-SC1SEED-10--0-20190618-12:05:40-11528','urban-SC1SEED-11--0-20190618-12:09:53-11528','urban-SC1SEED-12--0-20190618-12:58:54-11528',
       'urban-SC1SEED-13--0-20190618-13:09:16-11528','urban-SC1SEED-14--0-20190618-13:12:24-11528','urban-SC1SEED-15--0-20190618-13:18:12-11528',
       'urban-SC1SEED-16--0-20190618-13:22:03-11528','urban-SC1SEED-17--0-20190618-13:25:24-11528','urban-SC1SEED-18--0-20190618-13:28:37-11528',
       'urban-SC1SEED-19--0-20190618-13:34:14-11528']
df = pd.DataFrame()
df_QoE_jitter = pd.DataFrame()
df_QoE_delay = pd.DataFrame()
df_QoE_gwav = pd.DataFrame()
df_QoE_pdr = pd.DataFrame()
df_QoE_thbps = pd.DataFrame()
df_QoI_validity = pd.DataFrame()

df_QoI_accuracy = pd.DataFrame()
df_QoI_timeliness = pd.DataFrame()
df_QoI_detail = pd.DataFrame()
df_QoI_precision = pd.DataFrame()
df_QoI_quantity = pd.DataFrame()
df_QoI_recall = pd.DataFrame()

df_general = pd.DataFrame()
df_QoD = pd.DataFrame()
df_QoI = pd.DataFrame()
df_QoE = pd.DataFrame()
df_QC = pd.DataFrame()

for t in range(0,len(files_list)):
#for t in range(0,3):
    data = pd.read_json(files_list[t])
    columns = len(data[var[t]]['vectors'])
    print("columns: "+str(columns))

    if t==0:
        df['time'] = data[var[t]]['vectors'][0]['time']
        df_QoD['time'] = data[var[t]]['vectors'][0]['time']
        df_QoI['time'] = data[var[t]]['vectors'][0]['time']
        df_QoE['time'] = data[var[t]]['vectors'][0]['time']
        nombres = ["time"]
        nombres_Q = ["time"]
        processing_period = int(data[var[t]]['moduleparams'][12]['**.networkServer1.samplePeriod'][:-1])

    nombres_Q.append((files_list[t][0:2]))
    for i in range(0, columns):
        temp1 = files_list[t][0:2]+'_'+data[var[t]]['vectors'][i]['attributes']['source'][:-2]
        nombres.append(temp1)
        df[temp1] = data[var[t]]['vectors'][i]['value']

        if (data[var[t]]['vectors'][i]['attributes']['source'][0:3] == 'QoD'):
            df_QoD[t+1] = data[var[t]]['vectors'][i]['value']

        else:
            if (data[var[t]]['vectors'][i]['attributes']['source'][0:3] == 'QoI'):
                df_QoI[t+1] = data[var[t]]['vectors'][i]['value']
            else:
                if (data[var[t]]['vectors'][i]['attributes']['source'][0:3] == 'QoE'):
                    df_QoE[t+1] = data[var[t]]['vectors'][i]['value']
    #print(nombres)
    #print(df.to_string())

df.columns = nombres
df_QoD.columns = nombres_Q
df_QoI.columns = nombres_Q
df_QoE.columns = nombres_Q
df_QoD['mean'] = df_QoD[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoI['mean'] = df_QoI[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoE['mean'] = df_QoE[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df.to_csv('D:/OneDrive - Universidad Politécnica de Cartagena/OMNeT++/S1_Urban.csv',sep=';',index=False,header=True)
'''
print(list(df.columns.values))

df_QoE_jitter['time'] = df['time']
for lo in range(10,20):
    stri = str(lo)+'_Jitter'
    df_QoE_jitter[str(lo)] = df[stri]

    stri = str(lo)+'_Delay'
    df_QoE_delay[str(lo)] = df[stri]

    stri = str(lo)+'_GWAv'
    df_QoE_gwav[str(lo)] = df[stri]

    stri = str(lo)+'_PDR'
    df_QoE_pdr[str(lo)] = df[stri]

    stri = str(lo)+'_ThBps'
    df_QoE_thbps[str(lo)] = df[stri]

    stri = str(lo)+'_quantity'
    df_QoI_quantity[str(lo)] = df[stri]

    stri = str(lo)+'_precision'
    df_QoI_precision[str(lo)] = df[stri]

    stri = str(lo)+'_recall_'
    df_QoI_recall[str(lo)] = df[stri]

    stri = str(lo)+'_detail'
    df_QoI_detail[str(lo)] = df[stri]

    stri = str(lo)+'_accuracy'
    df_QoI_accuracy[str(lo)] = df[stri]

    stri = str(lo)+'_timeliness_'
    df_QoI_timeliness[str(lo)] = df[stri]

    stri = str(lo)+'_validity'
    df_QoI_validity[str(lo)] = df[stri]

df_QoE_jitter['mean'] = df_QoE_jitter[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoE_delay['mean'] = df_QoE_delay[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoE_gwav['mean'] = df_QoE_gwav[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoE_pdr['mean'] = df_QoE_pdr[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoE_thbps['mean'] = df_QoE_thbps[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])

df_QoI_quantity['mean'] = df_QoI_quantity[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoI_precision['mean'] = df_QoI_precision[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoI_recall['mean'] = df_QoI_recall[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoI_detail['mean'] = df_QoI_detail[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoI_accuracy['mean'] = df_QoI_accuracy[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoI_timeliness['mean'] = df_QoI_timeliness[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])
df_QoI_validity['mean'] = df_QoI_validity[nombres_Q[1:]].sum(axis=1)/len(nombres_Q[1:])

print(df_QoE_jitter.head(n=10))
font = {'size':18}
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.plot(df['time'], df_QoE_jitter['mean'], color='#FF0000', linewidth=1, label='QoE - Jitter')#, linestyle='-')
ax1.plot(df['time'], df_QoE_delay['mean'], color='#804000', linewidth=1, label='QoE - Delay')#, linestyle='--')
ax1.plot(df['time'], df_QoE_gwav['mean'], color='#0000ff', linewidth=2, label='QoE - GW Availability')#, linestyle='--')
ax1.plot(df['time'], df_QoE_pdr['mean'], color='#00ff00', linewidth=1, label='QoE - PDR')
ax1.plot(df['time'], df_QoE_thbps['mean'], color='#6c4675', linewidth=1, label='QoE - Throughput(Bps)')
ax1.plot(df['time'], df_QoE['mean'], color='#000000', linewidth=2, label='QoE')
box = ax1.get_position()
ax1.grid(linestyle='--')
#ax1.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), fancybox=True, shadow=True, ncol=3,prop={'size':15})
#plt.title('Quality Components - Rural Environment',fontdict=font)
ax1.set_xlabel('time (s)',fontdict=font)
ax1.set_ylabel('Normalized Value',fontdict=font)
ax1.set_xlim([0.0, df['time'].max()])
ax1.set_ylim([0.0, 1.0])

ax2.plot(df['time'], df_QoI_quantity['mean'], color='#FF0000', linewidth=1, label='QoI - Quantity')#, linestyle='-')
ax2.plot(df['time'], df_QoI_precision['mean'], color='#804000', linewidth=1, label='QoI - Precision')#, linestyle='--')
ax2.plot(df['time'], df_QoI_recall['mean'], color='#0000ff', linewidth=1, label='QoI - Recall')#, linestyle='--')
ax2.plot(df['time'], df_QoI_detail['mean'], color='#00ff00', linewidth=1, label='QoI - Detail')
ax2.plot(df['time'], df_QoI_accuracy['mean'], color='#6c4675', linewidth=2, label='QoI - Accuracy')
ax2.plot(df['time'], df_QoI_timeliness['mean'], color='#7f1f2e', linewidth=2, label='QoI - Timeliness')
ax2.plot(df['time'], df_QoI_validity['mean'], color='#ff8000', linewidth=2, label='QoI - Validity')
ax2.plot(df['time'], df_QoI['mean'], color='#000000', linewidth=2, label='QoI')
box = ax1.get_position()
ax2.grid(linestyle='--')
#ax2.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 0.35), fancybox=True, shadow=True, ncol=4,prop={'size':15})
#plt.title('Quality Components - Rural Environment',fontdict=font)
ax2.set_xlabel('time (s)',fontdict=font)
ax2.set_ylabel('Normalized Value',fontdict=font)
ax2.set_xlim([0.0, df['time'].max()])
ax2.set_ylim([0.0, 1.0])
plt.show()

os.chdir('C:/omnetpp-5.2.1/workbench/flora/simulations/results/json/Scenario1/urban/NEC')
files_list = os.listdir();
print("files_list: "+str(files_list))


for t in range(0,len(files_list)):
#for t in range(0,1):
    print(files_list[t])
    data = pd.read_json(files_list[t])
    columns = len(data[var[t]]['vectors'])
    varii = 0; nombres_f = ['time_t']
    print("#columns: "+str(columns))

    for k in range(0, columns):
    #for k in range(0, 5):
        #print("iteration: "+str(i))
        nomb = []
        NodeCP = data[var[t]]['vectors'][k]['module'][14:16]
        if NodeCP[1] == "]":
            NodeCP = NodeCP[0:1]

        #print('node: ' + str(NodeCP))
        nombres_f.append(str(NodeCP))

    print(nombres_f)
    columns2 = len(nombres_f)-1
    print("columns2: "+str(columns2))

    for i in range(0, columns):
    #for i in range(0, 5):
        print("computing file: "+str(files_list[t])+" | iteration: "+str(i))
        df2 = pd.DataFrame()

        df2[0] = data[var[t]]['vectors'][i]['time']
        df2[1] = data[var[t]]['vectors'][i]['value']


        proc_block = df2[0] // processing_period
        sumato = 0; hist = 0; pc_node = [];

        if varii == 0 and t==0:
            mincol = proc_block[len(proc_block) - 1]
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

        print("len(pc_node): "+str(len(pc_node))+" | mincol: "+str(mincol))

        if len(pc_node) < mincol:
            tmp = mincol - len(pc_node);
            print("Entré")
            for j in range(0, int(tmp)):
                pc_node.append(0)

        #print(str(i)+" | len(pc_node): " + str(len(pc_node)))
        #print(pc_node)

        if len(pc_node) > mincol:
            pc[nombres_f[i+1]] = pc_node[:-1];
            print("Entro en la segunda condición")
        if len(pc_node) == mincol:
            pc[nombres_f[i + 1]] = pc_node;

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
    df_QC[files_list[t][0:2]] = QC

df_QC['mean'] = df_QC.sum(axis=1)/len(files_list)
print(df_QC.to_string())
fig, ax3 = plt.subplots()
ax3.plot(df['time'], df_QoD['mean'], color='#FF0000', linewidth=1, label='QoD')#, linestyle='-')
ax3.plot(df['time'], df_QoI['mean'], color='#0000ff', linewidth=1, label='QoI')#, linestyle='--')
ax3.plot(df['time'], df_QoE['mean'], color='#00ff00', linewidth=1, label='QoE')#, linestyle='--')
ax3.plot(pc['time_t'], df_QC['mean'], color='#000000', linewidth=1, label='QC')
box = ax1.get_position()
ax3.grid(linestyle='--')
#ax2.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 0.2), fancybox=True, shadow=True, ncol=4,prop={'size':15})
#plt.title('Quality Components - Rural Environment',fontdict=font)
ax3.set_xlabel('time (s)',fontdict=font)
ax3.set_ylabel('Normalized Value',fontdict=font)
ax3.set_xlim([0.0, df['time'].max()])
ax3.set_ylim([0.0, 1.0])

plt.show()'''