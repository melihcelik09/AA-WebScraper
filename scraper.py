# 181805014 Melih Çelik
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import matplotlib.pyplot as plt


# I counted the frequency of the words by throwing words.
def wordListToFreqDict(wordlist):
    counter = {}
    for word in wordlist:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    return counter


# I access values in dict for frequency.
def accessValues(news):
    ValuesList = []
    for unit in news.values():
        ValuesList.append(unit)
    return ValuesList


# I access keys in dict for frequency.
def accessKeys(news):
    KeysList = []
    for unit in news.keys():
        KeysList.append(unit)
    return KeysList


# website
URL = "https://www.aa.com.tr/"
browser = webdriver.Chrome()
browser.get(URL)
# Declare lists
titleList = []
dateList = []
summaryList = []
categoryList = []
summaryListExcel = []
titleListExcel = []
# The cycle continues until all of the slider images on news site are clicked.
for i in range(12):
    browser.maximize_window()
    # I take the slider's xpath in news site.
    browser.find_element_by_xpath(f'//*[@id="myCarousel"]/ol/li[{i + 1}]').click()
    # I got your website resource
    html_source = browser.page_source
    # With the help of the BeautifulSoup library, I made it get rid of unnecessary lines.
    site = BeautifulSoup(html_source, 'html.parser')
    title = site.find('div', attrs={'class': 'detay-spot-category'}).findNext('h1').text
    titleListExcel.append(title)
    # I remove the punctuation marks of the words belonging to the title list and change the letters to lowercase letters in order to compare the signs easily.
    # In addition, I divide the sentences in titles into individual words according to the spaces.
    withoutSymbolsTitle = re.sub(r'[^\w]', ' ', title)
    TitlesWithoutSymbols = withoutSymbolsTitle.lower().split()
    for string in TitlesWithoutSymbols:
        titleList.append(string)
    date = site.select_one(
        'body > div:nth-child(3) > main > div > div.detay-bg > div > div > div > span.tarih').get_text("tarih")
    dateList.append(date)
    summary = site.find('div', attrs={'class': 'detay-spot-category'}).findNext('h4').text
    summaryListExcel.append(summary)
    # I remove the punctuation marks of the words belonging to the summary list and change the letters to lowercase letters in order to compare the signs easily.
    # In addition,I divide the sentences into individual words according to the spaces.
    withoutSymbolsSummary = re.sub(r'[^\w]', ' ', summary)
    SummaryWithoutSymbols = withoutSymbolsSummary.lower().split()
    for string in SummaryWithoutSymbols:
        summaryList.append(string)
    category = site.find('span', attrs={'class': 'detay-news-category'}).findNext('a').text
    categoryList.append(category)
    browser.back()

# Frequency chapter
frequencyWords = wordListToFreqDict(summaryList)
frequencyTitles = wordListToFreqDict(titleList)
frequencyCategory = wordListToFreqDict(categoryList)
frequencyDates = wordListToFreqDict(dateList)
# I transferred the data I kept in the lists to Excel with the help of pandas library.
data = ({'title': titleListExcel, 'datetime': dateList, 'summary': summaryListExcel, 'category': categoryList})
df = pd.DataFrame(data=data)
df.to_excel("data.xlsx", index=False)

# Plot chapter
# I plotted my data with the help of matplotlib library and showed the frequencies.
fig = plt.figure(figsize=(50, 6))
# summary plot
x1 = fig.add_subplot(2, 2, 1)
x1.bar(accessKeys(frequencyWords), accessValues(frequencyWords))
x1.title.set_text("Frequency Summary")
plt.tick_params(axis='x', which='major', labelsize=8, rotation=90)
plt.tight_layout(pad=7)
# title plot
x2 = fig.add_subplot(2, 2, 3)
x2.bar(accessKeys(frequencyTitles), accessValues(frequencyTitles))
x2.title.set_text("Frequency Titles")
plt.tick_params(axis='x', which='major', labelsize=8, rotation=90)
plt.tight_layout()
# category plot
x3 = fig.add_subplot(2, 2, 4)
x3.bar(accessKeys(frequencyCategory), accessValues(frequencyCategory))
x3.title.set_text(dateList[0])
plt.tick_params(axis='x', which='major', labelsize=8, rotation=0)
plt.tight_layout()
plt.show()
