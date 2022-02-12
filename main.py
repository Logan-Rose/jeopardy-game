from bs4 import BeautifulSoup
from numpy import double, single
import requests
import re
import csv
import os
import glob
import pandas as pd
class Clue:
  def __init__(self, text, answer,row, col, half):
    self.half = half
    self.row = row
    self.col = col
    self.text = text
    self.answer = answer
  def getClue(self):
    return self.clue
class Game:
  def __init__(self, id):
    self.html_text = requests.get(f'https://www.j-archive.com/showgame.php?game_id={id}').text
    self.soup = BeautifulSoup(self.html_text, 'lxml')

  def isValid(self):
    error = self.soup.find('p', {"class":"error"})
    if error:
      return not (error.text == "ERROR: No game requested." or bool(re.match('^ERROR: No game -?[0-9]+ in database\.$',error.text)))
    # else:
    #   if len(self.getCategories) < 13:
    #     return False
    return True

  def getCategories(self):
    self.categoryNames = self.soup.find_all("td", {"class":"category_name"})
    for i in range(len(self.categoryNames)):
      self.categoryNames[i] = self.categoryNames[i].text
    return self.categoryNames

  def scrape(self):
    clues = self.soup.find_all("td", {"class":"clue"})
    categories = self.getCategories()
    if categories:
      self.game = self.buildGame(categories)

      for clue in clues:
        clueText = str(clue.find("td", {"class":"clue_text"}))
        clueInfo = re.match('^.*<td class="clue_text" id="clue_(DJ|J)_([1-6])_([1-5])">(.*)<\/td>.*$', clueText)
        if clueInfo:
          answer =  re.match('^.*<em class=\\\\?"correct_response\\\\?">(.*)<\/em>.*$', clue.find("div", onmouseover=True, onmouseout=True, onclick=True)['onmouseover']).group(1)
          half = clueInfo.group(1)
          row =  int(clueInfo.group(3))
          col =  int(clueInfo.group(2))
          text = clueInfo.group(4)
          #print('\n',half,'\n',row,'\n',col,'\n',text,'\n',answer)
          if half == 'J':
            self.game[0][col-1][row] = Clue(text, answer,row, col, half)
            writer.writerow([self.categoryNames[col-1],row*200,text,answer]);
          elif half == 'DJ':
            self.game[1][col-1][row] = Clue(text, answer,row, col, half)
            writer.writerow([self.categoryNames[col+5],row*400,text,answer]);
          else:
            self.game[2] = [Clue(text, answer,row, col,'F')]
        # else: 
        #   print('----')
        #   print(clue)
        #   print('----')
      return self.game

  def displayBoard(self, board):
    for i in board:
      print(i)


  def buildGame(self, categories):
    self.singleJeopardy = [
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
    ]
    for i in range(6):
      self.singleJeopardy[i][0] = categories[i]
    self.doubleJeopardy = [
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
      ['category', 'clue1', 'clue2', 'clue3', 'clue4', 'clue5'  ],
    ]
    for i in range(6, len(categories)-1, 1):
      self.doubleJeopardy[i%6][0] = categories[i]
    self.finalJeopardy = [categories[len(categories)-1], "clue"]
    return [self.singleJeopardy, self.doubleJeopardy, self.finalJeopardy]

f = open('clues.csv', 'w')
writer = csv.writer(f)
writer.writerow(['Category','Value','Clue','Answer']);

for i in range(7274):
  #6224-6232 - Tournament of champions
  #3576
  if i not in [3576, 6224, 6225, 6226, 6227,6228,6229,6230,6231,6232]:
    print("Getting Game" , i)
    bucket = i // 200
    if bucket != (i-1)//200:
      f.close()
      fileName = f'./data/clues_{bucket*200}-{min((bucket+1)*200-1,7274)}.csv'
      f = open(fileName, 'x')
      writer = csv.writer(f)
      writer.writerow(['Category','Value','Clue','Answer']);
    game = Game(i)
    if game.isValid():
      game.scrape()

all_files = [i for i in glob.glob('./data/*.{}'.format('csv'))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_files ])
#export to csv
combined_csv.to_csv( "clues.csv", index=False, encoding='utf-8-sig')
