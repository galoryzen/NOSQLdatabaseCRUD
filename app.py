from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)


MONGO_URI = 'mongodb://localhost'
client = MongoClient(MONGO_URI)
db = client['biblioteca']


@app.route('/')
def index():
    collection = db['autor']
    results = list(collection.find())
    data = {autor['nombre']: autor['_id'] for autor in results}
    return render_template("index.html", data=data)

@app.route('/libro')
def libro():

    return render_template("libro.html")

@app.route('/edicion')
def edicion():

    return render_template("edicion.html")

@app.route('/copia')
def copia():

    return render_template("copia.html")

@app.route('/usuario')
def usuario():

    return render_template("usuario.html")

@app.route('/prestamo')
def prestamo():

    return render_template("prestamo.html")

@app.route('/consultaL')
def consultaL():

    return render_template("consultaL.html")

@app.route('/consultaU')
def consultaU():

    return render_template("consultaU.html")




















#Consulta1
"""
collection=db['autor']
pipeline = [
    {'$lookup':
        {'from':'edicion',
         'localField':'isbn',
         'foreignField':'isbn',
         'as':'titulo_libro'}},
    {'$unwind': '$titulo_libro'},
    {'$lookup':
        {'from':'autorea',
         'localField':'titulo_libro.titulo',
         'foreignField':'titulo',
         'as':'autores'}},
    {'$project': 
                {'_id':0,'autor':"$autores.nombre",'libro':"$titulo_libro.titulo",'edicion':"$isbn", 'copia':"$numero"}} 
]
results = db.copia.aggregate(pipeline)
"""
#Consulta2
"""
pipeline= [
    {'$lookup':
        {'from':'prestamo',
         'localField':'rut',
         'foreignField':'rut',
         'as':'prestamo_libro'}},
    {'$unwind': '$prestamo_libro'},
    {'$lookup':
        {'from':'copia',
         'localField':'prestamo_libro.isbn',
         'foreignField':'isbn',
         'as':'copia_libro'}},
    {'$unwind': '$copia_libro'},
    {'$lookup':
        {'from':'edicion',
         'localField':'copia_libro.isbn',
         'foreignField':'isbn',
         'as':'edicion_libro'}},
    {'$unwind': '$edicion_libro'},
    {'$project': 
                {'_id':0,'nombre':"$nombre", 'rut':"$rut",'titulo':"$edicion_libro.titulo"}}
]

results = db.usuario.aggregate(pipeline)
"""