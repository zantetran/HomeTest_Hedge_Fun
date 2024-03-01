#### How it work
Based on the requirements of the task, I have created two main functions: **daily_download_files** for scheduling a daily cron job to download files externally and a **recovery** function that can backfill data for the desired time period.
Log was saved in file download.log and data saved at files folder.

### Improvement
Some possible improvements include adding additional unit tests, Dockerized the application, and setting up cron jobs. Furthermore, consider implementing a database instead of using files.