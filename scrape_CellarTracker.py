from bs4 import BeautifulSoup
import urllib3
import requests
import ssl
import certifi
from selenium import webdriver

url = \
	"http://www.cellartracker.com/notes.asp?iWine=56960"
client = webdriver.PhantomJS()
#client.get('https://www.vivino.com/')
client.get(url)
client.save_screenshot('hm.png')
soup = BeautifulSoup(client.page_source, 'lxml')
print(soup)
target = soup.find("div", class_="panel")
print(target)
#a = target.find("a")
"""
for tr in target.find_all("tr")[1:]:
	print("--------------------------------------------------------------------")
	td_type = tr.find("td", class_="type")
	td_details = tr.find("td", class_="name")
	td_score = tr.find("td", class_="score")
	print(td_type)
	print(td_details)
	print(td_score)
"""
"""
for t in table:
	t_body = t.find("tbody")
	rows = t_body.find_all("tr")
	for r in rows:
		c = r.find_all("td")
		c = [item.text.strip() for item in c]
		print(c)	
"""
#print("--------------------------------------------------------------------")



