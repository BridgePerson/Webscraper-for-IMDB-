#This is the scraper for imdb page
from bs4 import BeautifulSoup
import requests
from nordvpn_switcher import terminate_VPN, rotate_VPN, initialize_VPN
from itertools import cycle
import time
import json
import csv
from os.path import exists
import os

#class to make a movie's profile.
class Movie:
    def __init__(self, title="", genre="", length="", release="", age="", score="", director="", description=""):
        self._title=title
        self._genre= genre
        self._length= length
        self._release= release
        self._age= age
        self._score= score
        self._director= director
        self._description=description

    def getTitle(self):
        return self.title
    def setTitle(self, x):
        self._title=x

    def getGenre(self):
        return self._genre
    def setGenre(self, x):
        self._Genre=x

    def getLength(self):
        return self._length
    def setLength(self, x):
        self._length=x

    def getRelease(self):
        return self._release
    def setRelease(self, x):
        self._release=x

    def getAge(self):
        return self._age
    def setAge(self, x):
        self._age=x

    def getScore(self):
        return self._score
    def setScore(self, x):
        self._score=x

    def getDirector(self):
        return self._director
    def setDirector(self, x):
        self._director=x

    def getDescription(self):
        return self._description
    def setDescription(self, x):
        self._description = x

def main():
    
    #changeip
    instructions = initialize_VPN(area_input=['United States']) 
    url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&countries=us&languages=en'
    filename = "moviecw.csv"
    if os.path.exists(filename):
        ok=1
    else:
        fields = ['Title', 'Score IMBD', 'Age Rating', 'Runtime', 'Genres', 'Description', 'Release', 'Director']
        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    numoftitles=soup.find('div', attrs={'desc'})
    number=numoftitles.find('span').text.split(" ")[2]
    number=number.replace(',', '')
    i=0
    links=soup.findAll('div', attrs={'class':"lister-item-image float-left"})
    print(links[0].a['href'] +'?ref_=adv_li_i')
    #change ip
    t=0
    for i in range(int(number)): #range(50):
        if (i % 50 == 1 and i!=1):
            nextpage=soup.find('a',attrs='lister-page-next next-page')
            href=nextpage.get('href')
            url = 'https://www.imdb.com/' + href
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            t=-1
        elif(i == range(int(number))):
            terminate_VPN()
            quit()
        elif(i % 500 == 0):
            #change ip
            t=t
            rotate_VPN(instructions)
        else:
            links=soup.findAll('div', attrs={'class':"lister-item-image float-left"})
            link=('https://www.imdb.com'+links[t-1].a['href'] +'?ref_=adv_li_i')
            print (link)
            with open(filename, 'a') as csvfile: 
                csvwriter = csv.writer(csvfile)
                Scrapepage(link, csvwriter)
            i+=1
            t+=1
            try:
                print(i) 
            except:
                print(i)
            # creating a csv writer object 

    #        Scrapepage('https://www.imdb.com/title/tt1877830/?ref_=adv_li_tt', csvwriter)
    #        Scrapepage('https://www.imdb.com/title/tt2463208/?ref_=adv_li_tt', csvwriter)  

    
    #print(soup)
    #terminate_VPN(settings)

    #print(BeautifulSoup(response.text, 'html.parser'))

def Scrapepage(url, csvwriter):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('h1', attrs={'sc-b73cd867-0 eKrKux'})
    genres = soup.findAll('span', attrs={'class':'ipc-chip__text'})
    rating = soup.find('span', attrs={'class':'sc-7ab21ed2-1 jGRxWM'})
    release = soup.find('span', attrs= {'class' : 'sc-52284603-2 iTRONr'})
    description = soup.find("meta", attrs = {'property' : "og:description"})
    age = soup.findAll('a', attrs={'class':'ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-52284603-1 ifnKcw'})
    length = soup.find('script', attrs={'type' : 'application/ld+json'})
    #I came I saw 
    #print(length)
    jsonData = json.loads(length.text)    #Convert to JSON Object.
    
    Title=jsonData['name']
    if(rating!=None):
         IMBDScore=rating.text
    else:
        IMBDScore= 'tba'
    if('contentRating' in jsonData):
        ageRating=jsonData['contentRating']
    else:
        ageRating='none'
    if('duration' in jsonData):
        runTime=jsonData['duration']
    else:
        runTime='tba'
    if('genre' in jsonData):
            Genres= jsonData['genre']
    else:
        Genres='tba'
    if(description != None):
        Description = description.get('content')
    else:
        Description='No description'
    if(release!=None):
        Release = release.text
    else:
        Release = 'unknown'
    if('director' in jsonData):
        Director = jsonData['director'][0]['name']
    else:
        Director = 'Unknown'
    
    csvwriter.writerows([[Title, IMBDScore, ageRating, runTime, Genres, Description, Release, Director]])

    #Print 
    #print(title.text)
    #print(rating.text)
    #print(genres[0].text, genres[1].text, genres[2].text)
    #print(release.text)
    #print(description.get('content'))
    #print(jsonData['contentRating'])
    #print(jsonData['duration'])
    #print(jsonData['director'][0]['name'])



    
        


if __name__=="__main__": 
    main() 
