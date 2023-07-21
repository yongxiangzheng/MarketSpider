import os
import json
import sys
import time
import random
import tkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from playsound import playsound
import functions.jdSpiderDependence as jds
import requests
from PIL import Image
from io import BytesIO

VERSION = '1.3'
print(f'程序版本{VERSION}\n最新程序下载地址:https://github.com/yongxiangzheng/MarketSpider.git')

# 全局变量状态文字
gui_text = {}
gui_label_now = {}
gui_label_eta = {}

# 已下载图片的URL集合
downloaded_urls = set()

# 启动浏览器
print('正在启动浏览器')
options = webdriver.EdgeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Edge(options=options)
browser.get('https://mobile.yangkeduo.com')

# cookie相关
print('正在清空Cookie')
browser.delete_all_cookies()
print('正在注入Cookie')
try:
    with open('pinduoduo.cookie', 'r') as f:
        cookie_list = json.load(f)
        for cookie in cookie_list:
            browser.add_cookie(cookie)
except:
    print('未找到Cookie')
print('正在刷新浏览器')
browser.refresh()

while 1:
    # 输入店铺名称
    store_name = input('请输入店铺名称进行下载（无输入则结束）:')
    if store_name == '':
        break
    image_elements = browser.find_elements(By.XPATH, '//img[@aria-label="商品大图" or @aria-label="查看图片"]')

    for index, img_element in enumerate(image_elements):
        image_url = img_element.get_attribute('src')
        aria_label = img_element.get_attribute('aria-label')

        if image_url and aria_label:
            # 检查图片URL是否已经下载过，如果已经下载则跳过
            if image_url in downloaded_urls:
                print(f"Image {index + 1} with aria-label '{aria_label}' already downloaded.")
                continue

            response = requests.get(image_url)

            if response.status_code == 200:
                # 将二进制数据转换为图像
                try:
                    img = Image.open(BytesIO(response.content))
                except:
                    continue

                # 创建目录层级：images/店铺名称/aria-label/
                sub_directory = os.path.join("images", store_name, aria_label)
                os.makedirs(sub_directory, exist_ok=True)

                # 设置本地文件名
                filename = os.path.join(sub_directory, f"image_{index + 1}.png")

                # 保存图片为PNG格式到本地
                img.save(filename, "PNG")

                print(f"Image {index + 1} with aria-label '{aria_label}' downloaded and saved as {filename}")

                # 将已下载的图片URL添加到集合中
                downloaded_urls.add(image_url)
            else:
                print(f"Failed to download Image {index + 1}")

    print('图片保存完成!')

print('程序结束')
browser.close()
sys.exit()
