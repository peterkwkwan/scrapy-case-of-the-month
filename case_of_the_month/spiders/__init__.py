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
from scrapy.mail import MailSender

mailer = MailSender()

_ = load_dotenv()
# email_address = os.environ.get("EMAIL_ADDRESS")
# email_password = os.environ.get("EMAIL_PASSWORD")
# error_address = os.environ.get("ERROR_ADDRESS")
recipients = os.environ.get("RECIPIENTS")

class WatchNewCasesSpider(scrapy.Spider):
    name = 'cases'
    start_urls = ['https://www.collegept.org/case-of-the-month']
    # allowed_domains = ['www.collegept.org']

    def parse(self, response):
        print(f'RESPONSE: {response}')
        latest_case = response.css("div.sfpostAuthorAndDate::text").get()
        print(f'Lastest case: {latest_case}')
        if latest_case != self.settings.get('latest_case_seen'):
            print(f'New case found!')
            subject = 'New Case of the Month!'
            message = 'Click here to read: https://www.collegept.org/case-of-the-month'
            # Update the latest case seen
            self.settings.set('latest_case_seen', latest_case)
            self.settings.save()
        else:
            print(f'No new case')
            subject = 'Nothing Changed'
            message = 'No new cases'

        print(f'Sending email to: {recipients}')
        print(f'Email subject: {subject}')
        mailer.send(to=[recipients], subject=subject, body=message)