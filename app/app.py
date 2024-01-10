from flask import Flask, render_template
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

@app.route('/peliculas/cartelera')
def peliculas():
     cursor = cnx.cursor(dictionary=True)
     cursor.callproc('sp_getPeliculass')
     for data in cursor.stored_results():
          peliculas = data.fetchall()
     cursor.close()
     #return cartelera
     return render_template('peliculas.html', peliculas=peliculas)

@app.route('/peliculas/cartelera/pelicula')
def pelicula():
     cursor = cnx.cursor(dictionary=True)
     cursor.callproc('sp_getPelicula', (1,))
     for data in cursor.stored_results():
          pelicula = data.fetchall()
     cursor.close()
     #return pelicula
     return render_template('pelicula.html', pelicula=pelicula)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


