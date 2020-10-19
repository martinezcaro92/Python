import pandas as pd
import os
import numpy as np

os.chdir('C:/omnetpp-5.2.1/workbench/flora/simulations/stations')
actual_dir = os.getcwd()
print(actual_dir)
csv_files = os.listdir()
print(csv_files)


newNames = ['NO2', 'NOX', 'NO', 'PM10', 'PM2.5', 'Wind_Speed', 'Temp', 'Wind_Dir', 'Hum', 'End']

original_delete = ['Date', 'Hour', 'NO2 max (ľg/m3)', 'NO2 - ICA', 'O3 8h max (ľg/m3)', 'O3 8h max - ICA', 'PM10 - ICA',
                   'SO2 - ICA', 'ICA Estación', 'CO 8h max (mg/m3)', 'CO 8h max - ICA', 'PM2,5 - ICA', 'R (w/m2)',
                   'M-P-XILENO (ľg/m3)', 'Benceno (ľg/m3)', 'SH2 (ľg/m3)', 'Tolueno (ľg/m3)', 'Etilbenceno (ľg/m3)',
                   'Ortoxileno (ľg/m3)', 'R.UVA (w/m2)', 'NH3 (ľg/m3)', 'CO - ICA', 'O3 - ICA', 'CO 8h (mg/m3)',
                   'O3 8h (ľg/m3)','SO2 (ľg/m3)','O3 (ľg/m3)', 'CO (mg/m3)','Precipitación (l/m2)', 'P (mBar)',] # 'Precipitación (l/m2)'

original_modify = [ 'NO2 (ľg/m3)', 'NOX (ľg/m3)', 'NO (ľg/m3)', 'PM10 (ľg/m3)', 'PM2,5 (ľg/m3)', 'V.vien (m/s)',
                    'Tş (şC)',  'D.vien (grados)', 'H (%)','End']


for i in range(0,len(csv_files)):
#for i in range(7,8):
    os.chdir('C:/omnetpp-5.2.1/workbench/flora/simulations/stations')
    print(csv_files[i])
    estaciones = pd.read_csv(csv_files[i], sep=';',encoding='iso8859_2', decimal=',')
    #estaciones = pd.read_csv('ALONSOTEGI.csv', sep=';',encoding='iso8859_2', decimal=',')
    estaciones2 = pd.DataFrame(columns=newNames)

    for j in range(0,len(original_delete)):
        if original_delete[j] in estaciones.columns:
            estaciones = estaciones.drop(columns=original_delete[j])

    #print(estaciones)

    for j in range(0,estaciones.columns.size):
        for k in range(0,len(original_modify)):
            if estaciones.columns[j] in original_modify[k]:
                estaciones = estaciones.rename(index=str, columns={estaciones.columns[j]: newNames[k]})


    #print(estaciones.to_string())

    var = [None] * len(newNames)
    for j in range(0,len(newNames)):
        for k in range(0, estaciones.columns.size):
            if newNames[j] is estaciones.columns[k] and var[j] is None:
                #print("Coincide-> newNames[" +str(j)+ "]: "+newNames[j]+ " y estaciones.columns.size["+str(k)+"]: "
                #      + estaciones.columns[k])
                var[j] = k
    #print(var)
    for j in range(0,len(var)):
        if var[j] is None:
            estaciones2[newNames[j]] = [-999.0] * len(estaciones.index)
        else:
            estaciones2[newNames[j]] = estaciones[newNames[j]].tolist()


    estaciones2 = estaciones2.fillna(-999)
    #estaciones2 = estaciones2.drop['Date']
    #print(estaciones2.shape)
    #print(estaciones2.to_string())


    os.chdir('C:/omnetpp-5.2.1/workbench/flora/simulations/')

    var2 = 'Temp' + str(i) + '.csv'
    estaciones2.to_csv(var2, index=False, header=False)