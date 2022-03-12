import requests
from bs4 import BeautifulSoup

date = input('Where I should you take? Type date in YYY-MM-DD format ')
URL = f'https://www.billboard.com/charts/hot-100/{date}'

response = requests.get(URL)
website_list = response.text
soup = BeautifulSoup(website_list, 'html.parser')
titles = soup.findAll(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-"\
                                        "size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-"\
                                        "normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet"\
                                        "-only", id="title-of-a-story")
first_title = soup.find(name='a', class_="c-title__link lrv-a-unstyle-link").getText().strip()
titles_list = [title.getText().strip() for title in titles]
titles_list.append(first_title)
print(titles_list)