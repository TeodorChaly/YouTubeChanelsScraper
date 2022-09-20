from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

PATH = "C:\WEBDRIVER\chromedriver.exe"
option = webdriver.ChromeOptions()
#option.headless = True
option.add_argument("user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17")
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(PATH,chrome_options = option)

def filtering_links():
    print(1)

def scraping_search_page():
    count = 1
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        if count == 2:
            break
        count += 1

    epr = driver.find_elements(By.ID, "content-section")
    for i in epr:

        try:
            try:
                print(i.find_element(By.ID, "main-link").get_attribute("href"))
                sub = i.find_element(By.ID, "subscribers").text.split("подпи")[0]
                if "тыс" in i.find_element(By.ID, "subscribers").text.split("подпи")[0]:
                    # Тысячи
                    print("тыс")
                    number = sub.split("тыс")[0]
                    if number.count(",") != 0:
                        comma_id = number.find(",")
                        print(comma_id == 1, comma_id == 2)
                        if comma_id == 1:
                            print(1)
                            number1 = int(number.split(",")[0]) * 1000
                            number2 = int(number.split(",")[1]) * 10
                            full_number = number1 + number2
                        elif comma_id == 2:
                            print(2)
                            number1 = int(number.split(",")[0]) * 1000
                            number2 = int(number.split(",")[1]) * 100
                            full_number = number1 + number2
                    else:
                        full_number = int(number) * 1000
                elif "млн" in i.find_element(By.ID, "subscribers").text.split("подпи")[0]:
                    # Миллионы
                    print("млн")
                    number = sub.split("млн")[0]
                    if number.count(",") != 0:
                        comma_id = number.find(",")
                        if comma_id == 1:
                            print(1)
                            number1 = int(number.split(",")[0]) * 1000000
                            number2 = int(number.split(",")[1]) * 10000
                            full_number = number1 + number2
                        elif comma_id == 2:
                            print(2)
                            number1 = int(number.split(",")[0]) * 1000000
                            number2 = int(number.split(",")[1]) * 100000
                            full_number = number1 + number2

                    else:
                        full_number = int(number) * 1000
                else:
                    # Сотни/ десятки
                    print("сотни/ десятки")  # Comma
                    full_number = sub
                print(full_number)
                filtering_links()
            except:
                print("Pass")
        except:
            print(i)



def main():
    try:
        driver.get("https://www.youtube.com/results?search_query=fitness&sp=EgIQAg%253D%253D")
        driver.implicitly_wait(10)
        yes = driver.find_elements(By.CLASS_NAME, "style-scope.ytd-button-renderer.style-primary.size-default")
        yes[2].click()
        time.sleep(3)
        scraping_search_page()

    except Exception as ex:
        print(ex)
        driver.close()
    finally:
        driver.close()


if __name__ == '__main__':
    main()

