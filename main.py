from bs4 import BeautifulSoup
from numpy import double, single
import requests
import re


class Clue:
  def __init__(self, clue, answer, value):
    self.clue = clue
    self.answer = answer
    self.value = value
  def getClue(self):
    return self.clue
class Scraper:
  def __init__(self):
    self.html_text = requests.get('https://www.j-archive.com/showgame.php?game_id=7262').text
    self.soup = BeautifulSoup(self.html_text, 'lxml')

  def getCategories(self):
    category_names = self.soup.find_all("td", {"class":"category_name"})
    for i in range(len(category_names)):
      category_names[i] = category_names[i].text
    return category_names

  def scrapeById(self):
    clues = self.soup.find_all("td", {"class":"clue"})
    game = self.buildGame(self.getCategories())
    singleJeopardy = game[0]
    doubleJeopardy = game[1]
    finalJeopardy = game[2]

    for clue in clues:
      clueText = str(clue.find("td", {"class":"clue_text"}))
      clueInfo = re.match('^.*<td class="clue_text" id="clue_(DJ|J)_([1-6])_([1-5])">(.*)<\/td>.*$', clueText)

      if clueInfo:
        answer =  re.match('^.*<em class=\\\\?"correct_response\\\\?">(.*)<\/em>.*$', clue.find("div", onmouseover=True, onmouseout=True, onclick=True)['onmouseover']).group(1)
        half = clueInfo.group(1)
        row =  int(clueInfo.group(2))
        col =  int(clueInfo.group(3))
        text = clueInfo.group(4)

        print('\n',half,'\n',row,'\n',col,'\n',text,'\n',answer)

        if half == 'J':
          print(col-1)
          print(row)
          singleJeopardy[col][row-1] = Clue(text, answer, row * 200)
        elif half == 'DJ':
          doubleJeopardy[col][row-1] = Clue(text, answer, row * 400)
      else: 
        print(clue)

  def displayBoard(self, board):
    for i in board:
      print(i)


  def buildGame(self, categories):
    singleJeopardy = [
      ['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6'  ],
      ['200','200','200','200','200','200',],
      ['400','400','400','400','400','400',],
      ['600','600','600','600','600','600',],
      ['800','800','800','800','800','800',],
      ['1000','1000','1000','1000','1000','1000',]
    ]
    for i in range(6):
      singleJeopardy[0][i] = categories[i]
    doubleJeopardy = [
      ['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6'  ],
      ['400','400','400','400','400','400',],
      ['800','800','800','800','800','800',],
      ['1200','1200','1200','1200','1200','1200',],
      ['1600','1600','1600','1600','1600','1600',],
      ['2000','2000','2000','2000','2000','2000',]
    ]
    for i in range(6, len(categories)-1, 1):
      doubleJeopardy[0][i%6] = categories[i]
    finalJeopardy = categories[len(categories)-1]
    return [singleJeopardy, doubleJeopardy, finalJeopardy]


scraper = Scraper()
scraper.scrapeById()
categories = scraper.getCategories()
scraper.buildGame(categories)
#scraper.getInfo()
