#! python3
# Mehmet Hatip API Test

import requests, json, praw, os, shutil, logging, re, pprint

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logging.disable(logging.INFO)

while True:
        sub = input("Enter subreddit, e to exit: ")
        if sub == 'e':
                break
        if not os.path.isdir(sub):
                os.mkdir(sub)
        os.chdir(sub)

        reddit = praw.Reddit(client_id='TNXJh1DaoUyO1w', client_secret='hKfekLF_vORYMV4-XQEm3iNz55Q', user_agent='windows:my_script:1.0 (by /u/memohat')

        for submission in reddit.subreddit(sub).top(limit=10):
                url = submission.url
                title = re.sub("\*|\/|\\|\:|\?|\"|\<|\>|\|", '', submission.title)
                text = submission.selftext
                extension = re.search("\.\w+$", url).group() if re.search("\.\w+$", url) else ''
                logging.info("URL: " + str(url))
                logging.info("Extension: " + str(extension))
                logging.info(f"Text: {text}")
                logging.ERROR(submission.media.reddit_video.fallback_url)
                if not os.path.isfile(title + extension):
                        if text:
                                saveFile = open(title + ".txt", 'w')
                                saveFile.write(text)
                        elif bool(submission.is_video):
                                logging.ERROR(submission.media.reddit_video.fallback_url)
                        else:
                                res = requests.get(url, stream=True)
                                #res.raise_for_status()
                                saveFile = open(title + extension, 'wb')
                                for chunk in res:
                                        saveFile.write(chunk)
                        saveFile.close()

        os.chdir("..")
        print("Done")
	
