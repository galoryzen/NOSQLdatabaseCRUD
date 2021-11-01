from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from datetime import date, datetime

app = Flask(__name__)


MONGO_URI = 'mongodb://localhost'
client = MongoClient(MONGO_URI)
db = client['biblioteca']

@app.route('/')
def init():
    return redirect(url_for('index'))

@app.route('/autor')
def index():
    collection = db['autor']
    results = list(collection.find())
    data = {autor['nombre']: autor['_id'] for autor in results}
    return render_template("index.html", data=data, id_oculto="", nombre="")

@app.route('/autor/<id>')
def index2(id):
    
    collection = db['autor']
    results = list(collection.find())
    data = {autor['nombre']: autor['_id'] for autor in results}
    
    try:
        id = ObjectId(id)
    except:
        return render_template("index.html", data=data, id_oculto='', nombre='')
    
    nombre = collection.find({'_id': id})[0]['nombre']
    
    return render_template("index.html", data=data, id_oculto=id, nombre=nombre)

@app.route('/createAutor', methods=['POST'])
def create_autor():
    collection = db['autor']

    nombre_autor = request.form['nombre']
    try:
        collection.insert_one({"nombre": nombre_autor})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('index'))
    
    
@app.route('/deleteAutor/<id>')
def delete_autor(id):
    collection = db['autor']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('libro'))

@app.route('/deleteLibro/<id>')
def delete_libro(id):
    collection = db['libro']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('libro'))

@app.route('/edicion')
def edicion():
    collection = db['edicion']
    results = list(collection.find())
    data = []
    for edicion in results:
       data.append([int(edicion['isbn']),int(edicion['año']),edicion['idioma'],edicion['titulo'],edicion['_id']])
    return render_template("edicion.html", data=data, input=['', '', '', ''])

@app.route('/edicion/<id>')
def edicion2(id):
    
    collection = db['edicion']
    results = list(collection.find())
    data = []
    for edicion in results:
        data.append([int(edicion['isbn']),int(edicion['año']),edicion['idioma'],edicion['titulo'],edicion['_id']])
        
    dic = list(collection.find({'_id': ObjectId(id)}))[0]
    
    return render_template("edicion.html", data=data, id_oculto=id, input=[int(dic['isbn']), int(dic['año']), dic['idioma'], dic['titulo']])

@app.route('/createEdicion', methods=['POST'])
def create_edicion():
    collection = db['edicion']

    isbn = request.form['isbn']
    ano = request.form['año']
    idioma = request.form['idioma']
    titulo = request.form['titulo']
    
    try:
        collection.insert_one({'isbn': int(isbn), 'año': ano, 'idioma': idioma, 'titulo': titulo})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('edicion'))

@app.route('/deleteEdicion/<id>')
def delete_edicion(id):
    collection = db['edicion']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('edicion'))

@app.route('/updateEdicion', methods=['POST'])
def update_edicion():
    collection = db['edicion']

    isbn = request.form['isbn']
    ano = request.form['año']
    idioma = request.form['idioma']
    titulo = request.form['titulo']
    id = request.form['id_oculto']
    
    dic = list(collection.find({'_id': ObjectId(id)}))[0]
    isbn_anterior = dic['isbn']

    try:
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'isbn': int(isbn), 'año': ano, 'idioma': idioma, 'titulo': titulo}})
        collection2 = db['copia']
        collection2.update_many({'isbn': isbn_anterior}, {'$set': {'isbn': int(isbn)}})
        collection3 = db['prestamo']
        collection3.update_one({'isbn': isbn_anterior}, {'$set': {'isbn': int(isbn)}})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('edicion'))


@app.route('/copia')
def copia():
    collection = db['copia']
    results = list(collection.find())
    data = []
    for copia in results:
        data.append([int(copia['isbn']),copia['numero'],copia['_id']])
    return render_template("copia.html", data=data, numero='', isbn='', id_oculto='')


@app.route('/copia/<id>')
def copia2(id):
    
    collection = db['copia']
    results = list(collection.find())
    data = []
    for copia in results:
        data.append([int(copia['isbn']),copia['numero'],copia['_id']])
    
    dic = list(collection.find({'_id': ObjectId(id)}))[0]
    
    return render_template("copia.html", data=data, numero=dic['numero'], isbn=int(dic['isbn']), id_oculto=id)

@app.route('/createCopia', methods=['POST'])
def create_copia():
    collection = db['copia']

    isbn = request.form['isbn']
    numero = request.form['numero']
    
    try:
        collection.insert_one({'isbn': int(isbn), 'numero': int(numero)})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('copia'))

@app.route('/deleteCopia/<id>')
def delete_copia(id):
    collection = db['copia']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('copia'))

