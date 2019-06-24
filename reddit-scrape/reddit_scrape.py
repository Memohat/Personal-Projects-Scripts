#! python3
# Mehmet Hatip API Test

import requests, json, praw, os, shutil, logging
import re, pprint, sys, time, random, subprocess
from imgurpython import ImgurClient


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logging.disable(logging.ERROR)
data_file_name = 'Reddit scrape'
msg_exit_format = 'Exiting to main menu: {0}'

def find_extension(url):
    try:
        ext = re.search(r'(\.\w{3,5})(\?.{1,2})?$', url).group(1)
        return ext
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

def make_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)

def slim_title(title):
    name = re.sub(r"[^\s\w',]", '', title).strip()
    char_max = 250 - len(os.path.abspath('.'))
    name = name[:char_max-1] if len(name) >= char_max else name
    return name

def get_size(storage, start_path=os.getcwd()):
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
    exceeded = bool(total_size >= storage * 10**9)
    if exceeded:
        print(msg_exit_format.format(f'Reached {storage} gigabyte(s)'))
    return exceeded

def get_num_sub(num):
    if num == 'e':
        print(msg_exit_format.format(''))
        return True
    elif type(num) == int:
        num -= 1
        if num == 0:
            print(msg_exit_format.format('Subreddit count reached'))
            return True
    return False

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

def settings():
    choices = ['hot', 'top', 'new']
    section, posts = 'top', 10
    msg = f'Enter hot, top, or new: '
    while True:
        section = input(msg).lower()
        if section in choices:
            break
        print('Error, try again')

    msg = f'Enter number of posts: '
    while True:
        try:
            posts = int(input(msg))
            if posts < 1 or posts > 999:
                raise Exception
            else:
                break
        except:
            print('Error, try again')
    return section, posts

def subreddit_param(sub, section='top', posts=10):
    if section == 'top':
        return sub.top(limit=posts)
    elif section == 'hot':
        return sub.hot(limit=posts)
    elif section == 'new':
        return sub.new(limit=posts)

def automation(storage):
    msg_storage = f'Limit set at {storage} gigabyte(s). Change? (y/n) '
    usr_storage = None
    while True:
        usr_storage = input(msg_storage)
        if usr_storage == 'y':
            while True:
                storage = input('Enter new gigabyte amount: ')
                try:
                    storage = float(storage)
                    break
                except:
                    print('Error: not number value')
            break
        elif usr_storage == 'n':
            break

    num_sub = input('Enter number of random subreddits to download, or press '
                    + f'Enter to fill all {storage} gigabyte(s) (e to exit) ')
    try:
        num_sub = float(num_sub)
    except:
        if num_sub != 'e':
            num_sub = None

    return num_sub, storage

def main():
    prompt = ("Enter name of subreddits, separate with space\n\t"
    + "r for random\n\t"
    + "rr for random automation\n\t"
    + "del to delete subreddit folder\n\t"
    + "s for settings\n\t"
    + "e to exit\n")

    reddit, imgur = clients()
    make_dir(data_file_name)
    automate, num = False, -1
    inp = None
    storage = 1
    logging.debug('Start of while loop')

    while True:
        if automate:
            if num == -1:
                num, storage = automation(storage)
            if get_num_sub(num):
                automate = False
                num = -1
                continue
            inp = 'r'
        else:
            if len(sys.argv) <= 1:
                sys.argv = sys.argv + input(prompt).split()
            inp = sys.argv.pop(1)
        if inp == 'r':
            sub = reddit.random_subreddit()
        elif inp == 'rr':
            automate = True
            continue
        elif inp == 'del':
            del_sub = input('Enter subreddit to be deleted: ')
            if os.path.isdir(del_sub):
                shutil.rmtree(del_sub)
                print(f'{del_sub} successfully deleted')
            else:
                print(f'Error: {del_sub} was not found')
            continue
        elif inp == 's':
            settings()
            continue
        elif inp == 'e':
            print('Exiting')
            break
        else:
            try:
                sub = reddit.subreddit(inp)
                sub.title
            except:
                print(f'Error, subreddit {inp} does not exist')
                continue

        logging.debug('Subreddit downloaded')

        name = sub.display_name
        title = sub.title

        if sub.over18:
            print(f'\n{"*"*20}\nNice try...\n{"*"*20}\n')
            continue

        print('{:<22}: '.format(name) + title + '\n')
        make_dir(sub.display_name)


        for submission in subreddit_param(sub):
            url = submission.url
            title = slim_title(submission.title)
            text = submission.selftext
            extension = find_extension(url)

            # logging
            logging.info("Initial URL: " + str(url))
            logging.info("ID: " + submission.id)
            variables = pprint.pformat(vars(submission))
            #logging.debug(variables)

            if submission.is_reddit_media_domain and submission.is_video:
                url = submission.media['reddit_video']['fallback_url']
                if submission.media['reddit_video']['is_gif']:
                    extension = '.mp4'
                else:
                    url_audio = re.sub(r'\/[^\/]+$',r'/audio', url)
                    download_video(title, url, url_audio)
                    continue
            elif bool(re.search(r'streamable\.com\/\w+', url)):
                try:
                    url_id = re.search(r'(\w+)([-\w]+)?$', url).group(1)
                    req = requests.get('https://api.streamable.com/videos/' + url_id)
                    url = 'http:' + req.json()['files']['mp4']['url']
                    extension = 'mp4'
                except:
                    logging.debug('streamable page not found')
                    continue
            elif bool(re.search(r'gfycat\.com\/\w+', url)):
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
                            if item.animated:
                                url = item.mp4
                            else:
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
                        item = imgur.get_image(id)
                        if item.animated:
                            url = item.mp4
                        else:
                            url = item.link
                        extension = find_extension(url)
                except:
                    logging.debug("Error, imgur file is missing, skipping")
                    continue
            elif text:
                extension = '.txt'
            elif not extension:
                text = url
                extension = '.URL'

            logging.info('Download URL: ' + url)
            name = title + extension if extension else title

            print(f'Downloading {name if not n else extension}')

            status = download_file(name, url, text=text)
            logging.debug(status)

            if get_size(storage):
                automation, num = False, -1
                print(f'\n{"*"*20}\n{storage} gigabytes exceeded.\n{"*"*20}\n')


        while not os.path.basename(os.getcwd()) == data_file_name:
            os.chdir("..")
        print('Done\n')
if __name__ == '__main__':
    main()
