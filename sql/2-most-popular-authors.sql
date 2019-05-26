select name, sum(views) as total_views from
    (select name, author, title, views from
        (select substr(path, 10), count(*) as views from log
            where path !='/' group by path)
        as hits, articles, authors
        where substr = slug and author = authors.id
        order by views desc)
    as threetables group by name order by total_views desc;
