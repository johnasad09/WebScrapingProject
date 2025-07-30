from bs4 import BeautifulSoup
import requests

URL = "https://news.ycombinator.com/news"

response = requests.get(url=URL)
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

articles = [element for element in soup.select(selector=".titleline a") if not element.find(name="span")]
article_texts = [article.getText() for article in articles]

article_links_raw = [article.get("href") for article in articles]
article_links = [f"https://news.ycombinator.com/{item}" if "item" in item else item for item in article_links_raw]

subtexts = soup.findAll(class_="subtext")
article_upvotes = [int(line.span.span.getText().strip(" points")) if line.span.span else 0 for line in subtexts]

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(
    f"Most upvoted article: {article_texts[largest_index]}\n"
    f"Number of upvotes: {article_upvotes[largest_index]} points\n"
    f"Available at: {article_links[largest_index]}."
)
