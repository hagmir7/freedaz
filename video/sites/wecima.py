

import requests
from bs4 import BeautifulSoup
import re
from video.models import Movie, Video
from django.http import JsonResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
import os


pattern = r'\((.*?)\)'  # Regular expression pattern to match the text inside parentheses

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




def download_file(url, id):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.raise_for_status() 

            file_temp = NamedTemporaryFile()
            file_temp.write(response.content)
            file_temp.flush()

            movie = Movie.objects.get(id=id)  # Instantiate your model object
            with open(file_temp.name, 'rb') as file:
                movie.image.save("image.png", File(file))

            print("File saved successfully.")
        else:
            print("Failed to download the file.")
    except:
        pass


def download_video(url, id):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.raise_for_status() 

            file_temp = NamedTemporaryFile()
            file_temp.write(response.content)
            file_temp.flush()

            size = os.path.getsize(file_temp)
            print(size)
            video = Video.objects.get(id=id)  # Instantiate your model object
            with open(file_temp.name, 'rb') as file:
                video.video_file.save("image.mp4", File(file))

            print("File saved successfully.")
        else:
            print("Failed to download the file.")
    except:
        print(url)
        print("Video Downlod Error.")




def getItem(url, image):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        movie_content = soup.find('div', {'class': 'Download--Wecima--Single'})
        movies = movie_content.find_all('a', {'class': 'hoverable'})

        name = re.sub(r'\([^)]*\)', '', soup.find('h1').text).strip()
        description = soup.find('div', {'class': 'StoryMovieContent'})
        if description:
            description = description.text

        tags = soup.find('span', {'class': 'mpaadesc'})
        if tags:
            tags = tags.text

        quality = {}
        for movie in movies:
            if len(re.findall(r"(.*?)\.html", movie['href'])) > 0:
                quality[movie.find('resolution').text] =  re.findall(r"(.*?)\.html", movie['href'])[0]

        data = {
                "name": str(name),
                "description": description if description else " ",
                "tags": tags,
                "image": image,
                "quality": quality
            }
    

        if not Movie.objects.filter(title=data.get('name')).exists():
            movie = Movie.objects.create(
                user = User.objects.get(id=1),
                title = re.sub(r'\(مشاهدة\)', '', data.get('name')),
                description = data.get('description'),
                tags = data.get('tags'),
                scraping_url = url
            )
            download_file(image, movie.id)
            for key, value in data.get('quality').items():
                Video.objects.create(
                    quality = key,
                    url = value,
                    movie = movie
                )
        else:
            print("Movie is exists....")
        print("--------------------------------------------")
        return data
    except:
        pass


def wecima(request):
    for page in range(323, 0, -1):
        url = f"https://weciimaa.online/movies/page/{page}/"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        results = soup.find_all("div", {'class': 'Thumb--GridItem'})
        print(f"Page ==== {page}")
        for item in results:
            if item:
                link = item.find('a')['href']
                try: image = item.find('span', {'class': 'BG--GridItem'})['data-lazy-style']
                except: image = None
                image = re.findall(pattern, image)[0]
                getItem(link, image)

    return JsonResponse({"message": "Compoletd"})
                
                
