import pandas as pd

estaciones = pd.read_csv('C:/omnetpp-5.2.1/workbench/flora/simulations/estaciones.csv', sep=';',encoding='iso8859_2', decimal=',');
print(estaciones.shape)
longLat = pd.read_csv('C:/omnetpp-5.2.1/workbench/flora/simulations/dataSet4.csv')

estaciones = estaciones.drop(columns=['Province', 'Address','Coordenates X (ETRS89)', 'Coordenates Y (ETRS89)','Longitude','Latitude'])
print(estaciones.shape)

estaciones['Description'] = estaciones['Town'] + ' - ' + estaciones['Name']
estaciones = estaciones.drop(columns = 'Town')

estaciones['Longitude'] = longLat['lat'][0:estaciones.shape[0]]
estaciones['Latitude'] = longLat['long'][0:estaciones.shape[0]]

print(estaciones.columns.values)
estaciones.to_csv('C:/omnetpp-5.2.1/workbench/flora/simulations/estaciones2.csv',index=False,encoding='utf-8')
