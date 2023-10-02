import numpy as np
import pandas as pd
import sqlite3 as sql
from sklearn.preprocessing import MinMaxScaler
from ipywidgets import interact ## para análisis interactivo
from sklearn import neighbors ### basado en contenido un solo producto consumido
import joblib
from mlxtend.preprocessing import TransactionEncoder
#### conectar_base_de_Datos

conn=sql.connect('Datos//db_movies_2')
cur=conn.cursor()

#### ver tablas disponibles en base de datos ###

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
cur.fetchall()


######################################################################
################## 1. sistemas basados en popularidad ###############
#####################################################################


##### recomendaciones basado en popularidad ######

####¿Cuáles son las 10 películas con la calificación promedio más alta?
consulta_sql = """
    SELECT title, AVG(rating) as calificacion
    FROM full_ratings
    GROUP BY title
    ORDER BY calificacion DESC 
    LIMIT 10
"""
pd.read_sql(consulta_sql, conn)

#### ¿Cuáles son las 10 películas más populares (con más calificaciones) junto con el número total de calificaciones que han recibido?
consulta_sql = """
    SELECT title, COUNT(rating) as total_calificacion
    FROM full_ratings
    GROUP BY title
    ORDER BY total_calificacion DESC 
    LIMIT 10
"""
pd.read_sql(consulta_sql, conn)

####¿Cuáles son los 5 géneros más vistos basado en la cantidad total de películas en ese género?
consulta_sql = """
    SELECT SUBSTR(genres, 1, INSTR(genres, '|') - 1) AS genero, COUNT(genres) AS total_peliculas, AVG(rating) as calificacion
    FROM full_ratings
    GROUP BY genero
    ORDER BY calificacion DESC
    LIMIT 5
"""
pd.read_sql(consulta_sql, conn)

consulta_sql = """
    SELECT * FROM movies_final
"""
pd.read_sql(consulta_sql, conn)


#######################################################################
######## 2.1 Sistema de recomendación basado en contenido un solo producto - Manual ########
#######################################################################

movies=pd.read_sql('select * from full_ratings', conn )

movies.info()


## eliminar filas que no se van a utilizar ###
movies_dum1=pd.read_sql("""select * from full_ratings""", conn)
genres=movies_dum1['genres'].str.split('|')
te = TransactionEncoder()
genres = te.fit_transform(genres)
genres = pd.DataFrame(genres, columns = te.columns_)
movies_dum1.genres.unique()
genres.head()
movies_dum1 = pd.concat([movies_dum1, genres], axis=1)
movies_dum1
# df_concatenado = pd.concat([df1, df2], axis=0)

movies_dum1=movies_dum1.drop(columns=['genres'])
movies_dum1.head()

#### convertir a dummies

# movies_dum1['book_author'].nunique()
# movies_dum1['publisher'].nunique()

col_dum=genres.columns
movies_dum2=pd.get_dummies(movies_dum1,columns=col_dum)
movies_dum2.shape
movies_dum2.head()

joblib.dump(movies_dum2,"Datos//movies_dum2.joblib") ### para utilizar en segundos modelos



###### libros recomendadas ejemplo para un libro#####

pelicula='Toy Story (1995)'
ind_libro=pelicula[pelicula['book_title']==pelicula].index.values.astype(int)[0]
similar_books=movies_dum2.corrwith(movies_dum2.iloc[ind_libro,:],axis=1)
similar_books=similar_books.sort_values(ascending=False)
top_similar_books=similar_books.to_frame(name="correlación").iloc[0:11,] ### el 11 es número de libros recomendados
top_similar_books['book_title']=books["book_title"] ### agregaro los nombres (como tiene mismo indice no se debe cruzar)
    


#### libros recomendados ejemplo para visualización todos los libros

def recomendacion(libro = list(books['book_title'])):
     
    ind_libro=books[books['book_title']==libro].index.values.astype(int)[0]   #### obtener indice de libro seleccionado de lista
    similar_books = books_dum2.corrwith(books_dum2.iloc[ind_libro,:],axis=1) ## correlación entre libro seleccionado y todos los otros
    similar_books = similar_books.sort_values(ascending=False) #### ordenar correlaciones
    top_similar_books=similar_books.to_frame(name="correlación").iloc[0:11,] ### el 11 es número de libros recomendados
    top_similar_books['book_title']=books["book_title"] ### agregaro los nombres (como tiene mismo indice no se debe cruzar)
    
    return top_similar_books


print(interact(recomendacion))