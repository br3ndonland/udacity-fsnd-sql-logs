# SQL database logs analysis code review

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo">
</a>

[Udacity Full Stack Developer Nanodegree program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

Brendon Smith ([br3ndonland](https://github.com/br3ndonland))

[![code license](https://img.shields.io/badge/code%20license-MIT-blue.svg?longCache=true&style=for-the-badge)](https://choosealicense.com/licenses/mit/)

## Table of Contents <!-- omit in toc -->

- [Reviewer summary](#reviewer-summary)
- [Review](#review)
  - [`logs.py`](#logspy)
  - [README.md](#readmemd)
  - [logs-methods.md](#logs-methodsmd)
- [My updates](#my-updates)
- [My response](#my-response)

## Reviewer summary

> Well done! All of the information in your report is correct, and I found no issues serious enough to require you to resubmit your project. I did make a number of suggestions that I hope you find useful and that in your spare time you consider incorporating into your project. Your project meets all specifications - congratulations and good luck with your next courses and projects!

[(Back to TOC)](#table-of-contents)

## Review

### `logs.py`

#### Query 1

> - _Awesome:_ The Python code begins with a valid shebang line.
> - _Awesome:_ Docstrings have been included with all of your functions.
> - _Awesome:_ This SELECT statement runs efficiently and returns the correct results. _(Query 1)_
> - _Suggestion:_ Consider adding a little formatting to your detail print line. This code:
>
>   ```py
>       results = c.fetchall()
>       for title, num in results:
>           print("    {}  --  {} views".format(title, num))
>   ```
>
>   will produce the following:
>
>   ```text
>   Query 1: Most popular three articles
>       Candidate is jerk, alleges rival  --  338647 views
>       Bears love berries, alleges bear  --  253801 views
>       Bad things gone, say good people  --  170098 views
>   ```
>
> - The indentation helps to set off the detail lines. I added "views" to the end of the line to help describe what the numeric value represents.
> - Some good information and better examples of this kind of string formatting can be found at the [following site](https://pyformat.info/). See my comment on line 94 before for another example.

#### Query 2

> _Awesome:_ This SELECT statement also runs efficiently and returns the correct results.

#### Query 3

> - _Suggestion:_ You can easily calculate the error percentage rate within the SELECT statement. Use the following to replace lines 76 - 77:
>
>   ```py
>       c.execute("""
>           select requests.date,
>                 100.0 - http_404 / http_requests as errpct
>           from
>   ```
>
>   Using 100.0 instead of 100 avoids any integer division truncation issues (PostgreSQL truncates the result of integer division, similar to what Python 2 does).
>
> - _Suggestion:_ If you use my suggestion for line 77, you can replace lines 90 - 94 with the following and write a date string and a rounded error percentage rate on one line instead of two:
>
>   ```py
>       for errdate, errpct in c.fetchall():
>           print("    {:%B %d, %Y}  --  {:.2f}% errors".format(errdate, errpct))
>   ```
>
>   (I left your comments out only to simplify my suggested code.)
>
> - The [date directives](https://pyformat.info/#datetime) are the same ones available when using the `strftime()` date conversion library. The errpct value is rounded to two decimal places. The output looks like this:
>
>   ```text
>   Query 3: Days on which >1% HTTP requests returned 404 errors
>       July 17, 2016  --  2.26% errors
>   ```
>
> - _Suggestion:_ Because the database-related code in your three functions is essentially the same, consider refactoring it into a separate helper function that the three functions would call. This function would take a SELECT statement as a parameter, do the connect/cursor/execute/fetchall/close steps, then return the results of the SELECT statement. The code could look something like this:
>
>   ```py
>   def get_query_results(query):
>       db = psycopg2.connect(database="news")
>       c = db.cursor()
>       c.execute(query)
>       result = c.fetchall()
>       db.close()
>       return result
>   ```

### README.md

> - _Awesome:_ Thanks for including both the download link to the newsdata.sql file and this psql command to import the newsdata.sql file into the news database. Often these steps are overlooked.
> - _Suggestion:_ For my testing purposes I added the following to the end of your Python code file:
>
>   ```py
>   if __name__ == "__main__":
>       popular_articles()
>       popular_authors()
>       errors()
>   ```
>
>   This allows me to execute your code by either typing
>
>   ```sh
>   python3 logs.py
>   ```
>
>   or by invoking the shebang line:
>
>   ```sh
>   ./logs.py
>   ```

### logs-methods.md

> _Suggestion:_ Coming up with the join criteria for the log/articles table is a bit of a challenge. Your solution is good.Another solution would be the following:
>
> ```sql
>     where log.path = concat('/article/', articles.slug)
> ```
>
> Take a look at the following query - notice that it's sorted first on status, then by views (for brevity I limit the results to the first 15 rows):
>
> ```sql
> news=> select path, status, count(*) as views from log
> news-> group by path, status
> news-> order by status, views desc limit 15;
> ```
>
> ```text
>                 path                |    status     | views
> ------------------------------------+---------------+--------
> /                                  | 200 OK        | 479121
> /article/candidate-is-jerk         | 200 OK        | 338647
> /article/bears-love-berries        | 200 OK        | 253801
> /article/bad-things-gone           | 200 OK        | 170098
> /article/goats-eat-googles         | 200 OK        |  84906
> /article/trouble-for-troubled      | 200 OK        |  84810
> /article/balloon-goons-doomed      | 200 OK        |  84557
> /article/so-many-bears             | 200 OK        |  84504
> /article/media-obsessed-with-bears | 200 OK        |  84383
> /spam-spam-spam-humbug             | 404 NOT FOUND |    301
> /%20%20%20                         | 404 NOT FOUND |    290
> /+++ATH0                           | 404 NOT FOUND |    288
> /article/candidate-is-jerkx        | 404 NOT FOUND |    161
> /article/candidate-is-jerkq        | 404 NOT FOUND |    155
> /article/candidate-is-jerkh        | 404 NOT FOUND |    152
> (15 rows)
> ```
>
> Notice how there are less than ten log.path values for those rows that have a status of '200 OK'. Almost all of the rows start with "/article/" followed by a value that can be found in the articles.slug column, with no appended characters (not like the last three rows in the above results). These are the rows we want to include in the first two sections of the report. Using the join criteria I suggested will guarantee that only those rows will be included.
>
> In the real world (I say this as someone who has worked with relational databases for 20+ years) you would likely be given clearer information on what columns to use in any join criteria. Some options may work but (for reasons a bit too deep to get into here) they won't run efficiently. I've seen the following on occasion:
>
> ```sql
>     where log.path like concat('%', articles.slug)
> ```
>
> This might work but the LIKE keyword tells PostgreSQL to search through the string looking for a match, which can be a bit slower than a direct match using an equality (as I suggested above).

[(Back to TOC)](#table-of-contents)

## My updates

- **Implement helper function to re-use code shared among the SQL queries**

  - Creating the helper function was straightforward, and I got it to work in my first few tries.
  - Group database connection commands into the helper function
  - Save each SQL query as an object instead of in `c.execute()`, like

    ```py
    query = ("""query here""")
    ```

  - Run helper function to execute query, and save as another object:

    ```py
    result = get_query_results(query)
    ```

  - Reference the object `result` when printing output.

- **Improve Python output string formatting**

  - It was easy to reformat queries 1 and 2 based on the reviewer's suggestion.
  - Query 3 was throwing an error:

    ```py
        # Print results
        print('\n', 'Query 3: Days on which >1% HTTP requests returned 404 errors')
        for errdate, errpct in result:
            print("    {:%B %d, %Y}  --  {:.2f}% errors".format(errdate, errpct))
    ```

    ```text
    Traceback (most recent call last):
      File "logs.py", line 107, in <module>
        errors()
      File "logs.py", line 99, in errors
        for errdate, errpct in result:
    ValueError: too many values to unpack (expected 2)
    ```

  - The solution was to declare all columns from the SQL query in the `for` loop:

    ```py
        # Print results
        print('\n', 'Query 3: Days on which >1% HTTP requests returned 404 errors')
        for errdate, http_requests, http_404, errpct in result:
            print("    {:%B %d, %Y}  --  {:.2f}% errors".format(errdate, errpct))
    ```

- **Update README with new info**

[(Back to TOC)](#table-of-contents)

## My response

> Thank you so much for taking the time to provide a thorough and thoughtful review! I learned a great deal from your suggestions, and successfully implemented all of them. Stay Udacious!

[(Back to TOC)](#table-of-contents)
