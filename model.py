import time
import os,sys
# 禁用代理,防止 requests 无法访问 下载源
os.environ['no_proxy'] = '*'
# del os.environ['HTTP_PROXY']  # 取消禁用

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.core.http import HttpClient
from webdriver_manager.core.download_manager import WDMDownloadManager

import requests
from pathlib import Path

os.environ['WDM_SSL_VERIFY'] = '0'  # 禁用ssl验证
os.environ['WDM_LOG'] = "false"     # 禁用 webdriver_manager 日志
requests.packages.urllib3.disable_warnings()  # 关ssl警告


# 判断文件,创建 _driver 文件夹
if getattr(sys, 'frozen', False):  # 判断是exe还是.py程序
    dir_pre = Path(os.path.realpath(sys.executable)).parent  # exe程序路径
elif __file__:
    dir_pre = Path(__file__).parent  # .py程序路径
dir_driver = dir_pre/'_driver'
if not dir_driver.is_dir():
    dir_driver.mkdir()


class Global_g():
    def __init__(self):
        self.D_cur_browser = 'firefox'

        self.D_cur_version = None
        self.D_url_pre = None

g = Global_g()



# (todo) 自定义 下载的镜像网址(模块只支持 github 的api,这里可以自定义国内镜像)
class CustomHttpClient(HttpClient):
    def get(self, url, params=None, **kwargs) -> requests.Response:
        """
        Add you own logic here like session or proxy etc.
        """
        return requests.get(url, params, **kwargs)





#  封装 selenium
class Driver(object):
    def __init__(self):
        cur_driver = g.D_cur_browser
        if cur_driver=='firefox':
            driver = self.run_firefox()
        elif cur_driver=='edge':
            driver = self.run_edge()
        elif cur_driver=='ie':
            driver = self.run_ie()
        else:
            driver = self.run_chrom()



        self.driver = driver


    def get(self,url):
        '''
        重写 get,  如果url 不带 http, 就给url加上预设的前缀
        :param url:
        :return:
        '''
        if 'http' not in url:
            url = g.D_url_pre + url
        self.driver.get(url)
        return None











    def run_firefox(self):
        '''
        火狐浏览器设置, 并启动
        :return: driver
        '''
        ver = g.D_cur_version if g.D_cur_version else 'latest'


        service = FirefoxService(executable_path=GeckoDriverManager(path = dir_driver,version=ver,cache_valid_range=60).install())
        driver = webdriver.Firefox(service=service)

        return driver

    def run_chrom(self):
        '''
        谷歌浏览器设置, 并启动
        :return: driver
        '''
        ver = g.D_cur_version if g.D_cur_version else 'latest'


        service = ChromeService(executable_path=ChromeDriverManager(path = dir_driver,version=ver,cache_valid_range=60).install())
        driver = webdriver.Chrome(service=service)

        return driver

    def run_edge(self):
        '''
        edge浏览器设置, 并启动
        :return: driver
        '''
        ver = g.D_cur_version if g.D_cur_version else 'latest'


        service = EdgeService(executable_path=EdgeChromiumDriverManager(path = dir_driver,version=ver,cache_valid_range=60).install())
        driver = webdriver.Edge(service=service)

        return driver

    def run_ie(self):
        '''
        IE浏览器设置, 并启动
        :return: driver
        '''
        ver = g.D_cur_version if g.D_cur_version else 'latest'



        service = IEService(executable_path=IEDriverManager(path = dir_driver,version=ver,cache_valid_range=60).install())
        driver = webdriver.Ie(service=service)
        return driver



driver = Driver()
print(driver)
driver.get(r'https://www.baidu.com')


time.sleep(15)
driver.quit()






