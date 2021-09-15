# rmf2_2021_scraping_intro

The code from a short introductory session to web scraping for Research Methods
in Finance 2, 2021.

# Scraping and Scrapy overview

Scraping roughly consists of two related tasks. The first is to follow URL links
and collect source HTML. And, the second is to parse that source HTML and get
data.

We write Scrapy code to go through the URLs and it will automatically (once set up)
save the HTML in a cache for us. Scrapy will also manage the queue of URLs for us,
running them in parallel and also throttling as necessary. It also has nice 
search methods to pull data from a web page.

Scrapy is set up as a Python program and a library. What we'll do is write
code that interfaces with the program.

A layer of complexity arises since we are essentially writing code to plug into
Scrapy. 

# Tools

- Python 3.7 or above (breakpoint method is useful)
- Scrapy
- Browser with the developer tools extension (linking the visual page to the source code is VERY helpful)
 
# "Skills"

- Python
- Regular expressions are VERY helpful (nice intro site is Rubular.org)


# Scrapy

Note: Be sure to turn on HTTP caching in the config.py file.

## Create a project (once)
> scrapy startproject PROJECTNAME

## Generate a spider (once for each web crawler)

> scrapy genspide SPIDERNAME URL (no http://)

## Run our spider (as often as we like)
scrapy runspider SPIDERNAME

# If running the spider once or developing the spider use capital -O, which 
# deletes any existing data.
scrapy runspider SPIDERNAME -O DATA.JSON --logfile=my_log
scrapy runspider SPIDERNAME -O DATA.XML  --logfile=my_log

# Once the spider works, use lower case -o, which appends to the data.
scrapy runspider SPIDERNAME -o DATA.JSON --logfile=my_log
scrapy runspider SPIDERNAME -o DATA.XML  --logfile=my_log

* Always check the log file for errors and fix them
