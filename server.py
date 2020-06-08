from flask import Flask,g,jsonify
from flask import request
import psycopg2
from psycopg2 import pool

app = Flask(__name__)

app.config['postgreSQL_pool'] = psycopg2.pool.SimpleConnectionPool(1, 20,user = "postgres",password = "postgres",host = "db",port = "5432",database = "postgres")

def get_db():
    if 'db' not in g:
        g.db = app.config['postgreSQL_pool'].getconn()
    return g.db

@app.teardown_appcontext
def close_conn(e):
    print('CLOSING CONN')
    db = g.pop('db', None)
    if db is not None:
        app.config['postgreSQL_pool'].putconn(db)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/positionbyID')
def positionbyID():
    idFromTrunkToLookup=request.args.get('trukId', default = 1)
    jsonforResponse={}
    if idFromTrunkToLookup == 1:
        errorMessage="error in request trukId is required"
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from datosdummy where idunidad='"+idFromTrunkToLookup+"'")
        result = cursor.fetchall()
        counterForResponse=0
        #iterate over query results and setting up the response
        for row in result:
            if counterForResponse == 0:
                jsonforResponse={"idUnidad":row[0], "location": [{"latitud": row[1], "longitud":row[2], "timestamp": row[3]}]}
                counterForResponse=counterForResponse+1
            else:
                jsonforResponse['location'].append({"latitud": row[1], "longitud":row[2], "timestamp": row[3]})
                counterForResponse=counterForResponse+1
        print (result)
        cursor.close()
        if not(jsonforResponse):
            #response in case that there are not values that match
            jsonforResponse={"error": -50, "errorMessage": "there are not match with query"}
    return jsonify(jsonforResponse)

@app.route('/unitsavailable')
def unitsabilable():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select idunidad from datosdummy group by idunidad")
    result = cursor.fetchall()
    counterForResponse=0
    #iterate over query results and setting up the response
    for row in result:
        if counterForResponse == 0:
            jsonforResponse={"idUnidad":[row[0]],}
            counterForResponse=counterForResponse+1
        else:
            jsonforResponse['idUnidad'].append(row[0])
            counterForResponse=counterForResponse+1
    cursor.close()
    return jsonify(jsonforResponse)

@app.route('/alcaldiasavailable')
def alcaldiasavailable():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select alcaldia from datosdummy group by alcaldia")
    result = cursor.fetchall()
    counterForResponse=0
    #iterate over query results and setting up the response
    for row in result:
        if counterForResponse == 0:
            jsonforResponse={"alcaldias":[row[0]],}
            counterForResponse=counterForResponse+1
        else:
            jsonforResponse['alcaldias'].append(row[0])
            counterForResponse=counterForResponse+1
    cursor.close()
    return jsonify(jsonforResponse)

@app.route('/unitsperalcaldia')
def unitsperalcaldia():
    nombreDeAlcaldia=request.args.get('alcaldia', default = "default")
    jsonforResponse={}
    if(nombreDeAlcaldia == "default"):
        errorMessage="error in request trukId is required"
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select idunidad from datosdummy where alcaldia='"+nombreDeAlcaldia+"' group by idunidad")
        result = cursor.fetchall()
        print(result)
        counterForResponse=0
        #iterate over query results and setting up the response
        for row in result:
            if counterForResponse == 0:
                jsonforResponse={"alcaldia":nombreDeAlcaldia, "idUnidesdes": [row[0]]}
                counterForResponse=counterForResponse+1
            else:
                jsonforResponse['idUnidesdes'].append(row[0])
                counterForResponse=counterForResponse+1
        cursor.close()
        if not(jsonforResponse):
            #response in case that there are not values that match
            jsonforResponse={"error": -50, "errorMessage": "there are not match with query"}
    return jsonify(jsonforResponse)
