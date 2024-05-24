# import datetime as dt

# date = dt.datetime(1970, 1, 7)
# dates = [dt.datetime(1970, 1, 2), dt.datetime(1970, 1, 3), dt.datetime(1970, 1, 4), dt.datetime(1970, 1, 5), dt.datetime(1970, 1, 8)]
# print(min(dates, key=lambda d: abs(d - date)))

from datetime import timezone 
import datetime 
  
  
# Getting the current date 
# and time 
dt = datetime.datetime.now(timezone.utc) 
  
utc_time = dt.replace(tzinfo=timezone.utc) 
utc_timestamp = utc_time.timestamp() 
  
print(utc_timestamp) 
