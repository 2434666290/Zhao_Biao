from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import ddddocr
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import streamlit as st
import base64
import requests
from lxml import etree
import re
import urllib.parse
from io import BytesIO
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
def Get_Cookies(url_login, url_target, user_name, secret):
    strr = ''  # 创建空的cookie值
    with st.spinner('Loading cookie...'):
        while (True):
            options = Options()
            options.add_argument('--disable-gpu')
            options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url_lo
