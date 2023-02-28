# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import requests
import smtplib
from pathlib import Path
from email.message import EmailMessage
import os
from dotenv import load_dotenv
# from scrapy.mail import MailSender

# mailer = MailSender()

_ = load_dotenv()
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
error_address = os.environ.get("ERROR_ADDRESS")
recipients = os.environ.get("RECIPIENTS")

def send_email(to, subject, message):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg.set_content(message)
        msg['From'] = email_address
        msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)    
            smtp.close()
            print ("Email sent successfully!")   
        return True
    except Exception as e:
        print("Problem while sending email")
        print(str(e))
    return False

class WatchNewCasesSpider(scrapy.Spider):
    name = 'cases'
    start_urls = ['https://www.collegept.org/case-of-the-month']
    # allowed_domains = ['www.collegept.org']

    def parse(self, response):
        filename = 'last-date.txt'
        path = Path(filename)
        if path.is_file():
            f = open(filename)
            saved_date = f.read()
            print(f'saved_date: {saved_date}')
        else:
            f = open(filename, 'x')
            saved_date = ''
            print(f'created new file')

        print(f'RESPONSE: {response}')
        try:
            latest_case = response.css("div.sfpostAuthorAndDate::text").get().strip()
        except Exception as e:
            error_message = f'ERROR: Cannot get date from CSS: {e}'
            print(error_message)
            send_email(error_address, 'ERROR', error_message)

        print(f'Lastest case: {latest_case}')
        
        if latest_case != saved_date:
            print(f'New case found!')
            subject = 'New Case of the Month!'
            message = 'Click here to read: https://www.collegept.org/case-of-the-month'

            # Update the latest case seen
            try:
                os.remove(filename)
                new_file = open(filename, 'x')
                new_file.write(latest_case)
                print(f'saved_new_case')
                return True
            except Exception as e:
                print(f'ERROR: Cannot write file: {e}')
                return False
           
        else:
            print(f'No new case')
            subject = 'Nothing Changed'
            message = 'No new cases'

        print(f'Sending email to: "{recipients}"')
        print(f'Email subject: "{subject}"')
        send_email(recipients, subject, message)
        yield None

    
