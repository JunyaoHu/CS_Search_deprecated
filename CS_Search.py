from time import sleep

from msedge.selenium_tools import Edge, EdgeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By


def get_article_word(driver, string):
    try:
        article_name = driver.find_element(By.CSS_SELECTOR, "body > div.container > form > div > h1").text
        article_content = driver.find_element(By.CSS_SELECTOR, "body > div.container > form > div").text
        state = article_content.find(string)
        if state != -1:
            f = open('text/需修改_' + article_name.replace('"', "_") + '_' + string + '.txt', 'w', encoding='utf-8')
            f.write(driver.current_url + '\n')
            f.write(string + '\n')
            f.write(article_content)
            f.close()
            print('\n【需修改】' + article_name + ' have ' + string)
        driver.close()
    except NoSuchElementException:
        print("无权限、重定向或者文件")
        driver.close()
    except TimeoutException:
        print("超时")
        driver.close()
    except AttributeError:
        print("文件链接，自动下载")


def search(string):
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("headless")
    driver = Edge(executable_path='src/msedgedriver.exe', options=options)

    driver.implicitly_wait(10)
    driver.get(r'http://cs.cumt.edu.cn')
    driver.set_window_size(width=300, height=600, windowHandle='current')
    # 找搜索框，输入关键词
    search_box = driver.find_element(By.CSS_SELECTOR, "#showkeycode1021687")
    search_box.send_keys(string)
    search_box.submit()

    # 检索标签页
    handle_main = driver.current_window_handle

    # 检查总页数
    try:
        total_num_box = driver.find_element(By.CSS_SELECTOR,
                                            "body > div.container > table > tbody > tr > td > a:nth-child(2)")
        total_num = eval(str(total_num_box.get_attribute('href')).split('=')[-2].split('&')[0])
    except NoSuchElementException:
        total_num = 1

    count = 1
    while count <= total_num:
        cur_page_all_article = driver.find_elements(By.XPATH, "/ html / body / div[3] / ul / li")
        cur_total = len(cur_page_all_article)
        cur = 0
        for article in cur_page_all_article:
            cur += 1
            driver.implicitly_wait(10)
            article.click()
            print("\r({:2}/{:2}) ({:4}/{:4}) [{}]\t".format(cur, cur_total, count, total_num, article
                                                            .text[2:]
                                                            .replace('\n', ' ')), end='')

            # 找到新标签页
            handle_all = driver.window_handles  # 只有2个窗口时
            handle_new = ""
            for h in handle_all:
                if h != handle_main:
                    handle_new = h
            driver.switch_to.window(handle_new)

            # 读取该文章信息
            get_article_word(driver, string)

            driver.switch_to.window(handle_main)

        if total_num != 1 and count == 1:
            driver.find_element(By.XPATH, "/html/body/div[3]/table/tbody/tr/td/a[1]").click()
        elif total_num != 1 and count < total_num:
            driver.find_element(By.XPATH, "/html/body/div[3]/table/tbody/tr/td/a[3]").click()
        else:
            pass
        driver.implicitly_wait(10)
        sleep(1)
        count += 1

    driver.quit()


wrong_words = ["习近平新时代中国特色社会主义经济思想",
               "习近平同志为首",
               "习近平法制思想",
               "习 近 平",
               "社会主义道理",
               "社会注意",
               "纪念建党",
               "纪念中国共产党成立",
               "劳记使命",
               "党史教育专题学习",
               "党史教育学习",
               "党史学教育",
               "当时学习教育",
               "不记初心",
               "爱国主意",
               "爱国注意"]
for word in wrong_words:
    print("\n------------------" + word + "---------------------")
    search(word)
