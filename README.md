# Jeopardy

This past Christmas, I went home and was reintroduced to my family's daily ritual of gathering around the TV to watch Jeopardy.
Since returning to University, I have continued watching Jeopardy each night, and have been looking to practice so I can increase my score each night.
Thus I have set out to build a jeopardy game that fetches a random assortment of 6 categories from past jeopardy games to test myself on.

## Step 1: Getting the clues

The first task in this project is getting the clues. Luckily, there is the fan-run [J Archive](https://j-archive.com/) that has text versions of every Jeopardy game since 1985. Unfortunately, [the site was created before REST was popular](https://www.reddit.com/r/Jeopardy/comments/5n6bw3/comment/dc93yov/?utm_source=share&utm_medium=web2x&context=3), and for the sake of data integrity, its developers will not be updating the architecture of the site. Not to be dissuaded, I decided to use BeautifulSoup to scrape the contents of the site and store it locally to be used in the web app.

## Step 2: Making the Game

Coming soon...
