import schedule
import time

import coll_filtering


# schedule.every(3).minutes.do(coll_filtering.create_recommendations)


# while True:
#     schedule.run_pending()
#     time.sleep(1)

coll_filtering.create_recommendations()