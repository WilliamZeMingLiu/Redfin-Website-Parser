from bs4 import BeautifulSoup
import requests

#url = requests.get('https://www.basketball-reference.com/players/j/jamesle01/gamelog/2019/')
url = open('lebron_james.html')
soup = BeautifulSoup(url, 'lxml')
url.close()

match = soup.find_all('div', class_="breadcrumbs")
print(match)