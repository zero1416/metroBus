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
    if idFromTrunkToLookup == 1:
        errorMessage="error in request trukId is required"
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from datosdummy where idunidad='"+idFromTrunkToLookup+"'")
        result = cursor.fetchall()
        counterForResponse=0
        for row in result:
            if counterForResponse == 0:
                jsonforResponse={"idUnidad":row[0], "location": [{"latitud": row[1], "longitud":row[2], "timestamp": row[3]}]}
                counterForResponse=counterForResponse+1
            else:
                jsonforResponse['location'].append({"latitud": row[1], "longitud":row[2], "timestamp": row[3]})
                counterForResponse=counterForResponse+1
        print (result)
        cursor.close()

    return jsonify(jsonforResponse)

@app.route('/unitsabilable')
def unitsabilable():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select idunidad from datosdummy group by idunidad")
    result = cursor.fetchall()
    counterForResponse=0
    for row in result:
        if counterForResponse == 0:
            jsonforResponse={"idUnidad":[row[0]],}
            counterForResponse=counterForResponse+1
        else:
            jsonforResponse['idUnidad'].append(row[0])
            counterForResponse=counterForResponse+1
    cursor.close()
    return jsonify(jsonforResponse)
