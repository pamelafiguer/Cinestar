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
cursor = cnx.cursor(dictionary=True)



@app.route('/')
def index():
   return render_template('index.html')


@app.route('/cines')
def cines():
   cursor.callproc('sp_getCines')
   for data in cursor.stored_results():
      cines = data.fetchall()
   return render_template('cines.html', cines=cines, id = id)




@app.route('/cine/<int:id>')
def cine(id):
   cursor.callproc('sp_getCineTarifas', (id, ))
   for data in cursor.stored_results():
      tarifas = data.fetchall()
   
   cursor.callproc('sp_getCinePeliculas', (id, ))
   for data in cursor.stored_results():
      horarios = data.fetchall()
   
   cursor.callproc('sp_getCine', (id, ))
   for data in cursor.stored_results():
      cines = data.fetchall()
   
   return render_template('cine.html', tarifas=tarifas, horarios=horarios, cines=cines, id=id)



@app.route('/peliculas/<id>')
def peliculas(id):
   id = 1 if id == 'cartelera' else 2 if id  == 'estrenos' else 0 
   if id == 0 : 
      return render_template('index.html')
   
   if id == 1:
         cursor.callproc('sp_getPeliculass')
         for data in cursor.stored_results():
            peliculas = data.fetchall()
         return render_template('peliculas.html', peliculas = peliculas)
   if id == 2:
         cursor.callproc('sp_getPeliculasEstrenoss')
         for data in cursor.stored_results():
            estrenos = data.fetchall()
         return render_template('estrenos.html', estrenos = estrenos)
   
   




@app.route('/pelicula/<int:id>')
def pelicula(id):
   #cursor.execute("select * from pelicula where id = %s", (id,))
   cursor.callproc('sp_getPelicula',(id, ))
   for data in cursor.stored_results(): 
      pelicula = data.fetchall()
   return render_template('pelicula.html', pelicula=pelicula, id = id)

   cursor.close()

if __name__ == '__main__':
   app.run(debug=True, port=5000)



