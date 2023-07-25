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
            driver.get(url_login)

            zhanghao_mima = driver.find_element(By.ID, 'zh')
            zhanghao_mima.click()
            # 定位账号，密码，验证码和登录按钮部分
            username_input = driver.find_element(By.ID, 'loginUserId')
            password_input = driver.find_element(By.ID, 'loginPassword')
            captcha = driver.find_element(By.ID, 'yzm')
            login_button = driver.find_element(By.CLASS_NAME, 'login_button')
            username_input.send_keys(user_name)  # 填写用户名 zhjk2019
            password_input.send_keys(secret)  # 填写密码 535cmeyr
            # 识别验证码部分
            png = driver.find_element(By.ID, 'randimg')
            screenshot = png.screenshot_as_png  # 获取屏幕截图的二进制数据
            image_stream = BytesIO(screenshot)  # 使用BytesIO创建一个内存文件对象
            image = Image.open(image_stream)  # 通过内存文件对象加载图像
            ocr = ddddocr.DdddOcr()  # 验证码识别库
            res = ocr.classification(image)
            captcha.send_keys(res)  # 输入识别的验证码
            login_button.click()
            # 等待页面跳转
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.url_to_be(url_target))
                time.sleep(5)
                cookie = driver.get_cookies()
                strr = ''
                for c in cookie:
                    strr += c['name']
                    strr += '='
                    strr += c['value']
                    strr += ';'
                st.success('获取cookies成功！')
                image_stream.close()  # 关闭内存文件对象
                break
            except:
                image_stream.close()  # 关闭内存文件对象
                continue
    return strr

def Create_dataframe():
    # 为创建的excel表格添加表头
    data_list = ['类型', '标题', '地区', '发布时间', '品牌', '供应商', '中标金额', '招标金额', '标的物', '对应网址',
                 '附件']
    # 创建空的DataFrame
    df = pd.DataFrame(columns=data_list)
    return df

def Analyze_Main_Url_1(main_url, keyword, Information_category, start_time, end_time, i, cookie):
    headers_1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '233',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 's.zhaobiao.cn',
        'Origin': 'https://s.zhaobiao.cn',
        'Referer': 'https://s.zhaobiao.cn/s',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    from_data_1 = {
        'queryword': keyword,
        'channels': Information_category,
        'starttime': start_time,
        'endtime': end_time,
        'currentpage': i
    }
    response_1 = requests.post(main_url, headers=headers_1, data=from_data_1)
    html_1 = etree.HTML(response_1.text)
    detail_Urls = html_1.xpath('.//tr[@class = "datatr"]')
    return detail_Urls

def Analyze_Main_Url_2(main_url, keyword, Information_category, year, month, i, cookie):
    headers_1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '233',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 's.zhaobiao.cn',
        'Origin': 'https://s.zhaobiao.cn',
        'Referer': 'https://s.zhaobiao.cn/s',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    from_data_1 = {
        'hisType': 'zb',
        'queryword': keyword,
        'channels': Information_category,
        'year': year,
        'month': month,
        'currentpage': i
    }
    response_2 = requests.post(main_url, headers=headers_1, data=from_data_1)
    html_2 = etree.HTML(response_2.text)
    detail_Urls = html_2.xpath('.//tr[@style = "border-bottom:1px dashed #ccc;"]')
    return detail_Urls

def Sift_Url(detail_Url, index, keyword_list, cookie):
    headers_2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '46',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'zb.zhaobiao.cn',
        'Origin': 'https://s.zhaobiao.cn',
        'Referer': 'https://s.zhaobiao.cn/s',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    from_data_2 = {
        'q': '%D0%C4%B5%E7%CD%F8%C2%E7',
        'm': '1'
    }
    url = detail_Url.xpath('td/a/@href')[index]
    st.write("正在爬取的网页是:", url)
    response_2 = session.post(url, headers=headers_2, data=from_data_2)
    html_2 = etree.HTML(response_2.text)
    contents = html_2.xpath('.//div[@class = "w-noticeCont"]/div[@class = "w-contIn page"]/script/text()')[0].strip()
    # 网页信息被编码了，提取编码
    secret = re.findall('var ss = "(.*)";', contents)[0]
    # 解码
    pass_word = urllib.parse.unquote(urllib.parse.unquote(secret))
    html_3 = etree.HTML(pass_word)
    texts = html_3.xpath('//text()')
    combine_texts = ' '.join(texts)
    for th in keyword_list:
        if th in combine_texts:
            type = detail_Url.xpath('td[@align="center"]/text()')[0]  # 类型
            title = html_2.xpath('//h1[@id="infotitle"]/text()')[0]  # 标题
            place = detail_Url.xpath('td[@align="center"]/text()')[1]  # 地点
            release_time = detail_Url.xpath('td[@align="center"]/text()')[2]  # 时间
            return type, title, place, release_time, html_3, url, th

