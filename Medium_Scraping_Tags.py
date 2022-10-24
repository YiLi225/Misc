# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 16:11:48 2022

@author: yilis
"""

import requests
import pandas as pd
allTopic = {"accessibility":"accessibility","addiction":"addiction","android-development":"android-development","art":"art",
            "artificial-intelligence":"artificial-intelligence","astrology":"astrology","basic-income":"basic-income","beauty":"beauty","biotech":"biotech","blockchain":"blockchain","books":"books","business":"business","cannabis":"cannabis","cities":"cities","climate-change":"climate-change","comics":"comics","coronavirus":"coronavirus","creativity":"creativity","cryptocurrency":"cryptocurrency","culture":"culture","cybersecurity":"cybersecurity","data-science":"data-science","design":"design","digital-life":"digital-life","disability":"disability","economy":"economy","education":"education","equality":"equality","family":"family","feminism":"feminism","fiction":"fiction","film":"film","fitness":"fitness","food":"food","freelancing":"freelancing","future":"future","gadgets":"gadgets","gaming":"gaming","gun-control":"gun-control","health":"health","history":"history","humor":"humor","immigration":"immigration","ios-development":"ios-development","javascript":"javascript","justice":"justice","language":"language","leadership":"leadership","lgbtqia":"lgbtqia","lifestyle":"lifestyle","machine-learning":"machine-learning","makers":"makers","marketing":"marketing","math":"math","media":"media","mental-health":"mental-health","mindfulness":"mindfulness","money":"money","music":"music","neuroscience":"neuroscience","nonfiction":"nonfiction","outdoors":"outdoors","parenting":"parenting","pets":"pets","philosophy":"philosophy","photography":"photography","podcasts":"podcast","poetry":"poetry","politics":"politics","privacy":"privacy","product-management":"product-management","productivity":"productivity","programming":"programming","psychedelics":"psychedelics","psychology":"psychology","race":"race","relationships":"relationships","religion":"religion","remote-work":"remote-work","san-francisco":"san-francisco","science":"science","self":"self","self-driving-cars":"self-driving-cars","sexuality":"sexuality","social-media":"social-media","society":"society","software-engineering":"software-engineering","space":"space","spirituality":"spirituality","sports":"sports","startups":"startup","style":"style","technology":"technology","transportation":"transportation","travel":"travel","true-crime":"true-crime","tv":"tv","ux":"ux","venture-capital":"venture-capital",
            "visual-design":"visual-design","work":"work","world":"world","writing":"writing"}

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

#------------------------INPUTS-----------------------------------------------#

#to generalize this scraper for later use - EDIT THIS to suit your purposes
#keep all list items strings, or else this doesn't work

tags = list(allTopic.values()) ## ["Artificial-Intelligence"] #tags to scrape
years = ['2022'] #years to scrape during
months = ['06', '07', '08'] #months to scrape during (every available day within the month will be scraped)
textName = "mediumText.txt" #name of the output file

#don't touch unless you need to
hdr = {'User-Agent': 'Mozilla/5.0'}


#------------------------Get Top Tags------------------------------------#
from collections import defaultdict
tagInfo = defaultdict(list)

for tag in tags:
    # tag = 'visual-design'
    startLink = "https://medium.com/tag/"+tag
    
    response = requests.get(startLink, allow_redirects=True)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser')
    articleAuthor = soup.find_all('p', {'class':"bm b dm dn fv"})
    article, author = articleAuthor[0].contents[0], articleAuthor[1].contents[0]
    tagInfo[tag].append([article, author])
    print(f'**** {tag} = {[article, author]} ***')

tagDF = pd.DataFrame([[k] + j for k,v in tagInfo.items() for j in v], columns=['Topic', 'Article', 'Author'])

def numFormat(curVal):
    if 'K' in curVal:
        curVal = int(float(curVal.replace('K', '')) * 1000)
    else:
        curVal = int(curVal)
    return curVal
        
tagDF['Article'] = tagDF['Article'].apply(lambda x:  int(float(x.replace('K', '')) * 1000) if 'K' in x else int(x))
tagDF['Author'] = tagDF['Author'].apply(lambda x:  int(float(x.replace('K', '')) * 1000) if 'K' in x else int(x))
tagDF['ArticleRank'] = tagDF['Article'].rank(ascending=False).astype('int')
tagDF['WriterRank'] = tagDF['Author'].rank(ascending=False).astype('int')
tagDF.loc[tagDF['ArticleRank'].isin(list(range(51))), 'Topic']

TopTags = list(tagDF.sort_values('Article', ascending=False).iloc[:50]['Topic'])
tagDF = tagDF.sort_values('Article', ascending=False)


tagDF.to_excel('article.xlsx', index=False)

'''
(How to get the) Top Meduim tags with the highest numbers/largest number of articles

I compiled a list of Meduim tags/topics and scraped the meta-data about these tags, which includes # of articles and # of authors
published under each tag. (insert a screenshot)
of all time  

I scraped and extracted meta-data from Medium. 

These are the top tags having the largest numbers of articles, 
but this data does not provide information about popularity of these articles. 
By popularity, I mean questions such as how many Views and Likes these articles get? 
which tags are more likely to get viral articles that have earned 1000+ Likes? 
which tags have more viral articles that have earned 1000+ Likes? 


Most popular tags/Go viral tags

To get the most recent data, I focused on all articles published under each tag in Jun, July and Aug, 2022. 
Another consideration of selecting these 3 months is that as of Oct, when my analysis is done, 
articles published in these 3 months would have enough time to gain traction and get reliable amount of data on views/likes.




'''


#############================= Bar chart
# import matplotlib.pyplot as plt
# # creating the dataset
# fig = plt.figure(figsize = (10, 5))
 
# # creating the bar plot
# plt.bar(tagDF['Topic'], tagDF['Article'], color ='blue',
#         width = 0.4)
 
# plt.xlabel("Medium Tags")
# plt.ylabel("No. of articles")
# plt.title("Articles with each tag")
# plt.show()

####== 
import matplotlib.pyplot as plt
# Figure Size
fig, ax = plt.subplots(figsize =(20, 15)) ## 16, 10
 
# Horizontal Bar Plot
ax.barh(tagDF['Topic'][:30], tagDF['Article'][:30], alpha = 0.8)
 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10, labelsize = 22)
ax.xaxis.label.set_size(20)
ax.yaxis.label.set_size(30)

 
# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
# Show top values
ax.invert_yaxis()
 
# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 15, fontweight ='bold',  ## 8
             color ='grey')
 
# Add Plot Title
ax.set_title('Top 30 Tags with the Largest Number of Articles',
             loc ='left', fontsize=30)
 
# Add Text watermark
fig.text(0.9, 0.15, 'Created by Kat Li', fontsize = 12,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)
 
# Show Plot
plt.show()




#------------------------SCRAPER FUNCTIONS------------------------------------#
import re
#INPUT - components needed to get the start link
#OUTPUT - the links of all the articles in the tag in the date range
def scrapeLinksToArticles(tag, years, months):
    startLink = "https://medium.com/tag/"+tag+"/archive/"
    articleLinks, titlesList, likesList = [], [], []   
    
    for y in years:
        yearLink = startLink + y
        for m in months:
            monLink = yearLink + "/" + m
            #open the month link and scrape all valid days (days w/ link) into drive
            req = Request(monLink,headers=hdr)
            page = urlopen(req)
            monSoup = BeautifulSoup(page)
            try: #if there are days
                allDays = list(monSoup.find("div", {"class": "col u-inlineBlock u-width265 u-verticalAlignTop u-lineHeight35 u-paddingRight0"}).find_all("div", {"class":"timebucket"}))
                for a in allDays:
                    print(f'Working on {m}/{a}')
                    try: #try to see if that day has a link
                        dayLink = a.find("a")['href']
                        req = Request(dayLink, headers=hdr)
                        page = urlopen(req)
                        daySoup = BeautifulSoup(page)
                        links = list(daySoup.find_all("div", {"class": "postArticle-readMore"}))
                        
                        ## article title:
                        titles = daySoup.find_all("h3", class_="graf--title")
                        for title in titles:                            
                            if title is None:
                                title = ''
                            else:                            
                                title = title.contents[0]                        
                                ## only get text excluding web tags
                                if type(title) != str: title = title.get_text().replace('\xa0', ' ')
                            titlesList.append(title)
                        
                        ## likes: 
                        ### this will not give claps = 0
                        ## daySoup.find_all('button', class_ ='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents')
                        claps = re.findall('"totalClapCount":(\d+)', str(daySoup)) 
                        likesList.append(claps)
                        # likesListDict[f'{m}/{day}'].append(claps)
            
                        ## artile hyperlinks:
                        for l in links:
                            articleLinks.append(l.find("a")['href'])
                        
                        # articleLinksDict[f'{m}/{day}'].append(articleLinks)
                        # titlesListDict[f'{m}/{day}'].append(titlesList)                        
                        
                    except: pass
            except: #take the month's articles
                links = list(monSoup.find_all("div", {"class": "postArticle-readMore"}))
                for l in links:
                    articleLinks.append(l.find("a")['href'])
                print("issueHere")
    print("Article Links: ", len(articleLinks))
    return articleLinks, titlesList, likesList


#INPUT - link to a medium article
#OUTPUT - string with all the article text
def scrapeArticle(link):
    bodyText = ""
    req = Request(link,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)    
    textBoxes = list(soup.find("article", {"class": "meteredContent"}).find_all("p"))
    for t in textBoxes:
        bodyText = bodyText + t.get_text()
    return bodyText

#------------------------PROCESS----------------------------------------------#
from time import time
import pickle
#tags = TopTags
# tags = ['blockchain'] ## ['cryptocurrency']
# articleLinks = []

# tag = 'blockchain'
# articleLinks, titlesList, totalLikes = scrapeLinksToArticles(tag, years, months)

likesDict = dict()
for tag in TopTags:
    print(f'=== Start tag {tag} ===')
    articleLinks, titlesList, totalLikes = scrapeLinksToArticles(tag, years, months)
    likesDict[tag] = totalLikes
    # # myFile = open('LikesDict_46after.pkl', 'wb')
    # myFile = open('LikesDict_50after.pkl', 'wb')

    # pickle.dump(likesDict, myFile)
    # myFile.close()

myFile = open('LikesDict_50after.pkl', 'wb') 
pickle.dump(likesDict, myFile)  
myFile.close()

 
# with open('LikesDict_46after.pkl', 'rb') as file:
#     dd46 = pickle.load(file)
# dd46

import os
os.chdir(r'C:\Users\YLi\Downloads\Tags')
with open('LikesDict_50after.pkl', 'rb') as file:
    dd = pickle.load(file)
# dd

# dd.update(dd46)

[len(likesDict[tag]) for tag in likesDict.keys()]

    
likesDict = dd
import numpy as np

summaryDict = {}
summaryData = pd.DataFrame(columns=['Topic', 'Total', 'Viral', 'Ratio', 'TotLikes', 'AvgLikes'])
for ix, tag in enumerate(likesDict.keys()):    
    total = [float(j) for i in likesDict[tag] for j in i]
    totalCnt = len(total)
    totalLikes = np.sum(total)
    avgLikesPerDay = np.round(totalLikes/len(likesDict[tag]), 3)
    
    viral = len([i for i in total if i >= 1000])
        
    # len([i for i in total if i >= 1000]) / len(total)
    # len([i for i in total if i >= 500 and i < 1000])/len(total)
    # len([i for i in total if i >= 100 and i < 500])/len(total)

    ratio = np.round(viral/len(total), 3)
    # summaryDict[tag] = [totalCnt, viral, ratio, totalLikes, avgLikesPerDay]
    summaryData.loc[ix] = [tag, totalCnt, viral, ratio, totalLikes, avgLikesPerDay]
    
    print(f'==== {tag}: total = {totalCnt}; Viral = {viral}; Ratio = {ratio}; TotLikes = {totalLikes}; AvgLikes = {avgLikesPerDay} ====')

summaryData = summaryData.sort_values('Ratio', ascending=False).reset_index(drop=True)

# myFile = open('SummaryData.pkl', 'wb')
# pickle.dump(summaryData, myFile)
# myFile.close()
summaryData.to_excel('SummaryData_50after.xlsx', index=False)



# summaryData = pd.DataFrame(summaryDict)
# pd.DataFrame.from_dict(summaryDict)
# pd.DataFrame(list(summaryDict.items()) )
    
    
##=============== radar chart
from matplotlib import pyplot as plt
categories = ['Total', 'Viral', 'Ratio']## , 'AvgLikes', 'Affordability']
categories = [*categories, categories[0]]

## convert to ratio-> viral articles:total articles; 
# tag1 = [0.0168, 0.0307, 0.1659]
# tag2 = [0.0208, 0.0438, 0.15449]
# tag3 = [0.01074, 0.0100, 0.114]

tag1 = [18365/1000,  1885/100, 10.3]
tag2 = [8194/1000,   787/100, 9.6]
tag3 = [7769/1000,   662/100, 8.5]
tag4 = [7904/1000,   606/100, 0.07700*100]
tag5 = [11149/1000,    32/100, 0.00300*100]
tag6 = [12900/1000,   382/100, 0.03000*100]

restaurant_1 = tag1
restaurant_2 = tag2
restaurant_3 = tag3

restaurant_1 = [*restaurant_1, restaurant_1[0]]
restaurant_2 = [*restaurant_2, restaurant_2[0]]
restaurant_3 = [*restaurant_3, restaurant_3[0]]
tag4 = [*tag4, tag4[0]]
tag5 = [*tag5, tag5[0]]
tag6 = [*tag6, tag6[0]]


label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(restaurant_1))

plt.figure(figsize=(8, 8))
plt.subplot(polar=True)
plt.plot(label_loc, restaurant_1, label='Writing')
plt.plot(label_loc, restaurant_2, label='Humor')
plt.plot(label_loc, restaurant_3, label='Culture')
plt.plot(label_loc, tag4, label='Self')
plt.plot(label_loc, tag5, label='Data Science')
plt.plot(label_loc, tag6, label='Money')

plt.title('Comparison of Medium Articles Tags', size=20, y=1.05)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend()
plt.show()


######======== Plot all
outList = []
for ix, row in summaryData.iterrows():
    tag = [row['Total']/1000, row['Viral']/1000, row['Ratio']*100]
    tagUpdate = [*tag, tag[0]]
    outList.append(tagUpdate)
    
outLabels = list(summaryData.Topic)

label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(restaurant_1))

plt.figure(figsize=(8, 8))
plt.subplot(polar=True)

ixToPlot = [ix for ix, i in enumerate(summaryData.Topic) if i in 
            ['writing', 'poetry', 'mental-health', 'productivity', 'lifestyle', 
             'cryptocurrency', 'artificial-intelligence', 'programming', 'leadership', 'education']]

# for i in range(len(outLabels)):
for i in ixToPlot:
    plt.plot(label_loc, outList[i], label=outLabels[i])

plt.title('Medium article tags comparison', size=20, y=1.05)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend()
plt.show()

















totalLikes = [j for i in totalLikes for j in i]
len(articleLinks)
len(titlesList)
len(totalLikes)
len([i for i in totalLikes if float(i) >= 1000])/len(totalLikes)
len([i for i in totalLikes if float(i) >= 800])/len(totalLikes)


#####=================================================================#############
#####===== OLD EXPLORATIONS ==========================================#############
# start = time()
# for tag in tags: 
#     articleLinks.extend(scrapeLinksToArticles(tag, years, months)[0])
# articleLinks = set(articleLinks) #get rid of any duplicates
# end = time()
# print(f'** total time = {(end-start)/60} mins **')


# articleLinks = list(articleLinks)
# import re
# start = time()
# dataFile = defaultdict(list)

# start = time()
# for ix, url in enumerate(articleLinks):
#     title, subtitle, claps = '', '', 0
#     try:        
#         response = requests.get(url, allow_redirects=True)
#         page = response.content
#         soup = BeautifulSoup(page, 'html.parser')
#     except: 
#         pass 
#     try:
#         title = soup.find("h1").contents[0]
#     except:
#         pass
#     try:
#         subTitle = soup.find("h3").contents[0]
#     except:
#         pass
#     try:
#         claps = re.search('"clapCount":(\d+)', str(soup))    
#         claps = claps.group(1)
#     except:
#         pass 
#     dataFile[url].append([tag, title, subtitle, claps])
#     print(f'*** Done {ix} with Claps = {claps} ***')
# end = time()
# print(f'** total time = {(end-start)/60} mins **')



# # from copy import deepcopy
# # dataFileCropto = deepcopy(dataFile)
# # dataFileBlockChain = deepcopy(dataFile)
# len([i for i in dataFile['articleLinks'] if int(float(i[3]))>=1000])
# good = []
# for i in dataFile['articleLinks']:
#     if not i[3]:
#         print(i)
#         continue 
#     else:
#         if float(i[3])>=1000: 
#             good.append(i[3])
# len(good)


# outPutText = open(textName, "a+", encoding='utf8')
# count = 0
# for art in articleLinks:
#     print(count)
#     outPutText.write(str(scrapeArticle(art)))
#     count += 1    
# outPutText.close()