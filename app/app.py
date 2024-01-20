from flask import Flask, render_template, url_for

import mysql.connector


app = Flask (__name__)

config = {

   'host' : 'localhost',

   'user' : 'root',

   'password' : '',

   'database' : 'CineStar' 

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

#direciones web
   print(url_for('index'))
   print(url_for('cines'))
   print(url_for('cartelera'))
   print(url_for('peliculas', idd = id))
   print(url_for('estrenos'))
   return render_template('index.html')


@app.route('/cines')
def cines():
   cursor = cnx.cursor(dictionary=True)
   cursor.callproc('sp_getCines')
   for data in cursor.stored_results():
      cines = data.fetchall()
   cursor.close()
   return render_template('cines.html', cines=cines)



@app.route('/peliculas/cartelera')
def cartelera():
   cursor = cnx.cursor(dictionary=True)
   cursor.callproc('sp_getPeliculass')
   for data in cursor.stored_results():
      peliculas = data.fetchall()
   cursor.close()
   return render_template('peliculas.html', peliculas=peliculas)

@app.route('/peliculas/estrenos')
def estrenos():
   cursor = cnx.cursor(dictionary=True)
   cursor.callproc('sp_getPeliculasEstrenos')
   for data in cursor.stored_results():
      estrenos = data.fetchall()
   cursor.close()
   return render_template('estrenos.html', estrenos = estrenos)


@app.route('/pelicula/id=<idd>')
def peliculas(idd):
   cursor = cnx.cursor(dictionary=True)
   cursor.callproc('sp_getPelicula', [idd, ])
   for data in cursor.stored_results():
      pelicula = data.fetchall()
      cursor.close() 
   return render_template('pelicula.html', pelicula=pelicula, idd=idd)
   

@app.route('/cine/id=<cine_id>')
def cine(cine_id):
   cursor = cnx.cursor(dictionary=True)
   cursor.callproc('sp_getCineTarifas', (cine_id, ))
   for data in cursor.stored_results():
      tarifas = data.fetchall()
   cursor.nextset()
   
   cursor.callproc('sp_getCinePeliculas', (cine_id, ))
   for data in cursor.stored_results():
      horarios = data.fetchall()
   cursor.nextset()
   
   query = "select * from Cine where id = %s" 
   cursor.execute(query, (cine_id,))
   cines = cursor.fetchone()
   cursor.nextset()
   cursor.close()
   
   return render_template('cine.html', tarifas=tarifas, horarios=horarios, cines=cines, cine_id=cine_id)


if __name__ == '__main__':
   app.run(debug=True, port=5000)



