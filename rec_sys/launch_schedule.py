import schedule
import time

import coll_filtering

schedule.every().day.at("00:00", "Europe/Moscow").do(coll_filtering.create_recommendations)
schedule.every().day.at("11:30", "Europe/Moscow").do(coll_filtering.create_recommendations)

while True:
    schedule.run_pending()
    time.sleep(1)