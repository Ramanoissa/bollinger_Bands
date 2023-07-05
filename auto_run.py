import schedule
import time
import main



# Schedule updates daily at midnight
schedule.every().day.at('00:00').do(main)

# Continuously run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)