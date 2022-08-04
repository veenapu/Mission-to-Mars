# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #  Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None,None

    return news_title, news_p    


#  10.3.4 Scrape Mars Data: Featured Image
# ### JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except block for error handling
    try:
        #  use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
     
    except AttributeError:
        return None

    # add the base URL to our code and Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        #  scrape the entire table with Pandas' .read_html() function.
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # assign columns and set index of DataFrame
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # convert DataFrame back into HTML-ready code using the .to_html() function, add bootstrap. 
    return df.to_html(classes="table table-stripped")

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere
    for i in range(4):
        browser.find_by_css('a.product-item h3')[i].click()
        
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_image_urls.append(hemisphere_data)
       
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    
    # Parse html
    hemisphere_soup = soup(html_text, "html.parser")

    # error handling using try/except
    try:
        title_elem = hemisphere_soup.find("h2", class_="title").get_text()
        sample_elem = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem

    }    
    return hemispheres

if __name__ == "__main__":
    print(scrape_all())

