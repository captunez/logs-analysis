# logs-analysis

## INTRODUCTION

This project is based on newsdata provided by Udacity's logs analysis project. Three querying functions are written to ask three business questions such as what are the most popular articles on the website. As reminder, this dataset include limited numbers of authors and articles so don't be confused, however, the log data is big.

## SETTING UP

Follow these steps to get started:

1. Clone this repository into a directory.

2. `cd logs_analysis`

3. Load the newsdata into your PostgreSQL database
```
psql -d news -f newsdata.sql
```
Before loading the data, you should make sure you have installed PostgreSQL and create a database named news. To test it, you can run `\psql news` in your command line.

4. Create views. There are four views created: top_path, top_articles, count_404, count_200. **You must create them to run logs_analysis.py correctly**.

```
create view top_path as select substring(path,10) as name,count(*) 
as total from log group by path having substring(path,10)!='' 
order by total desc ;
```

```
create view top_articles 
as select articles.title, total, authors.name 
from articles, top_path,authors 
where articles.slug = top_path.name 
and authors.id = articles.author;
```

```
create view count_404 as select date_trunc('day',time) as date, count(status)
from log where substring(status from 1 for 1)='4' 
group by date_trunc('day',time), status;"
```

```
create view count_200 as select date_trunc('day',time) as date, count(status)
from log where substring(status from 1 for 1)='2' 
group by date_trunc('day',time), status;"
```

5. Run the python file

`python3 logs_analysis.py`

## EXPECTED OUTPUT

```
Top 3 articles of all time

Candidate is jerk, alleges rival -- 338647 views
Bears love berries, alleges bear -- 253801 views
Bad things gone, say good people -- 170098 views

Top authors of all time

Ursula La Multa -- 507594 views
Rudolf von Treppenwitz -- 423457 views
Anonymous Contributor -- 170098 views
Markoff Chaney -- 84557 views

Days with 404 requests greater than 1%

 July 17, 2016 -- 2.26 % errors
 ```
 
 You can also check by opening output.txt.
