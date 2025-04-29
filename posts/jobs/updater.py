from .jobs import get_reddit_post
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_reddit_post, 'interval', minutes=30)
    scheduler.start()
