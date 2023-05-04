import schedule
import time

import coll_filtering


schedule.every(30).seconds.do(coll_filtering.copy_table, 1)


while True:
    schedule.run_pending()
    time.sleep(1)