
# Import all the necessary libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
from string import Template
from pathlib import Path
import smtplib
from email.message import EmailMessage
import datetime

# Date for header of newsletter in format day, date, month
date = datetime.date.today()
today_date = date.strftime('%a %d %B')

# Using beautiful soup to search the website
base_url = 'https://news.ycombinator.com/'
res = requests.get(base_url)
soup = BeautifulSoup(res.text, 'html.parser')  # Prepares the page html to be scraped


def parse_page(next_soup):
    more_link = next_soup.select('.morelink')  # Here we define the link for moving through the pages
    href = more_link[0].get('href')  # This is the link
    links = next_soup.select('.storylink')  # This is the story title
    subtext = next_soup.select('.subtext')  # This is where the votes lie
    while True:
        if 'news?p=3' != href:  # This loop keeps cycles through the web pages until reaches page 3
            create_custom_hn(links, subtext)  # Sends all the data we scraped into the next function
            next_page_url = (base_url + href)  # Modifies the url to move into next page
            request = requests.get(next_page_url)  # Moves to next page
            next_soup = BeautifulSoup(request.text, 'html.parser')  # Prepares new page for scrape
            parse_page(next_soup)
        else:
            return print('\n All pages complete!\n ')
        break


def create_custom_hn(links, subtext):  # This function creates our custom list of HN stories
    hn = []
    for idx, item in enumerate(links):  # Selects the title, link and score of each story
        title = item.getText()
        href = item.get('href', None)
        votes = subtext[idx].select('.score')
        if len(votes):  # Only if the stories are over 99 up votes, append to our hn list
            points = int(votes[0].getText().replace('points', ''))
            if points > 99:
                hn.append({'Title': title, 'Link': href, 'Votes': points})
    return sort_stories_by_votes(hn)


def sort_stories_by_votes(hn_list): # Organises the stories into order high to low
    contents = (sorted(hn_list, key=lambda k: k['Votes'], reverse=True))
    return dataframe(contents)


def dataframe(contents): # Creates a dataframe to present the stories
    news = pd.DataFrame(contents, columns=['Votes', 'Title', 'Link'])
    news.index = [x for x in range(1, len(news.values)+1)]
    pd.set_option('max_columns', 3,  # Some formatting of table
                  'display.width', 200,
                  'display.max_colwidth', 50)
    html_news = news.to_html(justify='left', border=0)  # Creates a html version of news table
    return email_func(html_news)


def email_func(news):
    html = Template(Path('news.html').read_text())  # Opens the news.html file and reads it
    email = EmailMessage()
    email['from'] = 'Alex Baylis'
    email['to'] = 'YourEmail@gmail.com'
    email['subject'] = 'Hacker News Daily'
    email.set_content(html.substitute(name='Alex', date=f'{today_date}', news=f'{news}'), 'html')
    # This line substitutes the information here into the news.html file

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('Your@gmail.com, YourPassword')  # Enter your email and password
        smtp.send_message(email)
        print('Email sent!')


parse_page(soup)
# Initialises the code sequence. Sends the initial parsed url (soup) into the parse_page function.

