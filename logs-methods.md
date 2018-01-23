# Logs analysis project methods and notes

**Udacity Full Stack Web Developer Nanodegree program**

Part 03. Backend

Project 01

Brendon Smith

br3ndonland


## Getting started

### Setup

* I read through the Udacity documentation and rubric (see *logs-udacity.md*)
* Files:
	- *logs-methods.md* (this file) to log my progress
	- *logs-udacity.md* to store the project information and rubric from Udacity
	- *logs.py* for the main program code
	- *output.txt* to store sample output from the program
	- *README.md* for a concise description of the project
* I kept vagrant and the database in a separate directory because of the large size of the database file.


### Starting the virtual machine and exploring the data

* I already had vagrant installed from the instructions in *Lesson 2.17. Installing the Virtual Machine*.
* I unzipped *newsdata.sql* and moved it into the *vagrant* directory.
* I changed into the vagrant directory and started up vagrant (only necessary when restarting computer):
	```bash
	$ vagrant up
	```
* I then logged in to Ubuntu as before
	```bash
	$ vagrant ssh
	```
* I connected to the database and loaded the data with PostgreSQL:
	```bash
	$ cd /vagrant
	/vagrant$ psql -d news -f newsdata.sql
	```
	As explained in the Udacity documentation for the project (see *logs-udacity.md*):
	> Here's what this command does:
	> 
	> * `psql` — the PostgreSQL command line program
	> * `-d news` — connect to the database named news which has been set up for you
	> * `-f newsdata.sql` — run the SQL statements in the file newsdata.sql
	> 
	> Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
* I then began exploring the data:
	```
	/vagrant$ psql -d news
	psql (9.5.10)
	Type "help" for help.

	news=> \dt
	```
	Output (table reformatted for Markdown):

	| Schema |   Name   | Type  |  Owner  |
	|:-------|----------|-------|--------:|
	| public | articles | table | vagrant |
	| public | authors  | table | vagrant |
	| public | log      | table | vagrant |
* Next:


### Starting Python in *logs.py*

* Shebang: when reading through the "Functionality" section of the rubric, I saw that it recommended "a correct shebang line to indicate the Python version." I actually hadn't written a shebang line before, but looked it up on [Stack Overflow](https://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script) and drafted one.
* I created an outline in the python file *logs.py* with the steps I would be working on. Here's the initial outline:
	```python
	#!/usr/bin/env python3

	# Udacity database logs analysis project

	# 1. Most popular three articles

	# 2. Most popular authors

	# 3. Days on which >1% of HTTP requests led to errors

	```
* To function or not to function: Next, I decided to write each of the three queries as a Python function. I began building the functions based on *forumdb.py* and *3.3. Writing Code with DB API* from *Lesson 03. Python DB-API*.

## TODO

