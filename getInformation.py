import requests
import psycopg2
import datetime
import time

#get all information for api its set a 50 rows for test propose
r = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&q=&rows=50')
jsonResponseFromAPI=r.json()
ArrayOfAlcaldias=["Iztapalapa", "Iztacalco","Tlalpan","Miguel Hidalgo","Gustavo A. Madero","Benito Juárez","Coyoacán","Cuauhtémoc","Venustiano Carranza","Azcapotzalco"]
#iterate over the list of responses that gives you the api
for singleResponseFromAPI in  jsonResponseFromAPI['records']:
    #save all values to inser into DB
    idveiculo= singleResponseFromAPI['fields']['vehicle_id']
    longitud= singleResponseFromAPI['fields']['position_longitude']
    latitud= singleResponseFromAPI['fields']['position_latitude']
    fecha=singleResponseFromAPI['fields']['date_updated']
    latitudAndlogtitudForRequest=str(latitud)+','+str(longitud)
    requestValuesFromGoogle={'latlng': latitudAndlogtitudForRequest,'key':''}
    #send request to google to get alcaldia from coordenates
    requestAlcaldia=requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=requestValuesFromGoogle)
    jsonResponseFromGoogle=requestAlcaldia.json()
    #iterate over google response because not al response has the same data
    for eachAddressInGoogleReponse in jsonResponseFromGoogle['results']:
        fullAddressAfterSplit=eachAddressInGoogleReponse['formatted_address'].split(',')
        #check if Alcaldia is in the list defined previsusly
        if fullAddressAfterSplit[2].strip() in ArrayOfAlcaldias:
            addressToAddInDB=fullAddressAfterSplit[2].strip()
            break
        elif fullAddressAfterSplit[3].strip() in ArrayOfAlcaldias:
            addressToAddInDB=fullAddressAfterSplit[3].strip()
            break
    timestampFromRequest=time.mktime(datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").timetuple())
    #convert date to timestamp that makeit easy to handle
    try:
        #get connetion for postgres
        connection = psycopg2.connect(user="postgres",password="postgres",host="db",port="5432",database="postgres")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO datosdummy (idunidad, latitud, longitud,timestamp,alcaldia) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (idveiculo, latitud, longitud, timestampFromRequest,addressToAddInDB)
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
