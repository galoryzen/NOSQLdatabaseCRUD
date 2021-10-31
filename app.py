from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
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

@app.route('/createAutor', methods=['POST'])
def create_autor():
    collection = db['autor']

    nombre_padre = request.form['nombre']
    try:
        collection.insert_one({"nombre": nombre_padre})
    except Exception:
        print(Exception)
    finally:
        return redirect(url_for('index'))
    
    
@app.route('/deleteAutor/<id>')
def delete_autor(id):
    collection = db['autor']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception:
        print(Exception)
    finally:
        return redirect(url_for('index'))
    
@app.route('/updateAutor', methods=['POST'])
def update_autor():
    collection = db['autor']
    nombre_autor_nuevo = request.form['nombre']
    id_autor = request.form['id']
    
    nombre_autor_viejo = collection.find({'_id': ObjectId(id_autor)})['nombre']

    try:
        collection.update_one({'_id': ObjectId(id_autor)}, {'$set': {'nombre': nombre_autor_nuevo}})
        collection2 = db['autorea']
        collection2.update_many({'nombre': nombre_autor_viejo}, {'$set': {'nombre': nombre_autor_nuevo}})
    except Exception:
        print(Exception)
    finally:
        return redirect(url_for('index'))

@app.route('/libro')
def libro():
    collection = db['libro']
    results = list(collection.find())
    data = {libro['titulo']: libro['_id'] for libro in results}
    return render_template("libro.html", data=data)

@app.route('/edicion')
def edicion():
    collection = db['edicion']
    results = list(collection.find())
    for edicion in results:
       data = data.append([edicion['_id'],edicion['isbn'],edicion['aÃ±o'],edicion['idioma'],edicion['titulo']])
    return render_template("edicion.html", data=data)
    return render_template("edicion.html")

@app.route('/copia')
def copia():
    collection = db['copia']
    results = list(collection.find())
    data = []
    for copia in results:
        data = data.append([copia['_id'],copia['isbn'],copia['numero']])
    return render_template("copia.html", data=data)

@app.route('/usuario')
def usuario():
    collection = db['usuario']
    results = list(collection.find())
    data = []
    for result in results:
        data.append((result['_id'], int(result['rut']), result['nombre']))
    return render_template("usuario.html", data=data)

@app.route('/prestamo')
def prestamo():
    collection = db['prestamo']
    results = list(collection.find())
    data = []
    for prestamo in results:
        data = data.append([prestamo['_id'],prestamo['isbn'],prestamo['numero'],prestamo['rut'],prestamo['fecha_prestamo'],prestamo['fecha_devolucion']])
    return render_template("prestamo.html", data=data)

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