def analysis_detail_Url(from_data_1_cannels, html_3, thing):
    brand = ''
    supplier = ''
    succeed_price = ''
    bidding_price = ''
    # 构建网页中的表格信息
    table_elements = html_3.xpath('//table')
    for table_element in table_elements:  # 遍历网页中所有的表格（构造表格为竖状表格）
        table = []
        # 确认解码网页中是否含有thead标签
        thead_elements = table_element.xpath('.//thead/th')
        if thead_elements:
            for thead in thead_elements:
                table.append(thead.xpath('.//th/text()'))
        for trs in table_element.xpath('.//tr'):
            table_2 = []
            # 确认解码网页中是否含有th标签
            if len(trs.xpath('.//th')) > 1:
                table.append(trs.xpath('.//th/text()'))
            else:
                for td in trs.xpath('.//td'):
                    if td.xpath('.//text()'):
                        if td.xpath('.//p'):
                            table_2.append(td.xpath('.//p')[0].xpath('string()').replace('\n', '').replace(' ', ''))
                        elif td.xpath('.//div'):
                            table_2.append(td.xpath('.//div')[0].xpath('string()').replace('\n', '').replace(' ', ''))
                        else:
                            table_2.append(td.xpath('string()').replace('\n', '').replace(' ', ''))
                    else:
                        table_2.append('-')
            # 如果table_2不空，添加到table表格
            if len(table_2) > 0:
                table.append(table_2)
        if len(table) != 0:
            # 获取每行的最大列数
            max_cols = max(len(row) for row in table)
            # 输出对齐后的二维列表
            aligned_list = [row + ['-'] * (max_cols - len(row)) for row in table]
            f = 0  # 扫描列的初始索引
            if len(aligned_list) > 1:
                for index, row in enumerate(aligned_list):  # 输出关键词所在的行索引
                    row = ' '.join(row)
                    if thing in row or len(aligned_list) <= 2:
                        if thing in row:
                            k = index
                        else:
                            k = 1
                        for columns in aligned_list[0]:
                            if '品牌' in columns and brand == '':
                                brand = aligned_list[k][f]
                            if any(th in columns for th in
                                       succeed_prices) and succeed_price == '' and from_data_1_cannels == 'succeed':
                                succeed_price = aligned_list[k][f]
                            if any(th in columns for th in bidding_prices) and bidding_price == '' and (
                                        from_data_1_cannels == 'bidding' or from_data_1_cannels == 'cgall'):
                                bidding_price = aligned_list[k][f]
                            if any(th in columns for th in suppliers) and supplier == '':
                                supplier = aligned_list[k][f]
                            f = f + 1  # 循环扫描列的索引
                # 将表格竖向转换为横向表格，通过字典的形式呈现
                dict_table = {}
                for row in aligned_list:
                    if len(row) % 2 == 0:
                        for i in range(0, len(row), 2):
                            if i + 1 < len(row):
                                dict_table[row[i]] = row[i + 1]
                if dict_table:
                    # 获取字典中所有的键并打印
                    keys = dict_table.keys()
                    for key in keys:
                        if '品牌' in key and brand == '':
                            brand = dict_table[key]
                        if any(th in key for th in
                               succeed_prices) and succeed_price == '' and from_data_1_cannels == 'succeed':
                            succeed_price = dict_table[key]
                        if any(th in key for th in
                               bidding_prices) and bidding_prices == '' and (
                                        from_data_1_cannels == 'bidding' or from_data_1_cannels == 'cgall'):
                            bidding_price = dict_table[key]
                        if any(th in key for th in suppliers) and supplier == '':
                            supplier = dict_table[key]

    # 扫描网页所有文本
    texts = html_3.xpath('//text()')
    for text in texts:
        text = text.replace("\n", "").replace("\r", "").strip()
        if '品牌' in text and brand == '' and re.search(r"[:：]\s*(.*)(?:，|$)", text) != None:
            brand = re.search(r"[:：]\s*(.*)(?:，|$)", text).group(1)

        for th in suppliers:
            pattern = r"{th}：(.*?)(?:，|$)".format(th=th)
            if th in text and supplier == '' and re.search(pattern, text) != None:
                supplier = re.search(pattern, text).group(1)

        if Information_category == 'succeed':
            for th in succeed_prices:
                pattern = r"{th}[^：]*：(.*?)(?:，|$)".format(th=th)
                if th in text and succeed_price == '' and re.search(pattern, text) != None:
                    succeed_price = re.search(pattern, text).group(1)

        if Information_category == 'bidding':
            for th in bidding_prices:
                pattern = r"{th}[^：]*：(.*?)(?:，|$)".format(th=th)
                if th in text and bidding_price == '' and re.search(pattern, text) != None:
                    bidding_price = re.search(pattern, text).group(1)
                    
    # 下载网页中存在的附件
    Appendix = ''
    if html_3.xpath('//a[@target="_parent"]'):
        for appendix in html_3.xpath('//a[@target="_parent"]'):
            appendix_URL = appendix.xpath('.//@href')[0]
            appendix_name = appendix.xpath('.//text()')[0]
            Appendix = '\n' + Appendix + appendix_name + ' :' + appendix_URL

    return brand, supplier, succeed_price, bidding_price, Appendix

