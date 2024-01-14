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



def obtener_cines():
    cursor = cnx.cursor()
    cursor.execute("SELECT id, RazonSocial  FROM cine ORDER BY id ASC")
    lista_de_cines = [{'id': row[0], 'RazonSocial': row[1], 'Direccion':[2], 'Detalle':[3], 'Telefonos':[4] } for row in cursor.fetchall()]
    cursor.close()
    return lista_de_cines

def obtener_peliculas():
    cursor = cnx.cursor()
    cursor.execute("SELECT id, Titulo, Sinopsis, Link  FROM pelicula ORDER BY id ASC")
    lista_de_peliculas = [{'id': row[0], 'Titulo': row[1], 'Sinopsis':[2], 'Link':[3]} for row in cursor.fetchall()]
    cursor.close()
    return lista_de_peliculas

@app.route('/')

def index():

   print(url_for('index'))
   print(url_for('cines'))
   print(url_for('peli'))
   print(url_for('peliculas'))


   return render_template('index.html')


@app.route('/cines')

def cines():
   lista_de_cines = obtener_cines()
   cursor = cnx.cursor(dictionary=True)
   cursor.callproc('sp_getCines')
   for data in cursor.stored_results():
      
      cines = data.fetchall()
      
   cursor.close()
      #return cines
   return render_template('cines.html', cines=cines)


@app.route('/peliculas&id=cartelera')

def peli():
   
   lista_peliculas = obtener_peliculas()

   cursor = cnx.cursor(dictionary=True)

   cursor.callproc('sp_getPeliculass')

   for data in cursor.stored_results():

      peliculas = data.fetchall()
   cursor.close()
   
   return render_template('peliculas.html', peliculas=peliculas)


@app.route('/pelicula&id=<idd>')

def peliculas(idd):

   lista_peliculas = obtener_peliculas()

   cursor = cnx.cursor(dictionary=True)
   
   try:
      cursor.callproc('sp_getPelicula', (idd, ))
      for data in cursor.stored_results():
            pelicula = data.fetchall()
   finally:
      cursor.close() 
   return render_template('pelicula.html', pelicula=pelicula)
   

@app.route('/cine&id=<cine_id>')
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

   cursor.callproc('sp_getCine', (cine_id, ))
   for data in cursor.stored_results():
      
      cines = data.fetchall()

   return render_template('cine.html', tarifas=tarifas, horarios=horarios, cines=cines)

   cursor.close()




if __name__ == '__main__':

   app.run(debug=True, port=5000)



