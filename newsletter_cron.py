from crontab import CronTab

# Create crontab to schedule code to run each day at 7am
cron = CronTab(user='alex_dmb')  # Set user
job = cron.new(command='''~/PycharmProjects/modules/venv/bin/python  
/Users/alex_dmb/PycharmProjects/modules/ZerotoMasteryPython/ScrapeProject/scrape.py >/dev/null 2>&1''')
# runs the python 3.9 module from pycharm on the projects file path
job.hour.on(7)  # time set to 7am each day
cron.write()
print('cron.write() was executed')