def get_total_page_1(main_url, keyword, Information_category, start_time, end_time, cookie):
    headers_1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '233',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 's.zhaobiao.cn',
        'Origin': 'https://s.zhaobiao.cn',
        'Referer': 'https://s.zhaobiao.cn/s',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    from_data_1 = {
        'queryword': keyword,
        'channels': Information_category,
        'starttime': start_time,
        'endtime': end_time,
        'currentpage': 1
    }
    response_1 = requests.post(main_url, headers=headers_1, data=from_data_1)
    html_1 = etree.HTML(response_1.text)
    total_page = html_1.xpath('//form/input[@id ="totalPage"]/@value')[0]
    return total_page

def get_total_page_2(main_url, keyword, Information_category, year, month, cookie):
    headers_1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '233',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 's.zhaobiao.cn',
        'Origin': 'https://s.zhaobiao.cn',
        'Referer': 'https://s.zhaobiao.cn/s',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    from_data_1 = {
        'hisType': 'zb',
        'queryword': keyword,
        'channels': Information_category,
        'year': year,
        'month': month,
        'currentpage': 1
    }
    response_2 = requests.post(main_url, headers=headers_1, data=from_data_1)
    html_2 = etree.HTML(response_2.text)
    total_page = html_2.xpath('//form/input[@id ="totalPage"]/@value')[0]
    return total_page

def main(total_page):
    for i in range(1, int(total_page) + 1):
        if choose == '爬取一年内的数据':
            detail_urls = Analyze_Main_Url_1(main_url, keyword, Information_category, start_time, end_time, i, cookie)
        else:
            detail_urls = Analyze_Main_Url_2(main_url, keyword, Information_category, year, month, i, cookie)
        st.write(f'========================共需爬取{total_page}页，正在爬取第{i}页========================')
        for detail_url in detail_urls:
            LIST = []
            j = 0
            try:
                if Sift_Url(detail_url, j, keyword_list, cookie):
                    type, title, place, release_time, html_3, url, thing = Sift_Url(detail_url, j, keyword_list, cookie)
                    brand, supplier, succeed_price, bidding_price, appendix = analysis_detail_Url(Information_category, html_3, thing)
                    st.write("品牌：", brand)
                    st.write("供应商：", supplier)
                    if Information_category == 'succeed':
                        st.write("中标金额：", succeed_price)
                    if Information_category == 'bidding':
                        st.write("招标金额：", bidding_price)
                    st.write("标的物：", thing)
                    st.write("附件：", appendix)
                    # 合成二维列表
                    LIST.append(type)
                    LIST.append(title)
                    LIST.append(place)
                    LIST.append(release_time)
                    LIST.append(brand.replace(' ', ''))
                    LIST.append(supplier.replace(' ', ''))
                    LIST.append(succeed_price.replace(' ', ''))
                    LIST.append(bidding_price.replace(' ', ''))
                    LIST.append(thing.replace("/", ""))
                    LIST.append(url)
                    LIST.append(appendix)
                    df.loc[len(df)] = LIST
                    j = j + 1
            except:
                j += 1

