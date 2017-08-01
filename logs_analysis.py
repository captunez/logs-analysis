#!/usr/bin/env python3
#      --------------   DESCRIPTION   --------------
# logs_analysis.py is to analyze logs of a news website by
# querying a PostgreSQL database named news made of three
# tables(articles, authors, log). It is to answer three
# questions such as what are the most popular articles on
# the website.

import psycopg2

DBNAME = 'news'


def connect(dbname):
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	try:
	    db = psycopg2.connect("dbname={}".format(dbname))
	    c = db.cursor()
	    return db, c
	except psycopg2.Error as e:
	    print("Unable to connect to database")
	    # THEN perhaps exit the program
	    sys.exit(1) # The easier method
	    # OR perhaps throw an error
	    raise e
	    # If you choose to raise an exception,
	    # It will need to be caught by the whoever called this function


def make_query(sql):
	"""Return query results given a SQL"""
	db, cursor = connect(DBNAME)	
	cursor.execute(sql)
	results = cursor.fetchall()
	db.close()
	return results


def print_heading(heading):
	"""Print a heading before the output"""
	print('\n' + heading + '\n')


def top_three_articles():
	""" Print the three most popular articles of all time """
	# top_path is a view querying the path visited most
	# with ordering and sliceing
	# create view top_path as select substring(path,10) as name,count(*)
	# as total from log group by path having substring(path,10)!=''
	# order by total desc ;
	sql = "select title, total from articles, top_path where\
			articles.slug = top_path.name order by total desc limit 3"

	top_three = make_query(sql)
	print_heading("Top 3 articles of all time")
	for name, total in top_three:
		print("{} -- {} views".format(name, total))
	return


def top_authors():
	""" Print the top authors of all time """
	# top_articles is a view querying the most viewed articles
	# create view top_articles
	# as select articles.title, total, authors.name
	# from articles, top_path,authors
	# where articles.slug = top_path.name
	# and authors.id = articles.author;
	sql = "select name, sum(total) as author_total from top_articles\
	group by name order by author_total desc;"
	popular_authors = make_query(sql)
	print_heading("Top authors of all time")
	for name, total in popular_authors:
		print("{} -- {} views".format(name, total))
	return


def high_error_days():
	""" Print the days in which there were more than 1 percent bad requests """
	# only two kind of status: 200 and 404
	# create view count_404 as select date_trunc('day',time) as date,
	# count(status) from log where substring(status from 1 for 1)='4'
	# group by date_trunc('day',time), status;"
	# create view count_200 as select date_trunc('day',time) as date,
	# count(status) from log where substring(status from 1 for 1)='2'
	# group by date_trunc('day',time), status;"
	sql = "select error_percent.date, error_percent.percent \
	from (select count_404.date, \
	1.0*count_404.count/(count_404.count+count_200.count) \
	as percent from count_404, count_200 \
	where count_404.date = count_200.date) as error_percent\
	where error_percent.percent>0.01; "
	freq_404_days = make_query(sql)
	print_heading("Days with 404 requests greater than 1%")
	for date, percent in freq_404_days:
		print(" {0:%B %d, %Y} -- {1:.2f} % errors".format(date, percent*100))
	return

if __name__ == '__main__':
	top_three_articles()
	top_authors()
	high_error_days()
