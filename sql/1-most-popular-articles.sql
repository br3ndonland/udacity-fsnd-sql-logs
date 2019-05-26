select title, num from
    (select substr(path, 10), count(*) as num from log
    where path !='/' group by path)
as hits, articles where substr = slug order by num desc limit 3;