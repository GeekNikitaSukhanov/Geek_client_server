'''
1) Написать программу, которая собирает входящие письма из своего или тестового
почтового ящика и сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172???
'''
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from pymongo import MongoClient

chrome_options = Options()
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://mail.ru/')

login = driver.find_element_by_xpath("//input[contains(@class, 'email-input svelte-1tib0qz')]")
login.send_keys('study.ai_172')

password_button = driver.find_element_by_xpath("//button[contains(@data-testid, 'enter-password')]")
password_button.click()

password = driver.find_element_by_xpath("//input[contains(@data-testid, 'password-input')]")
password.send_keys('NextPassword172???')
password.send_keys(Keys.ENTER)
letters = driver.find_elements_by_xpath("//a[contains(@class, 'llc')]")
links_list = []
for letter in letters:
    link = letter.get_attribute('href')
    links_list.append(link)

letters_list = []

for link in links_list:
    driver.get(link)
    letter_dict = {}
    topic = driver.find_element_by_xpath("//h2[contains(@class,'thread__subject')]").text
    sender = driver.find_element_by_xpath("//div[contains(@class, 'letter__author')]/span").text
    date = driver.find_element_by_xpath("//div[contains(@class, 'letter__date')]").text
    letter_body = driver.find_element_by_xpath("//div[contains(@class, 'letter__body')]").text

    letter_dict['topic'] = topic
    letter_dict['sender'] = sender
    letter_dict['date'] = date
    letter_dict['body'] = letter_body
    letters_list.append(letter_dict)



