import numpy as np
import pandas as pd
import sqlite3 as sql
from sklearn.preprocessing import MinMaxScaler
from ipywidgets import interact ## para análisis interactivo
from sklearn import neighbors ### basado en contenido un solo producto consumido
import joblib
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

movies=pd.read_sql('select * from movies_final', conn )

movies.info()


## eliminar filas que no se van a utilizar ###

books_dum1=books.drop(columns=['isbn','i_url','year_pub','book_title'])

#### convertir a dummies

books_dum1['book_author'].nunique()
books_dum1['publisher'].nunique()

col_dum=['book_author','publisher']
books_dum2=pd.get_dummies(books_dum1,columns=col_dum)
books_dum2.shape

joblib.dump(books_dum2,"salidas\\books_dum2.joblib") ### para utilizar en segundos modelos



###### libros recomendadas ejemplo para un libro#####

libro='The Testament'
ind_libro=books[books['book_title']==libro].index.values.astype(int)[0]
similar_books=books_dum2.corrwith(books_dum2.iloc[ind_libro,:],axis=1)
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