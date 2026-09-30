import requests
from bs4 import BeautifulSoup

url = 'https://www.bilibili.com'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

file_path = 'C:/Users/DELL/Desktop/scraped_data.txt'

with open(file_path, 'w', encoding='utf-8') as file:
    for paragraph in soup.find_all('p'):
        file.write(paragraph.text + '\n')
