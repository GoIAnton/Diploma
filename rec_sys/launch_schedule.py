import schedule
import time

import coll_filtering

coll_filtering.create_recommendations()


schedule.every().day.at("00:00").do(coll_filtering.create_recommendations)
schedule.every().day.at("11:30").do(coll_filtering.create_recommendations)


while True:
    schedule.run_pending()
    time.sleep(1)