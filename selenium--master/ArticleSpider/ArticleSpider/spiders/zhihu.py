# -*- coding: utf-8 -*-
import scrapy


import time
from urllib import parse
from mouse import move,click
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']


    def start_requests(self):
        from selenium import  webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        chrome_option = Options()
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("debuggerAddress","127.0.0.1:9222")


        browser = webdriver.Chrome(executable_path='D:/Evns/article-spider/Scripts/chromedriver.exe',chrome_options=chrome_option)
        try:
            browser.maximize_window()
        except:
            pass

        browser.get("https://www.zhihu.com/signin")

        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL +'a')
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys('xxx')
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + 'a')
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys('xxx')
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(10)
        login_success = False
        if login_success:
            Cookies = browser.get_cookies()
            #print(Cookies)
            cookie_dict = {}
            import pickle
            for cookie in Cookies:
                # 写入文件
                # 此处大家修改一下自己文件的所在路径
                f = open('D:/py/ArticleSpider/cookies/' + cookie['name'] + '.zhihu', 'wb')
                pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
            browser.close()
            return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
        while not login_success:
            try:
                notify_ele = browser.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")
                login_success = True

                Cookies = browser.get_cookies()
                #print(Cookies)
                cookie_dict = {}
                import pickle
                for cookie in Cookies:
                    # 写入文件
                    # 此处大家修改一下自己文件的所在路径
                    f = open('d:/ArticleSpider/cookies/' + cookie['name'] + '.zhihu', 'wb')
                    pickle.dump(cookie, f)
                    f.close()
                    cookie_dict[cookie['name']] = cookie['value']
                browser.close()
                return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
            except:
                pass

            try:
                english_captcha_element = browser.find_element_by_class_name("Captcha-englishImg")
            except:
                english_captcha_element =None
            try:
                chinese_captcha_element = browser.find_element_by_class_name("Captcha-chineseImg")
            except:
                chinese_captcha_element = None


            if chinese_captcha_element:
                ele_postion = chinese_captcha_element.location
                x_relative = ele_postion["x"]
                y_relative = ele_postion["y"]
                browser_navigation_panel_height = 70
                base64_text =chinese_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace("data:image/jpg;base64,","").replace("%0A","")
                fh = open("yzm_cn.jpeg","wb")
                fh.write(base64.b64decode(code))
                fh.close()

                from zheye import zheye
                z= zheye()
                positions = z.Recognize('yzm_cn.jpeg')
                last_position = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        last_position.append([positions[1][1], positions[1][0]])
                        last_position.append([positions[0][1], positions[0][0]])
                    else:
                        last_position.append([positions[0][1], positions[0][0]])
                        last_position.append([positions[1][1], positions[1][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    second_position = [int(last_position[1][0] / 2), int(last_position[1][1] / 2)]
                    move(x_relative + first_position[0],
                         y_relative + browser_navigation_panel_height + first_position[1]+30)
                    click()

                    move(x_relative + second_position[0],
                         y_relative + browser_navigation_panel_height + second_position[1]+30)
                    click()

                else:
                    last_position.append([positions[0][1], positions[0][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    move(x_relative + first_position[0],
                         y_relative + browser_navigation_panel_height + first_position[1]+30)
                    click()

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + 'a')
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    'xxx')
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + 'a')
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys('xxx')
                browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
                move(672,564)
                click()

            if english_captcha_element:

                base64_text = english_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
                # print code
                fh = open("yzm_en.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                from tools.yundama_requests import YDMHttp
                yundama = YDMHttp("dingdapang", "123123", 7333, "1bb3a77475497442e99443717e204aa7")
                code = yundama.decode("yzm_en.jpeg", 5000, 60)
                while True:
                    if code == "":
                        code = yundama.decode("yzm_en.jpeg", 5000, 60)
                    else:
                        break
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(
                    code)

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "xxx")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys("xxx")
                move(668, 543)
                click()
        time.sleep(60)
    def parse(self, response):
        
        # all_urls = response.css("a::attr(href)").extract()
        # all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        # for url in all_urls:
        pass




