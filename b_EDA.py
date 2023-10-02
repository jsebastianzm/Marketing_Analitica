
import pandas as pd
import sqlite3 as sql ### para conectarse a BD
from mlxtend.preprocessing import TransactionEncoder
import plotly.graph_objs as go ### para gráficos
import plotly.express as px
import a_funciones as fn

##### conectarse a BD #######
conn= sql.connect('Datos\db_movies_2')
cur=conn.cursor()

### para ver las tablas que hay en la base de datos
cur.execute("select name from sqlite_master where type='table' ")
cur.fetchall()


# consulta_sql = """
#     SELECT SUBSTR(genres, 1, INSTR(genres, '|') - 1) AS genero, COUNT(*) AS total_peliculas
#     FROM movies
#     GROUP BY genero
#     ORDER BY total_peliculas DESC
# """

consulta_sql = """
    SELECT *
    FROM ratings
"""
ratings = pd.read_sql(consulta_sql, conn)

consulta_sql = """
    SELECT *
    FROM movies
"""
movies = pd.read_sql(consulta_sql, conn)




#####Exploración inicial #####

### Identificar campos de cruce y verificar que estén en mismo formato ####
### verificar duplicados

ratings.info()
ratings.head()
ratings.duplicated().sum() 

movies.info()
movies.head()
movies.duplicated().sum() 

ratings.rating.unique()

consulta_sql = """
    SELECT rating, COUNT(*) AS n_movies
    FROM ratings
    GROUP BY rating
    ORDER BY n_movies DESC
"""
###calcular la distribución de calificaciones
cr=pd.read_sql(consulta_sql, conn)


###Nombres de columnas con numeros o guiones se deben poner en doble comilla para que se reconozcan
#Se analiza la calificación dada a las peliculas por los usuarios
data  = go.Bar( x=cr.rating,y=cr.n_movies, text=cr.n_movies, textposition="outside")
Layout=go.Layout(title="Count of ratings",xaxis={'title':'Rating'},yaxis={'title':'Count movies'})
go.Figure(data,Layout)



consulta_sql = """
        SELECT userId as user, COUNT(*) AS n_id
        FROM ratings
        GROUP BY userId
        ORDER BY n_id asc
"""

### calcular cada usuario cuátas peliculas calificó
rating_users=pd.read_sql(consulta_sql, conn )

### Se visualiza que hay algunos valores exrtemos, por lo que serían personas que han visto más de 2000 peliculas, estos valores se pueden tomar
### como atipicos y se podrían llegar a reducir hasta un total de 600 peliculas desde mi punto de vista y siguiendo los valores dados por las descripción
### de los userId.
fig  = px.histogram(rating_users, x= 'n_id', title= 'Hist frecuencia de numero de calificaciones por usario')
fig.show() 


rating_users.describe()



consulta_sql = """
        SELECT userId as user, COUNT(*) AS n_id
        FROM ratings
        GROUP BY userId
        HAVING n_id >=10 and n_id <=600
        ORDER BY n_id asc
"""

#### filtrar usuarios con más de 50 libros calificados (para tener calificaion confiable) y los que tienen mas de mil porque pueden ser no razonables
rating_users2= pd.read_sql(consulta_sql,conn )


fig  = px.histogram(rating_users2, x= 'n_id', title= 'Hist frecuencia de numero de calificaciones por usario')
fig.show() 

### ver distribucion despues de filtros,ahora se ve mas razonables
rating_users2.describe()


### Despues de la reducción se de los datos atipicos podemos ver un mejor comportamientos y distribución de los datos
### Pero aun se puede proponer reducir más o menos estos datos.



consulta_sql = """
        SELECT movieId as movie, COUNT(*) AS n_movie
        FROM ratings
        GROUP BY movieId
        ORDER BY n_movie DESC
"""

#### verificar cuantas calificaciones tiene cada pelicula
rating_movie=pd.read_sql(consulta_sql,conn )


### graficar distribucion

fig  = px.histogram(rating_movie, x= 'n_movie', title= 'Hist frecuencia de numero de calificaciones para cada pelicula')
fig.show()  


### analizar distribucion de calificaciones por pelicula
rating_movie.describe()


### Filtrar los datos de las peliculas que no tengan más de 50 calificaciones

consulta_sql = """
        SELECT movieId as movie, COUNT(*) AS n_movie
        FROM ratings
        GROUP BY movieId
        HAVING n_movie>=50
        ORDER BY n_movie DESC
"""

rating_movie2=pd.read_sql(consulta_sql,conn )


fig  = px.histogram(rating_movie2, x= 'n_movie', title= 'Hist frecuencia de numero de calificaciones para cada pelicula')
fig.show()

rating_movie2.describe()

###########
fn.ejecutar_sql('preprocesamientos.sql', cur)

cur.execute("select name from sqlite_master where type='table' ")
cur.fetchall()


### verficar tamaño de tablas con filtros ####


####movies

pd.read_sql('select count(*) from movies', conn)
pd.read_sql('select count(*) from movies_final', conn)

##ratings
pd.read_sql('select count(*) from ratings', conn)
pd.read_sql('select count(*) from ratings_final', conn)

## 3 tablas cruzadas ###
pd.read_sql('select count(*) from full_ratings', conn)

ratings=pd.read_sql('select * from full_ratings',conn)
ratings.duplicated().sum() ## al cruzar tablas a veces se duplican registros
ratings.info()
ratings.head(10)


movies=pd.read_sql("""select * from movies""", conn)
genres=movies['genres'].str.split('|')
te = TransactionEncoder()
genres = te.fit_transform(genres)
genres = pd.DataFrame(genres, columns = te.columns_)

