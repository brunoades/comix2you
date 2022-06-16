import errno
from playwright.sync_api import sync_playwright
from wget import download
from bs4 import BeautifulSoup as bs
import time, random, sys

url = str(sys.argv[1])

def get_comic(firstPage, lastPage, comic_url):
    with sync_playwright() as p:
        for i in range(firstPage, lastPage):
            browser = p.chromium.launch()
            page = browser.new_page()
            url = comic_url[:-1]
            page.goto(f"{url}{i}")
            wait_time = random.randint(1, 5)
            print(f"Dormindo por {wait_time} segundos.")
            time.sleep(wait_time)
            image_element = page.locator('id=imgCurrent').get_attribute('src')
            download(image_element)
            print(image_element)
            browser.close()

def get_pages(origin_url):
    with sync_playwright() as gp:
        browser = gp.chromium.launch()
        page = browser.new_page()
        url = origin_url
        page.goto(url)
        pages_selector = page.query_selector('#selectPage')
        soup = bs(pages_selector.inner_html(), 'html.parser')
        start = len(soup.find("option"))
        end = len(soup.find_all("option"))
        browser.close()
    get_comic(start, end, origin_url)

def main():
    get_pages(url)

if __name__ == "__main__":
    main()