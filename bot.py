#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import date

import telebot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

key = config['DEFAULT']['SECRET_KEY']
bot = telebot.TeleBot(key, parse_mode=None) 

def covid_today(country: str):
  html_doc = requests.get('https://www.worldometers.info/coronavirus/').text
  soup = BeautifulSoup(html_doc, 'html.parser')
  # whole html document
  #print(soup.prettify())
  rows = soup.find_all('tr') #tr = rows
  #rows
  #type(rows) # bs4.element.ResultSet

  heading = rows[0]
  #heading
  #type(heading) #bs4.element.Tag

  header_element = BeautifulSoup(str(heading), 'html.parser').find_all('th')
  #type(header_element) # bs4.element.ResultSet
  header_text = [col.get_text() for col in header_element] # type(col) # bs4.element.Tag

  orszag = []
  for row in rows[:50]:
    element = BeautifulSoup(str(row), 'html.parser').find_all('td')
    text = [col.get_text() for col in element]
    #print(text)
    if country in text:
      orszag = text

  data = OrderedDict(zip(header_text, orszag))
  return data


# Daily cases of COVID INFECTED IN HUNGARY
@bot.message_handler(commands=['covid'])
def covid_data(message):
	data = covid_today("Hungary")
	bot.send_message(message.chat.id, f"Covid statistics for {data['Country,Other']} on this day ({date.today()}).")
	bot.send_message(message.chat.id, f"Total cases are {data['TotalCases']}.")
	bot.send_message(message.chat.id, f"New cases are {data['NewCases']} for today.")
	bot.send_message(message.chat.id, f"Total deaths are {data['TotalDeaths']} for today.")
	bot.send_message(message.chat.id, f"New deaths are {data['NewDeaths']} for today.")




bot.polling()



