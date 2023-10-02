----procesamientos---

---crear tabla con usuarios con más de  libros leídos y menos de 600

drop table if exists usuarios_sel;

create table usuarios_sel as 

        SELECT userId, COUNT(*) AS n_id
        FROM ratings
        GROUP BY userId
        HAVING n_id >=10 and n_id <=600
        ORDER BY n_id asc ;



---crear tabla con peliculas que han sido vistas por más de 50 usuarios
drop table if exists movies_sel;

create table movies_sel as 

        SELECT movieId, COUNT(*) AS n_movie
        FROM ratings
        GROUP BY movieId
        HAVING n_movie>=50
        ORDER BY n_movie DESC;


-------crear tablas filtradas de peliculas y calificaciones ----
drop table if exists ratings_final;

create table ratings_final as
    select a."userId",
    a.movieId,
    a."rating",
    a."timestamp"
    from ratings a
    inner join movies_sel b
    on a.movieId=b.movieId
    inner join usuarios_sel c
    on a.userId=c.userId;

drop table if exists movies_final;

create table movies_final as
    select a.movieId,
    a."title",
    a."genres"
    from movies a
    inner join movies_sel c
    on a.movieId = c.movieId;


--- crear tabla filtrada de movies y ratings
drop table if exists full_ratings;

create table full_ratings as 
    select a.*, b.title, b.genres
    from ratings_final a
    inner join movies_final b
    on a.movieId=b.movieId;

