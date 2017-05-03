from bs4 import BeautifulSoup
from selenium import webdriver
"""
browser = webdriver.PhantomJS()
#browser = webdriver.Firefox()  
browser.get('http://techcrunch.com/2012/05/15/facebook-lightbox/') 
html_source = browser.page_source
browser.quit()


soup = BeautifulSoup(html_source, 'html.parser')
comments = soup.findAll('div', {'class': 'postTest'})
print (comments)
"""
"""
driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)
driver.get('https://google.com/')
driver.save_screenshot('screen.png')
sbtn = driver.find_element_by_css_selector('button.gbqfba')
sbtn.click()
driver.save_screenshot('screenafter.png')
"""
url = \
	"http://www.cellartracker.com/notes.asp?iWine=2248270&searchId=46027824%23selected%253DW2248270_3_K6187ee20a4d670985d51487a929a3554"
client = webdriver.PhantomJS()
#client.get('https://www.vivino.com/')
client.get(url)
client.save_screenshot('hm.png')
soup = BeautifulSoup(client.page_source, 'lxml')
print(soup)