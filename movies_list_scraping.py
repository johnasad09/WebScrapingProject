from bs4 import BeautifulSoup
import requests

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(url=URL)
content = response.text

soup = BeautifulSoup(content, "html.parser")
movie_list = [movie.get_text() for movie in soup.find_all(name="h3", class_="title")]
movies = movie_list[::-1]

with open("movies.txt", mode="w") as file:
    for movie in movies:
        file.write(f"{movie}\n")
    print("success")

# alternatively
# for number in range(len(movie_list) -1, -1, -1):
#     print(movie_list[number])
