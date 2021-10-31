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
    return render_template("index.html", data=data, id_oculto="", nombre="")

@app.route('/<id>')
def index2(id):
    
    collection = db['autor']
    results = list(collection.find())
    data = {autor['nombre']: autor['_id'] for autor in results}
    
    nombre = list(collection.find({'_id' : ObjectId(id)}))[0]['nombre']
    
    return render_template("index.html", data=data, id_oculto=id, nombre=nombre)

@app.route('/createAutor', methods=['POST'])
def create_autor():
    collection = db['autor']

    nombre_autor = request.form['nombre']
    try:
        collection.insert_one({"nombre": nombre_autor})
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
    id_autor = request.form['id_oculto']
    
    nombre_autor_viejo = list(collection.find({'_id': ObjectId(id_autor)}))[0]['nombre']

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
    return render_template("libro.html", data=data, nombre="", id_oculto="")

@app.route('/libro/<id>')
def libro2(id):
    
    collection = db['libro']
    results = list(collection.find())
    data = {libro['titulo']: libro['_id'] for libro in results}
    nombre = list(collection.find({'_id' : ObjectId(id)}))[0]['titulo']
    return render_template("libro.html", data=data, id_oculto=id, nombre=nombre)

@app.route('/createLibro', methods=['POST'])
def create_libro():
    collection = db['libro']

    nombre_libro = request.form['titulo']
    try:
        collection.insert_one({"titulo": nombre_libro})
    except Exception:
        print(Exception)
    finally:
        return redirect(url_for('libro'))

@app.route('/deleteLibro/<id>')
def delete_libro(id):
    collection = db['libro']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception:
        print(Exception)
    finally:
        return redirect(url_for('libro'))

@app.route('/updateLibro', methods=['POST'])
def update_libro():
    collection = db['libro']
    titulo_libro_nuevo = request.form['titulo']
    id_libro = request.form['id_oculto']
    
    titulo_libro_viejo = list(collection.find({'_id': ObjectId(id_libro)}))[0]['titulo']

    try:
        collection.update_one({'_id': ObjectId(id_libro)}, {'$set': {'titulo': titulo_libro_nuevo}})
        collection2 = db['autorea']
        collection2.update_many({'titulo': titulo_libro_viejo}, {'$set': {'titulo': titulo_libro_nuevo}})
        collection3 = db['edicion']
        collection3.update_one({'titulo': titulo_libro_viejo}, {'$set': {'titulo': titulo_libro_nuevo}})
    except Exception:
        print(Exception)
    finally:
        return redirect(url_for('libro'))

@app.route('/edicion')
def edicion():
    collection = db['edicion']
    results = list(collection.find())
    data = []
    for edicion in results:
       data.append([edicion['_id'],edicion['isbn'],edicion['año'],edicion['idioma'],edicion['titulo']])
    return render_template("edicion.html", data=data)

@app.route('/copia')
def copia():
    collection = db['copia']
    results = list(collection.find())
    data = []
    for copia in results:
        data.append([copia['_id'],copia['isbn'],copia['numero']])
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
        data.append([prestamo['_id'],prestamo['isbn'],prestamo['numero'],prestamo['rut'],prestamo['fecha_prestamo'],prestamo['fecha_devolucion']])
    return render_template("prestamo.html", data=data)

@app.route('/consultaL')
def consultaL():
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
                    {'_id':0,'autor':"$autores.nombre",'libro':"$titulo_libro.titulo",'isbn':"$titulo_libro.isbn", 'idioma':"$titulo_libro.idioma", 'ano':'$titulo_libro.año', 'copia':"$numero"}} 
    ]
    results = db.copia.aggregate(pipeline)

    data = []
    for row in results:
        data.append([row['autor'][0], row['libro'], int(row['isbn']), row['idioma'], int(row['ano']), int(row['copia'])])
        
    return render_template("consultaL.html", data=data)

@app.route('/consultaU')
def consultaU():
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
    
    data = {}
    for row in results:
        data[row['nombre']] = data.get(row['nombre'], []) + [row['titulo']]
    
    s={}
    for nombre,libros in data.items():
        s[nombre] = ', '.join([libro for libro in libros])
    
    return render_template("consultaU.html", data=s)