@app.route('/updateCopia', methods=['POST'])
def update_copia():
    collection = db['copia']

    isbn = request.form['isbn']
    numero = request.form['numero']
    id = request.form['id_oculto']
    
    dic = list(collection.find({'_id': ObjectId(id)}))[0]
    isbn_anterior = dic['isbn']
    numero_anterior = dic['numero']

    try:
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'isbn': int(isbn), 'numero': numero}})
        collection = db['prestamo']
        collection.update_many({'isbn': isbn_anterior, 'numero':numero_anterior}, {'$set': {'isbn': int(isbn), 'numero':numero}})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('copia'))


@app.route('/usuario')
def usuario():
    collection = db['usuario']
    results = list(collection.find())
    data = []
    for result in results:
        data.append([result['_id'], int(result['rut']), result['nombre']])
    return render_template("usuario.html", data=data, rut='', nombre='', id_oculto='')


@app.route('/usuario/<id>')
def usuario2(id):
    
    collection = db['usuario']
    results = list(collection.find())
    data = []
    for result in results:
        data.append([result['_id'], int(result['rut']), result['nombre']])
    
    dic = list(collection.find({'_id': ObjectId(id)}))[0]
    
    return render_template("usuario.html", data=data, rut=dic['rut'], nombre=dic['nombre'], id_oculto=id)

@app.route('/createUsuario', methods=['POST'])
def create_usuario():
    collection = db['usuario']

    rut = request.form['rut']
    nombre = request.form['nombre']
    
    try:
        collection.insert_one({'rut': int(rut), 'nombre': nombre})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('usuario'))

@app.route('/deleteUsuario/<id>')
def delete_usuario(id):
    collection = db['usuario']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('usuario'))

@app.route('/updateUsuario', methods=['POST'])
def update_usuario():
    collection = db['usuario']

    rut = request.form['rut']
    nombre = request.form['nombre']
    id = request.form['id_oculto']
    
    dic = list(collection.find({'_id': ObjectId(id)}))[0]
    rut_anterior = dic['rut']

    try:
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'rut': int(rut), 'nombre': nombre}})
        collection = db['prestamo']
        collection.update_many({'rut': rut_anterior}, {'$set': {'rut': int(rut)}})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('usuario'))

@app.route('/prestamo')
def prestamo():
    collection = db['prestamo']
    results = list(collection.find())
    data = []
    for prestamo in results:
        data.append([prestamo['_id'],prestamo['numero'],int(prestamo['isbn']),prestamo['rut'],prestamo['fecha_prestamo'],prestamo['fecha_devolucion']])
    return render_template("prestamo.html", data=data, input=['', '', '', 'Ej: 2021-05-14', 'Ej: 2021-11-24'])

@app.route('/prestamo/<id>')
def prestamo2(id):
    
    collection = db['prestamo']
    results = list(collection.find())
    data = []
    for prestamo in results:
        data.append([prestamo['_id'],prestamo['numero'],int(prestamo['isbn']),prestamo['rut'],prestamo['fecha_prestamo'],prestamo['fecha_devolucion']])
    
    dic = list(collection.find({'_id': ObjectId(id)}))[0]
    
    return render_template("prestamo.html", data=data, input=[dic['numero'], dic['isbn'], dic['rut'], dic['fecha_prestamo'].date(), dic['fecha_devolucion'].date()], id_oculto=id)

@app.route('/createPrestamo', methods=['POST'])
def create_prestamo():
    collection = db['prestamo']

    numero = request.form['numero']
    isbn = request.form['isbn']
    rut = request.form['rut']
    fp = [int(part) for part in request.form['fecha_prestamo'].split('-')]
    fd = [int(part) for part in request.form['fecha_devolucion'].split('-')]
    
    try:
        collection.insert_one({'numero': int(numero), 'isbn': int(isbn), 'rut': int(rut), 'fecha_prestamo': datetime(fp[0], fp[1], fp[2], 5, 0), 'fecha_devolucion': datetime(fd[0], fd[1], fd[2], 5, 0)})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('prestamo'))
    
@app.route('/deletePrestamo/<id>')
def delete_prestamo(id):
    collection = db['prestamo']
    
    try:
        collection.delete_one({'_id': ObjectId(id)})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('prestamo'))
    
@app.route('/updatePrestamo', methods=['POST'])
def update_prestamo():
    collection = db['prestamo']

    numero = request.form['numero']
    isbn = request.form['isbn']
    rut = request.form['rut']
    fp = [int(part) for part in request.form['fecha_prestamo'].split('-')]
    fd = [int(part) for part in request.form['fecha_devolucion'].split('-')]
    id = request.form['id_oculto']

    try:
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'numero': int(numero), 'isbn': int(isbn), 'rut': int(rut), 'fecha_prestamo': datetime(fp[0], fp[1], fp[2], 5, 0), 'fecha_devolucion': datetime(fd[0], fd[1], fd[2], 5, 0)}})
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('prestamo'))

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


