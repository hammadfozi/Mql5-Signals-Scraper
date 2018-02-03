# Mql5 Signals Scraper
You can use this scraper to download all the data from a signal at mql5.com

Features:
- Login to the website
- Scraping Tooltip, Graphs, Positions, History, Statistics, Risks, Slippage, Description and Reviews data.
- Ouput to multiple csv files.

Method:

- Just open up links.txt and add signals' id in it (one per line):

eg: https://www.mql5.com/en/signals/25221

in this url, id = 25221

A sample list of IDs are already added to links.txt

- run the software, it will open up chrome (Selenium) and will use that to scrape the data.