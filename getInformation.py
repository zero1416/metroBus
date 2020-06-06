import requests
import psycopg2
import datetime
import time

r = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&q=&rows=50')
jsonDerespuestaMetrobus=r.json()
ArrayOfAlcaldias=["Iztapalapa", "Iztacalco","Tlalpan","Miguel Hidalgo","Gustavo A. Madero","Benito Juárez","Coyoacán","Cuauhtémoc","Venustiano Carranza","Azcapotzalco"]
for numeroDeRegistro in  jsonDerespuestaMetrobus['records']:
    idveiculo= numeroDeRegistro['fields']['vehicle_id']
    longitud= numeroDeRegistro['fields']['position_longitude']
    latitud= numeroDeRegistro['fields']['position_latitude']
    fecha=numeroDeRegistro['fields']['date_updated']
    print("request antes de enviar a google")
    latitudAndlogtitudForRequest=str(latitud)+','+str(longitud)
    requestValuesFromGoogle={'latlng': latitudAndlogtitudForRequest,'key':''}
    print(requestValuesFromGoogle)
    requestAlcaldia=requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=requestValuesFromGoogle)
    jsonDerespuestaAlcaldia=requestAlcaldia.json()
    print('despues de peticion')
    fullAddress=jsonDerespuestaAlcaldia['results'][1]['formatted_address']
    arrayofAddress=fullAddress.split(',')
    print(arrayofAddress)
    timestampFromRequest=time.mktime(datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").timetuple())
    if not(arrayofAddress[2].strip() in ArrayOfAlcaldias):
        fullAddress=jsonDerespuestaAlcaldia['results'][0]['formatted_address']
        arrayofAddress=fullAddress.split(',')
        print("delegacion no valida nueva delegacion:"+arrayofAddress[2])
        #arrayofAddress[2]="default"
    try:
        connection = psycopg2.connect(user="postgres",password="postgres",host="db",port="5432",database="postgres")

        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO datosdummy (idunidad, latitud, longitud,timestamp,alcaldia) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (idveiculo, latitud, longitud, timestampFromRequest,arrayofAddress[2].strip())
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)


    #closing database connection.
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
