from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

#Obtém uma lista com todos os links internos encontrados em uma página
def getInternalLinks(bs, includeUrl):
  includeUrl = f'{urlparse(includeUrl).scheme}://{urlparse(includeUrl).netloc}'
  internalLinks = []

  #Encontra todos os links que começam com "/"
  for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
    if link.attrs['href'] is not None:
      if link.attrs['href'] not in internalLinks:
        if(link.attrs['href']).startswith('/'):
          internalLinks.append(includeUrl+link.attrs['href'])
        else:
          internalLinks.append(link.attrs['href'])
  return internalLinks


#Obtém uma lista de todos os links externos encoonotrados em uma página
def getExternalLinks(bs, excludeUrl):
  externalLinks = []

  #Encontra todos os links que começam com "http" e que não contenham o URL atual
  for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
    if link.attrs['href'] is not None:
      if link.attrs['href'] not in externalLinks:
        externalLinks.append(link.attrs['href'])
  return externalLinks

def getRandomExternalLink(startingPage):  
  html = urlopen(startingPage)
  bs = BeautifulSoup(html,'html.parser')

  externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)

  if len(externalLinks) == 0:
    print('No external links, looking around the site for one')
    domain = f'{urlparse(startingPage).scheme}://{urlparse(startingPage).netloc}'
    internalLinks = getInternalLinks(bs, domain)
    return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
  else:
    return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
  externalLink = getRandomExternalLink(startingSite)
  print(f'Random external link is: {externalLink}')
  
  followExternalOnly(externalLink)

followExternalOnly('http://oreilly.com')