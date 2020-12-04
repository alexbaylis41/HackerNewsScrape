import requests
from bs4 import BeautifulSoup
import pandas as pd
from string import Template
from pathlib import Path
import smtplib
from email.message import EmailMessage
import datetime

date = datetime.date.today()
today_date = date.strftime('%a %d %B')

base_url = 'https://news.ycombinator.com/'
res = requests.get(base_url)
soup = BeautifulSoup(res.text, 'html.parser')


def parse_page(next_soup):
    more_link = next_soup.select('.morelink')
    href = more_link[0].get('href')
    links = next_soup.select('.storylink')
    subtext = next_soup.select('.subtext')
    while True:
        if 'news?p=3' != href:
            create_custom_hn(links, subtext)
            next_page_url = (base_url + href)
            request = requests.get(next_page_url)
            next_soup = BeautifulSoup(request.text, 'html.parser')
            parse_page(next_soup)
        else:
            return print('\n All pages complete!\n ')
        break


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        votes = subtext[idx].select('.score')
        if len(votes):
            points = int(votes[0].getText().replace('points', ''))
            if points > 99:
                hn.append({'Title': title, 'Link': href, 'Votes': points})
    return sort_stories_by_votes(hn)


def sort_stories_by_votes(hn_list):
    contents = (sorted(hn_list, key=lambda k: k['Votes'], reverse=True))
    return dataframe(contents)


def dataframe(contents):
    news = pd.DataFrame(contents, columns=['Votes', 'Title', 'Link'])
    news.index = [x for x in range(1, len(news.values)+1)]
    pd.set_option('max_columns', 3,
                  'display.width', 200,
                  'display.max_colwidth', 50)
    html_news = news.to_html(justify='center', border=0)
    return email_func(html_news)


def email_func(news):
    html = Template(Path('news.html').read_text())
    email = EmailMessage()
    email['from'] = 'Alex Baylis'
    email['to'] = 'YourEmail@gmail.com'
    email['subject'] = 'Hacker News Daily'
    email.set_content(html.substitute(name='Alex', date=f'{today_date}', news=f'{news}'), 'html')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('Your@gmail.com, YourPassword')
        smtp.send_message(email)
        print('All good boss!')


parse_page(soup)

