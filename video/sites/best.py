import requests
from bs4 import BeautifulSoup
import re
from video.models import Movie, Video, Serie, PlayList
from django.http import JsonResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
import os
import time
from itertools import cycle
import cloudscraper
scraper = cloudscraper.create_scraper()


pattern = r'\((.*?)\)'  # Regular expression pattern to match the text inside parentheses


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
proxy ={"http": "http://10.122.53.36:8080", "https": "http://10.122.53.36:8080"}

# Remove end spaces
def remove_end_spaces(string):
    return "".join(string.rstrip())

# Remove first and  end spaces
def remove_first_end_spaces(string):
    return "".join(string.rstrip().lstrip())

# Remove all spaces
def remove_all_spaces(string):
    return "".join(string.split())

# Remove all extra spaces
def remove_all_extra_spaces(string):
    return " ".join(string.split())

urls = ['mycima.pw', 'mycimaa.monster', 'mycima.tube', 'mycima.movie', 'wecima.actor']
def download_image_serie(**kwargs):
    try:
        if not any(substring in kwargs.get('image_url') for substring in urls):
            response = scraper.get(kwargs.get('image_url'))
            if response.status_code == 200:
                response.raise_for_status() 

                file_temp = NamedTemporaryFile()
                file_temp.write(response.content)
                file_temp.flush()
                serie = Serie.objects.get(id=kwargs.get('serie_id'))  # Instantiate your model object
                if not serie.image:
                    with open(file_temp.name, 'rb') as file:
                        serie.image.save("image.png", File(file))
                    print("File saved successfully.")
                return file_temp.name
    except:
        pass


def download_image_list(**kwargs):
    try:
        if not any(substring in kwargs.get('image_url') for substring in urls):
            response = scraper.get(kwargs.get('image_url'))
            if response.status_code == 200:
                response.raise_for_status() 

                file_temp = NamedTemporaryFile()
                file_temp.write(response.content)
                file_temp.flush()
                playList = PlayList.objects.get(id=kwargs.get('list_id'))  # Instantiate your model object
                if not playList.image:
                    with open(file_temp.name, 'rb') as file:
                        playList.image.save("image.png", File(file))
                    print("File saved successfully.")
                return file_temp.name
    except:
        pass

def getNewItem(url, season, list_id):
    try:
        response = scraper.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = re.sub(r'\([^)]*\)', '', soup.find('h1').text).strip()
            

        getTagsContent = soup.find('ul', {'class': 'Terms--Content--Single-begin'})
        plainTags = []
        getTagsList = getTagsContent.find_all('a')
        for tag in getTagsList:
            plainTags.append(tag.text)

        tags = ",".join(plainTags)[0:100]

        description = soup.find('div', {'class': 'StoryMovieContent'})
        if description:
            description = description.text
        else:
            description = ' '
        
        if not Movie.objects.filter(episode=season, list=PlayList.objects.get(id=list_id)).exists():
            Movie.objects.create(
                user = User.objects.get(id=1),
                title = title,
                tags = tags,
                description = description,
                episode = season,
                list = PlayList.objects.get(id=list_id),
                scraping_url = url
            )
            print("Created successfully...")
        else:
            print("Movie is exists...")
    except:
        pass




def getItem(url, image, title):
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    sub_title = re.sub(r'\([^)]*\)', '', soup.find('h1').text).strip()
    is_season = soup.find('div', {'class': 'List--Seasons--Episodes'})
    load_btn = soup.find('div', {'class': 'MoreEpisodes--Button'})
    # if load_btn:
    #     return 0
    if not is_season:
        print("No season👽")
        # list_content = soup.find('div', {'class' : 'Full--Width'})
        list_items = soup.find_all('a', {'class': "activable"})

        # Create Season
        if not Serie.objects.filter(title=title).exists():
            serie = Serie.objects.create(
                title = title,
                user = User.objects.get(id=1)
            )
        else:
            serie = Serie.objects.filter(title=title)[0]
        if not PlayList.objects.filter(title=sub_title).exists():
            playList = PlayList.objects.create(
                title = sub_title,
                user = User.objects.get(id=1),
                season = 1,
                serie = serie
            )
        else:
            playList = PlayList.objects.filter(title=sub_title)[0]

        # Download image for List
        download_image_list(
            image_url = image,
            list_id = playList.id
        )

        # Download image for serie
        download_image_serie(
            image_url = image,
            serie_id = serie.id,
        )
        try:
            for item in range(len(list_items) - 1, -1, -1):
                newUrl = list_items[item]
                season = re.search(r'\d+', newUrl.find('episodetitle').text).group()
                getNewItem(newUrl['href'], season, playList.id)
        except:
            pass
    else:
        season_list = is_season.find_all('a')
        if not Serie.objects.filter(title=title).exists():
            serie = Serie.objects.create(
                title = title,
                user = User.objects.get(id=1)
            )
        else:
            serie = Serie.objects.filter(title=title)[0]

            # Download image for serie
        download_image_serie(
            image_url = image,
            serie_id = serie.id,
        )
               
        # Get season
        for item in season_list:
            print("الموسم")
            response = scraper.get(item['href'])
            soup = BeautifulSoup(response.content, "html.parser")
            image_style = soup.find('wecima', {'class': 'separated--top'})['style'] ##['data-lazy-style']
            
            season_image = re.findall(pattern, image_style)[0]
            print(season_image)
            sub_title = re.sub(r'\([^)]*\)', '', soup.find('h1').text).strip()
            list_content = soup.find('div', {'class' : 'Episodes--Seasons--Episodes'})
            list_items = list_content.find_all('a')
            if not PlayList.objects.filter(title=sub_title).exists():
                playList = PlayList.objects.create(
                    title = sub_title,
                    user = User.objects.get(id=1),
                    season = 1,
                    serie = serie
                )
            else:
                playList = PlayList.objects.filter(title=sub_title)[0]
            
            # Download image for List
            download_image_list(
                image_url = season_image,
                list_id = playList.id
            )

 

                # Get حلقة
            try:
                for item in range(len(list_items) - 1, -1, -1):
                    print("الحلقة")
                    newUrl = list_items[item]
                    season = re.search(r'\d+', newUrl.find('episodetitle').text).group()  #re.search(r'\d+', my_string).group()
                    getNewItem(newUrl['href'], season, playList.id)
            except:
                pass
 






proxy_list = [
    'ohekzdlm:es1g7jpw21uj@188.74.210.21:6100',
    # 'http://ohekzdlm:es1g7jpw21uj@185.199.229.156:7492',
    # # Add more proxies as needed
]


proxy_pool = cycle(proxy_list)

def best(request):
    proxy = next(proxy_pool)
    if request.GET.get('pages'):
        pages = request.GET.get('pages')
    else:
        pages = 1
    for page in range(int(pages), 0, -1):
        url = f"https://t4cce4ma.shop/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/page/{page}/"
        html = scraper.get(url)
        time.sleep(5)
        soup = BeautifulSoup(html.content, "html.parser")
        card_content = soup.find('div', {'class': 'Grid--WecimaPosts'})
        print("Title:", soup.title.text)
        results = card_content.find_all("div", {'class': 'GridItem'})
        print(f"Page ==== {page}")
        for item in results: 
            if item:
                url = item.find('a')['href']
                title  = re.sub(r'\([^)]*\)', '', item.find('a').text).strip() 
                try: image = item.find('span', {'class': 'BG--GridItem'})['data-lazy-style']
                except: image = None
                image = re.findall(pattern, image)[0]
                print("المسلسل")
                getItem(url, image, title) 