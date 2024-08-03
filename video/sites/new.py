import requests
from bs4 import BeautifulSoup
import re
from video.models import Movie, Serie, PlayList
from django.core.files import File
from django.contrib.auth.models import User
from django.core.files.temp import NamedTemporaryFile

pattern = r'\((.*?)\)'

def remove_spaces(string):
    return "".join(string.rstrip().lstrip())

def download_image(url, model_obj, image_field):
    response = requests.get(url)
    if response.status_code == 200:
        response.raise_for_status()
        file_temp = NamedTemporaryFile()
        file_temp.write(response.content)
        file_temp.flush()
        model_instance = model_obj  # Assuming model_obj is already instantiated
        if not getattr(model_instance, image_field):
            with open(file_temp.name, 'rb') as file:
                getattr(model_instance, image_field).save("image.png", File(file))
            print("File saved successfully.")
        return file_temp.name

def create_or_get_playlist(title):
    playlist, created = PlayList.objects.get_or_create(
        title=title,
        defaults={"user": User.objects.get(id=1)}
    )
    if created:
        print("Season created successfully ✔")
    return playlist



def create_or_get_serie(title):
    serie, created = Serie.objects.get_or_create(
        title=title,
        defaults={"user": User.objects.get(id=1)}
    )
    if created:
        print("Serie created successfully ✔")
    return serie


def create_movie(url, season, playlist_id):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = re.sub(r'\([^)]*\)', '', soup.find('h1').text).strip()
    tags_content = soup.find('ul', {'class': 'Terms--Content--Single-begin'})
    tags = ",".join(tag.text for tag in tags_content.find_all('a'))[:100]
    description = soup.find('div', {'class': 'StoryMovieContent'})
    description = description.text if description else ' '
    playlist_instance = PlayList.objects.get(id=playlist_id)
    if not Movie.objects.filter(episode=season, list=playlist_instance).exists():
        Movie.objects.create(
            user=User.objects.get(id=1),
            title=title,
            tags=tags,
            description=description,
            episode=season,
            list=playlist_instance,
            scraping_url=url
        )
        print("Created successfully...")
    else:
        print("Movie exists...")

def process_season(url, image, title):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    season_title = re.sub(r'\([^)]*\)', '', soup.find('h1').text).strip()
    season_list = soup.find('div', {'class': 'List--Seasons--Episodes'})


    
    if season_list:
        return 0  # Indicate no season
    else:
        playlist = create_or_get_playlist(title)
        serie = create_or_get_serie(season_title)
        download_image(image, playlist, 'image')
        download_image(image, serie, 'image')
        episode_links = soup.find('div', {'class': 'Seasons--Episodes'}).find_all('a')
        for episode_link in reversed(episode_links):
            episode_url = episode_link['href']
            season = re.search(r'\d+', episode_link.find('episodetitle').text).group()
            create_movie(episode_url, season, playlist.id)

def new(request):
    if request.GET.get("start"):
        start = int(request.GET.get("start"))
    else:
        start = 5

    for page in range(start, 0, -1):
        url = f"https://mycima.wecima.show/seriestv/new/?page_number={page}/"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        card_content = soup.find('div', {'class': 'Grid--WecimaPosts'})
        results = card_content.find_all("div", {'class': 'Thumb--GridItem'})
        print(f"Page ==== {page}")
        for item in results: 
            if item:
                url = str(item.find('a')['href']).replace("https://t4cce4ma.shop","https://mycima.wecima.show")
                title = re.sub(r'\([^)]*\)', '', item.find('a').text).strip()
                try: 
                    image = item.find('span', {'class': 'BG--GridItem'})['data-lazy-style']
                except Exception as error:
                    print(error)
                    image = None
                image = re.findall(pattern, image)[0]
                print("Processing the series...")
                process_season(url, image, title)
