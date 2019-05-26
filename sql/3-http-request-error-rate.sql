select errdate, http_requests, http_404,
100.0 * http_404 / http_requests as errpct from
    (select date_trunc('day', time) as reqdate, count(*)
    as http_requests from log group by reqdate)
    as requests,
    (select date_trunc('day', time) as errdate, count(*)
    as http_404 from log where status = '404 NOT FOUND'
    group by errdate)
    as errors
where reqdate = errdate
and errors.http_404 > 0.01 * requests.http_requests
order by errdate desc;