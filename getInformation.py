import requests

r = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&q=vehicle_id%3D450')
jsonDerespuesta=r.json()
for numeroDeRegistro in  jsonDerespuesta['records']:
    print numeroDeRegistro['fields']['vehicle_id']
    print numeroDeRegistro['fields']['position_longitude']
    print numeroDeRegistro['fields']['position_latitude']
