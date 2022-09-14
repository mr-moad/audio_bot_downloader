from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re
import os


def grab_single_mp3_links(link):
    all_links = []
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.maximize_window()
    driver.get(link)
    items_count = driver.execute_script("return document.querySelector('.results_count').innerText")
    number_of_items = int(items_count.split(" ")[0])
    number_of_mp3_links = 0
    while int(number_of_mp3_links) < number_of_items:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        mp_links = driver.execute_script("return document.querySelector('.results').querySelectorAll('a:not("
                                         ".stealth)').length")
        number_of_mp3_links = int(mp_links)
        links_elements = driver.execute_script("return document.querySelector('.results').querySelectorAll('a:not("
                                               ".stealth)')")
        for a_tag in links_elements:
            all_links.append(a_tag.get_attribute('href'))
    driver.quit()
    return all_links


def get_all_downloadable_links(links):
    all_mp3_links = []
    for link in links:
        res = requests.get(link)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if 'VBR MP3' in a.text and a['href'].endswith(".mp3"):
                    mp_name = re.search(r"([^\/]+$)", link).group()
                    os.system('cls')
                    print(f"Downloading File {mp_name}\n")
                    download = requests.get('https://archive.org' + a['href'])
                    if download.status_code == 200:
                        with open('files/' + mp_name+'.mp3', 'wb') as f:
                            f.write(download.content)
                    else:
                        print(f"Download Failed For File {mp_name}")
                    all_mp3_links.append(a['href'])
                    break
    return all_mp3_links


if __name__ == "__main__":
    with open('links.txt', "r+") as links_file:
        links_data = links_file.read().splitlines()
        for link in links_data:
            all_links = grab_single_mp3_links(link)
            get_all_downloadable_links(links=all_links)
