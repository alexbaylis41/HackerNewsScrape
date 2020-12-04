# HackerNewsScrape

Creating a newsletter, featuring the top news hits from Hacker News website.

This project originated from the python developer course by 'Zero to Mastery' (https://zerotomastery.io)

However, I went a litle further and added a few extra feautures to finalise this into a morning newsletter format.

Below is a summary of what the code does:

1. Using beautiful soup, scrape the first 3 pages of hacker news
2. Select the top stories (those with over 100 upvotes)
3. Organise the results from high to low and add to a pandas data frame
4. Convert to html and email the contents to myslef as a morning newsletter

Finally, you can schedule this code to run each morning using https://www.pythonanywhere.com/.

(Note you may have to set up a paid account as Hacker News is not on their 'white list' of websites, - those whitch you can utilise on a free account. See the website for details.) 
