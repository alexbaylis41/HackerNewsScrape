# HackerNewsScrape

Creating a daily newsletter, featuring the top news links from the 'Hacker News' website.

This project originated from the python developer course by 'Zero to Mastery' (https://zerotomastery.io)

I went a litle further and added a few extra feautures to finalise this into a useful daily morning newsletter!

Summary:

1. Using beautiful soup, scrape the first 3 pages of hacker news
2. Select the top stories (those with over 100 upvotes)
3. Organise the results from high to low and add to a pandas data frame
4. Convert to html then email the contents to my mailbox 
5. Utilise the crontab module to shedule the script.py to run each morning automatically

