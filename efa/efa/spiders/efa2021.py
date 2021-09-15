import scrapy                                   # Scrapy import necessary
import re                                       # Regular expressions
from scrapy.linkextractors import LinkExtractor # To get links
import w3lib.html                               # Utility functions installed with Scrapy

# Set this to None when not debugging, set to a number as a string to stop on a specific session
DEBUG_SESSION_NUMBER = None

class Efa2021Spider(scrapy.Spider):
    name = 'efa2021'
    # allowed_domains = ['https://www.conftool.com/efa2021']
    start_urls = ['https://www.conftool.com/efa2021/sessions.php/']

    # This is boiler plate to add a link extractor to our scrapy object
    def __init__(self):
        super()
        self.link_extractor = LinkExtractor()
        
    
    # Scrapy will go to all the start_urls, request HTML, and then
    # call the parse method below with the response from the website
    def parse(self, response):

        # Go through every link on the page
        for link in self.link_extractor.extract_links(response):

            # Only consider those with a URL pattern form_session=NUMBER
            if re.search('form_session=\d+', link.url):

                self.log(link.url)

                # Tell Scrapy that we want to scrape this session page
                yield scrapy.Request(url=link.url, callback=self.parse_session)


    # This is called by scrapy due to the callbath parameter in the
    # yield scrapy.Request statement above
    def parse_session(self, response):
        
        if DEBUG_SESSION_NUMBER and not re.search(DEBUG_SESSION_NUMBER, response.url):
            return

        # Loop over every paper division
        for paper_div in response.xpath('//div [@class="paper"]'):

            if DEBUG_SESSION_NUMBER is not None:
                breakpoint()

            # Get the title
            # The .// means search only in this division. // would go back from the division to the whole doc.
            title = paper_div.xpath('.//p [@class="paper_title"]/text()').extract()

            # Stop processing this paper_div and "continue" with the next paper_div
            if len(title) == 0:
                continue
                
            title = title[0].strip()

            # Get the authors
            author_html = paper_div.xpath('.//p [@class="paper_author"]').extract()
            breakpoint()
            author_html = w3lib.html.remove_tags(author_html[0])

            authors = []
            for author_str in author_html.split(','):
                # Get rid of leading and trailing spaces
                author_str = author_str.strip()

                # Regular expressions are FUN
                # [^\d]: Anything that's not a number
                # +: 1 or more
                # [^\d]+: 1 or more characters that aren't numbers
                #
                # \d: A digit
                # \d*: Zero or more digits
                #
                # Things in parentheses are available for extraction
                m = re.match("([^\d]+)(\d*)", author_str)

                if m is None:
                    breakpoint()

                author = { 'name': m[1], 'affiliation': m[2] }
                authors.append(author)

            # Process the affiliations to make them nice
            raw_affiliations = paper_div.xpath('.//p [@class="paper_organisation"]/text()').extract()
            affiliations = []
            for aff_str in raw_affiliations:
                aff = aff_str.replace(';', '')
                aff = aff.replace('\'', '')
                aff = aff.strip()
                affiliations.append(aff)

            # Construct a dictionary with our data
            paper = { 'title': title,
                      'authors': authors,
                      'affiliations': affiliations}

            # Send this data back to scrapy
            yield paper
           
                
