#import logging
import logging
import logging.handlers
import os

#email.message to send an email
from email.message import EmailMessage

#Importing security 
import ssl 
import smtplib

import requests
from bs4 import BeautifulSoup
from pony import orm
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available"

#Sending an email function
def send_email (game, price):
    email_sender = 'spencer.sv20@gmail.com'
    email_password = 'omvsotnnnwqxhwus'
    email_receiver = 'yuqinghao777@gmail.com'

    subject = f'Change price of {game}'
    body = f'The price of {game} is {price}. Go ahead and buy!' 

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


db = orm.Database()
db.bind(provider='sqlite', filename='products.db', create_db=True)

class Product(db.Entity):
    name = orm.Required(str)
    price = orm.Required(float)
    created_date = orm.Required(datetime)

db.generate_mapping(create_tables=True)

cookies = {'birthtime': '568022401'}

def steam(session):
    url = "https://store.steampowered.com/app/550/Left_4_Dead_2/"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        #"steaml4d NT",
        #float(soup.select_one("div.game_purchase_price.price").text.replace("NT$", "")),
        "steaml4d US",
        float(soup.select_one("div.game_purchase_price.price").text.replace("$", "")),
    )
    return data

def steam2(session):
    url = "https://store.steampowered.com/app/437920/Tricky_Towers/"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        #"trickytowers NT",
        #float(soup.select_one("div.game_purchase_price.price").text.replace("NT$", "")),
        "trickytowers US",
        float(soup.select_one("div.game_purchase_price.price").text.replace("$", "")),
    )
    return data



def steam3(session):
    url = "https://store.steampowered.com/app/218620/PAYDAY_2/"
    resp = session.get(url, cookies=cookies)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "PAYDAY 2 US",
        float(soup.select_one("div.game_purchase_price.price").text.replace("$", "")),
    )
    return data


def steam4(session):
    url = "https://store.steampowered.com/app/1225570/Unravel_Two/"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "Unravel Two US",
        float(soup.select_one("div.game_purchase_price.price").text.replace("$", "")),
    )
    return data


def main():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    })

    data = [
        steam(session),
        steam2(session),
        steam3(session),
        steam4(session),
    ]
    with orm.db_session:
        for item in data:
            Product(name=item[0], price=item[1], created_date=datetime.now())
            if item[1] <= 9.99:
                print(item[1])
                send_email(item[0], item[1])


if __name__ == '__main__':
    logger.info(f"Token value: {SOME_SECRET}")
    main()
