import re
import requests
import pickle
from bs4 import BeautifulSoup
import codecs
import time 
import sys
from selenium import webdriver
import json, sys, os
from psycopg2 import connect, Error
# import the JSON library from psycopg2.extras
from psycopg2.extras import Json
# import psycopg2's 'json' using an alias
from psycopg2 import extras
from psycopg2.extras import json as psycop_json

from scrape import scrape_all_pages
from parse import parse_all_pages
from insert_database import load_data_into_database


def start():
    # try running scraping and retry if error happen
    n_retry = 5
    for attempt in range(n_retry):
        try:
            scrape_all_pages()
        except:
            time.sleep(5)
            continue
        else:
            break
    else:
        print('Scraping failed')

    parse_all_pages()
    load_data_into_database()

if __name__ == '__main__':
    start()