def download_df_to_excel():
    # 创建一个内存文件对象
    excel_buffer = BytesIO()
    # 将 DataFrame 保存到内存文件对象中
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    # 获取内存文件对象的二进制数据
    excel_data = excel_buffer.getvalue()
    # 提供下载链接
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="data.xlsx">Download Excel File</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    # 获取cookies的urls
    login_url = 'http://user.zhaobiao.cn/login.html'
    url_target = 'https://user.zhaobiao.cn/homePageUc.do'
    # 查询网页所需要的关键字
    suppliers = ['供应商名称', '成交企业', '拟成交公司', '成交单位', '中标人', '成交候选人', '制造商', '成交供应商',
                 '中选机构', '拟中标公司', '中选人', '中标 (成交)单位']
    succeed_prices = ['成交价（元）', '中标金额', '中标（成交）金额', '总价(元)', '成交金额（元）',
                      '中标（成交）价', '成交价格', '拟成交金额', '中标（成交）结果', '报价（元）', '中选金额']
    bidding_prices = ['预算金额', '控制金额(元)', '招标控制价', '品目预算(元)', '最高限价', '项目预算',
                      '成交价（元）', '采购预算金额 （元）', '采购预算']
    # 创建一个会话对象保持动态连接
    session = requests.Session()
    st.set_page_config(page_title="招标网爬取工具")
    st.title("招标网爬取工具")   # Streamlit应用程序的标题和描述
    user_name = st.sidebar.text_input('输入用户名')
    secret = st.sidebar.text_input('输入密码')
    choose = st.sidebar.selectbox('爬取数据选项', ['爬取一年内的数据', '访问历史库往年数据'])
    if choose == '爬取一年内的数据':
        year_data = st.container()
        with st.form('year_data'):
            # 爬取的主页面
            main_url = 'https://s.zhaobiao.cn/s'
            df = Create_dataframe()
            keyword = st.text_input("请输入产品的关键词：")
            keyword_list = st.text_input("请输入具体的关键词（多个关键字用空格分隔）：").split()
            Information_category = st.text_input(
                '请根据提示输入你需要爬取的信息类别（如：招标公告、中标公告、采购公告）：')
            if Information_category == '招标公告':
                Information_category = 'bidding'
            elif Information_category == '中标公告':
                Information_category = 'succeed'
            elif Information_category == '采购公告':
                Information_category = 'cgall'
            start_time = st.text_input('请输入你要爬取的开始时间（如：20220605):')
            end_time = st.text_input('请输入你要爬取的结束时间（如：20220605):')
            submit_button = st.form_submit_button('开始爬取')
        if submit_button:
            cookie = Get_Cookies(login_url, url_target, user_name, secret)
            total_page_1 = get_total_page_1(main_url, keyword, Information_category, start_time, end_time, cookie)
            time.sleep(5)
            main(total_page_1)
            download_df_to_excel()
            st.write(df)
    if choose == '访问历史库往年数据':
        history_data = st.container()
        with st.form('history_data'):
            main_url = 'https://s.zhaobiao.cn/search/history/result'
            df = Create_dataframe()
            keyword = st.text_input("请输入产品的关键词：")
            keyword_list = st.text_input("请输入具体的关键词（多个关键字用空格分隔）：").split()
            Information_category = st.text_input(
                '请根据提示输入你需要爬取的信息类别（如：招标公告、中标公告、采购公告）：')
            if Information_category == '招标公告':
                Information_category = 'bidding'
            elif Information_category == '中标公告':
                Information_category = 'succeed'
            elif Information_category == '采购公告':
                Information_category = 'cgall'
            year = st.text_input('请输入你要需要访问的年份（如：2022):')
            month = st.text_input('请输入你要访问的月份（如：01):')
            submit_button = st.form_submit_button('开始爬取')
        if submit_button:
            cookie = Get_Cookies(login_url, url_target, user_name, secret)
            total_page_2 = get_total_page_2(main_url, keyword, Information_category, year, month, cookie)
            time.sleep(5)
            main(total_page_2)
            download_df_to_excel()
            st.write(df)
