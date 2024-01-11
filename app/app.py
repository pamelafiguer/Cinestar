from flask import Flask, render_template, url_for
import mysql.connector

app = Flask (__name__)

config = {
     'host' : 'localhost',
     'user' : 'root',
     'password' : '',
     'database' : 'cinestar' 
}

configRemote = {
     'host' : 'srv1101.hstgr.io',
     'user' : 'u584908256_cinestar',
     'password' : 'Senati2023@',
     'database' : 'u584908256_cinestar' 
}

cnx = mysql.connector.connect(**config)

@app.route('/')
def index():
     print(url_for('index'))
     print(url_for('cines'))
     print(url_for('peliculas'))
     print(url_for('nombre', id = '1'))
     print(url_for('cines', nombre = 'print(CinestarExcelsior)'))

     
     return render_template('index.html')


@app.route('/cines')
def cines():
     cursor = cnx.cursor(dictionary=True)
     cursor.callproc('sp_getCines')
     for data in cursor.stored_results():
          cines = data.fetchall()
     cursor.close()
     #return cines
     return render_template('cines.html', cines=cines)

@app.route('/cartelera')
def peliculas():
     
     cursor = cnx.cursor(dictionary=True)
     cursor.callproc('sp_getPeliculass')
     for data in cursor.stored_results():
          peliculas = data.fetchall()
     cursor.close()
     #return peliculas
     return render_template('peliculas.html', peliculas=peliculas)

@app.route('/peliculas/cartelera/<id>')
def nombre(id):
     cursor = cnx.cursor(dictionary=True)
     cursor.callproc('sp_getPelicula', (1, ))
     for data in cursor.stored_results():
          nombre = data.fetchall()
     cursor.close()
     #return nombre
     return render_template('pelicula.html', pelicula=nombre)


@app.route('/cines/<nombre>')
def cine(nombre):
     cursor = cnx.cursor(dictionary=True)
     cursor.callproc('sp_getCineTarifas',(1, ))
     cursor.callproc('sp_getCinePeliculas',(1, ))
     cursor.callproc('sp_getCines')
     for data in cursor.stored_results():
          cine = data.fetchall()
     cursor.close()
     #return cine
     return render_template('cine.html', cine=cine)


if __name__ == '__main__':
    app.run(debug=True, port=5000)


