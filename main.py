from bs4 import BeautifulSoup
import requests
import re

class Scraper:
  def __init__(self):
    self.html_text = requests.get('https://www.j-archive.com/showgame.php?game_id=7262').text
    self.soup = BeautifulSoup(self.html_text, 'lxml')

  def getCategories(self):
    category_names = self.soup.find_all("td", {"class":"category_name"})
    for i in category_names:
      print(i.get_text())

  def getClues(self):
    answers = self.soup.find_all("div", onmouseover=True, onmouseout=True, onclick=True)
    for i in answers:
        answer = i#re.match('^.*<em class="correct_response">(.*)<\/em>.*$', i['onmouseover'])
        if answer:
          print(i['onmouseout'])
  def getInfo(self):
    questions = self.soup.find_all("div", onmouseover=True, onmouseout=True, onclick=True)
    for i in questions:
        clue = re.match('^.*toggle\(\'.*\', \'.*\', (.*)\).*$', i['onmouseout'])
        if clue:
          clue = clue.group(1) 
        response = re.match('^.*<em class=\\\\?"correct_response\\\\?">(.*)<\/em>.*$', i['onmouseover'])
        if response:
          response = response.group(1)
        print(clue, ":", response)

scraper = Scraper()

scraper.getInfo()
