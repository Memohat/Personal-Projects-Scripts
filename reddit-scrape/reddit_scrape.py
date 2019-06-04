#! python3
# Mehmet Hatip API Test

import requests, json, praw, os, shutil, logging
import re, pprint, sys, time, random, subprocess
from imgurpython import ImgurClient

message = "Enter name of subreddit, e to exit, r for random: "
automate = [None,'r'][0] # Automates to select r each time
data_file_name = 'Reddit'

def find_extension(url):
    try:
        return re.search(r'(\.\w{3,5})(\?.{1,2})?$', url).group(1)
    except:
        return None

def download_file(name, url, text=None):
    try:
        if not os.path.isfile(name):
            if text:
                saveFile = open(name, 'w')
                saveFile.write(text)
            else:
                res = requests.get(url, stream=True)
                #res.raise_for_status()
                saveFile = open(name, 'wb')
                for chunk in res:
                    saveFile.write(chunk)
            saveFile.close()
            return str(f'Downloaded {name}')
        else:
            return str(f'{name} already exists')
    except:
        return str(f'{name} could not be downloaded')

def download_video(name, video, audio):
    try:
        if not os.path.isfile(name):
            download_file('video.mp4', video)
            download_file('audio.mp3', audio)
            name = slim_title(name) + '.mp4'
            logging.info(f'Video name: {name}')
            cmd = "ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s"
            cmd = cmd % ('video.mp4', 'audio.mp3', 'combined.mp4')
            logging.info(f'CMD: {cmd}')
            with open(os.devnull, 'w') as devnull:
                subprocess.run(cmd, stdout=devnull)
            os.remove('video.mp4')
            os.remove('audio.mp3')
            os.rename('combined.mp4', name)
            logging.info('Downloaded video with audio')
        else:
            return str(f'{name} already exists')
    except:
        return str(f'{name} could not be downloaded')

def get_subreddit(delay=5):
    if automate:
        sub = automate
        time.sleep(delay)
    else:
        sub = input(message)
    return sub

def make_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)

def slim_title(title):
    char_max = 255 - len(os.path.abspath('.'))
    title = title[:char_max-1] if len(title) >= char_max else title
    return title

def get_size(start_path=os.getcwd(), storage=50):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except:
                    None
    exceeded = bool(total_size >= storage**10)
    if exceeded:
        print(f'Exceeded {storage} gigabytes, exiting')
    return exceeded

def clients():
    reddit = praw.Reddit(
    client_id='TNXJh1DaoUyO1w',
    client_secret='hKfekLF_vORYMV4-XQEm3iNz55Q',
    user_agent='windows:my_script:1.0 (by /u/memohat)'
    )

    imgur = ImgurClient(
    client_id='39b04bdb6b54455',
    client_secret='9017657f85f04d1e32bb1f573102f8ec110ddc09'
    )

    return reddit, imgur

def subreddit_param(sub, section='top', posts=10):
    if section == 'top':
        return sub.top(limit=posts)
    elif section == 'hot':
        return sub.hot(limit=posts)
    elif section == 'new':
        return sub.new(limit=posts)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    logging.disable(logging.CRITICAL)
    reddit, imgur = clients()

    make_dir(data_file_name)

    sub = sys.argv[1] if len(sys.argv) > 1 else get_subreddit()

    while True:
        if sub == 'e':
            print('Exiting')
            break
        elif sub == 'r':
            sub = reddit.random_subreddit()
        else:
            sub = reddit.subreddit(sub)

        if get_size():
            break

        if sub.over18:
            sub.title = '*' * 4
            make_dir('z----')

        try:
            print(f'Subreddit: {sub.title}')
            make_dir(sub.display_name)
        except:
            print('Error, subreddit does not exist')
            sub = get_subreddit()
            continue
        print('Copying files...', end='')

        for submission in subreddit_param(sub):
            url = submission.url
            title = re.sub(r"[^\s\w',]", '', submission.title).strip()
            text = submission.selftext
            extension = find_extension(url)

            # logging
            logging.info("Initial URL: " + str(url))
            logging.info("ID: " + submission.id)
            variables = pprint.pformat(vars(submission))
            #logging.debug(variables)

            if bool(re.search(r'gfycat\.com\/\w+', url)):
                try:
                    url_id = re.search(r'(\w+)([-\w]+)?$', url).group(1)
                    req = requests.get('https://api.gfycat.com/v1/gfycats/' + url_id)
                    url = req.json()['gfyItem']['mp4Url']
                    extension = find_extension(url)
                    if not extension:
                        raise Exception
                except:
                    logging.debug('gfycat page not found')
                    continue

            elif bool(re.search(r'imgur', url)):
                regex = re.search(r'(imgur.com\/)(\w+\/)?(\w+)(\.\w+)?(.*)?$', url)
                if regex:
                    domain, album, id, extension, bs = regex.groups()
                logging.info('Imgur ID: ' + id)
                try:
                    if album:
                        images = imgur.get_album_images(id)
                        folder_name = str(title + '_' + id)
                        make_dir(folder_name)
                        logging.debug(f'Downloading imgur album to "{folder_name}"', end='')
                        i = 1

                        for item in images:
                            url = item.link
                            extension = find_extension(url)

                            if item.title:
                                title = item.title

                            else:
                                title = 'Untitled' + str(i)
                                i += 1

                            status = download_file(title + extension, url)

                        logging.debug('\nFinished imgur album')
                        os.chdir('..')
                        continue

                    else:
                        url = imgur.get_image(id).link
                        extension = find_extension(url)
                except:
                    logging.debug("Error, imgur file is missing, skipping")
                    continue
            elif bool(submission.is_video):
                url = submission.media['reddit_video']['fallback_url']
                url_audio = re.sub(r'\/[^\/]+$',r'/audio', url)
                download_video(title, url, url_audio)
                continue
            elif text:
                extension = '.txt'
            elif not extension:
                text = url
                extension = '.txt'

            logging.info('Download URL: ' + url)
            name = slim_title(title) + extension if extension else slim_title(title)
            status = download_file(name, url, text=text)
            logging.debug(status)

        while not os.path.basename(os.getcwd()) == data_file_name:
            os.chdir("..")
        print("Done")
        sub = get_subreddit()

if __name__ == '__main__':
    main()
