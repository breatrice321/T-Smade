# Watch the video

from urllib import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import re
import time


def watch_the_vedio():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.bilibili.com/')
    time.sleep(1)

    #  Get the input box and press the Enter key to search.
    driver.find_element_by_class_name('nav-search-input').send_keys('计算机体系结构', Keys.ENTER)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    time.sleep(3)  # You must wait, otherwise it won't respond in time.

    # get all the divs under the condition that class: 'mt_sm video-list row'
    url = driver.current_url
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'
    req = request.Request(url, None, headers=headers)
    response = request.urlopen(req)
    html = BeautifulSoup(response, 'html.parser')
    div = html.find(attrs={'class': 'video-list row'})

    # Get the href URL from all divs
    div_list = []
    for div_sub in div:
        if div_sub.find('div') != -1:
            content = str(div_sub.find('div'))
            element = re.findall(r'.*href="//(.*)" target="_blank"><div class="bili-video-card', content)  # every url is ['url], thus we have to remove the redundant section
            if element == []:
                continue
            else:
                temp = element[0]  # remove[]
                temp = temp.strip()  # remove '
                temp = temp.lstrip()  # remove '
                div_list.append(temp)
                # print(temp)

    # open each url
    time_init = time.time()
    state = True
    while state:
        for div in div_list:
            # get a url
            href = 'http://' + div
            # Open the URL in a new tab
            driver.execute_script(f'window.open("{href}", "_blank");')
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])
            time.sleep(30)  # the last time

            driver.close()
            # Do not close; to go to the previous page, we need to move the handle.
            handles = driver.window_handles
            # print(handles)
            driver.switch_to.window(handles[-1])

            if time.time() - time_init > 598:
                driver.quit()
                break

        if time.time() - time_init > 598:
            state = False


if __name__ == "__main__":
    watch_the_vedio()