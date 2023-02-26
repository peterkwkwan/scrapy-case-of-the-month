# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import time
import requests
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

_ = load_dotenv()
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
error_address = os.environ.get("ERROR_ADDRESS")
recipients = os.environ.get("RECIPIENTS")

class WatchNewCasesSpider(scrapy.Spider):
    name = 'cases'
    start_urls = ['https://www.collegept.org/case-of-the-month']
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    # allowed_domains = ['www.collegept.org']


    def parse(self, response):
       response.xpath('//*[@id="cph_content_T7A75863F005_Col00"]/div[1]/ul/li[1]/div[1]/text()')``