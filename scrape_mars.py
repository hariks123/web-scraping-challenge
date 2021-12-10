from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():

    #Open Chrome browser
    executable_path = {'executable_path': ChromeDriverManager(log_level=0).install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Mars Newssite
    url='https://redplanetscience.com/'
    #Open Mars Newsite in browser.
    browser.visit(url)
    # delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=2)
    #Parse the page using Beautiful Soup
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    #Get First News Title from the web page
    news_title=soup.find('div',class_='content_title').text
    #print(news_title)
    #Get Pargraph Text
    news_p=soup.find('div',class_='article_teaser_body').text
    #print(news_p)

    #URL for Mars Space Images
    url='https://spaceimages-mars.com/'
    #Open Above URL in Chrome browser
    browser.visit(url)
    # delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    #Click on the Full Image
    browser.links.find_by_partial_text('FULL IMAGE').click()
    # delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=2)
    #Parse the page using Beautiful Soup
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    #Get Image URL
    image_url=soup.find('a',class_='showimg fancybox-thumbs')['href']
    #Createa a complete URL
    featured_image_url=url+image_url
    #print(featured_image_url)

    #Mars Facts URL
    url='https://galaxyfacts-mars.com/'
    #Read all tables in the webpage, this creates a list of dataframes
    tables=pd.read_html(url)
    #Get the table with facts about Mars Earth Compasision into a dataframe
    df=tables[0]
    df.rename(columns={0:'Description',1:'Mars',2:'Earth'},inplace=True)
    df.set_index('Description',inplace=True)
    #Write dataframe to a html table
    #df.to_html('MarsProfileTable.html',classes=['table', 'table-striped', 'table-hover'])

    #Mars Hemispheres
    url='https://marshemispheres.com/'
    #Open Above URL in Chrome browser
    browser.visit(url)
    # delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=2)
    #Parse the page using Beautiful Soup
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    #Get Count of links in the page
    linkcounts=int(soup.find('span',class_='count').text.split()[0])
    #Find all h3's
    h3=soup.find_all('h3')
    links=[] #Intialize list to capture all the links
    i=0 #Intialize variable to loop through all the links 
    for h in h3:
        if i<linkcounts:
            links.append(h.text) #Append link to eh list
        i=i+1
    #Intialize list to capture hemisphere dictionary
    hemisphere_image_urls = []
    for link in links: #For each link in the links list
        image_urls={} #Intialize dictonary to capture hemisphere info
        browser.links.find_by_partial_text(link).click() #Click on the link
        #Parse the page using Beautiful Soup
        html=browser.html
        soup=BeautifulSoup(html,'html.parser')
        #Get Image URL
        #imgurl=soup.find_all('img',class_='wide-image')[0]['src']
        #imgurl=soup.find_all('img',class_='thumb')[0]['src']
        imgurl=soup.find('li').a.get('href')
        #Add key,value pair to hemisphere dict
        image_urls['title']=link
        image_urls['img_url']=url+imgurl #add full link to the image
        #append hemisphere info to a list for all hemispheres
        hemisphere_image_urls.append(image_urls)
        #Go back in the browser page to main page with all links
        browser.links.find_by_partial_text('Back').click()
    #print(hemisphere_image_urls)

    #close browser
    browser.quit()

    #Intialize dict to return
    mars={}
    mars['news_title']=news_title
    mars['news_p']=news_p
    mars['featured_image_url']=featured_image_url
    mars['hemispheres']=hemisphere_image_urls
    mars['facts']=df.to_html(classes=['table', 'table-striped', 'table-bordered'])
    #print(mars)

    return mars

