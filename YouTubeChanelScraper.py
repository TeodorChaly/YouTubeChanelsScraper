from random import randint
import undetected_chromedriver as uc
from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


PATH = "C:\WEBDRIVER\chromedriver.exe"
option = webdriver.ChromeOptions()
#option.headless = True
option.add_argument("user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17")
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_experimental_option("useAutomationExtension", False)
option.add_argument('disable-infobars')
option.add_experimental_option("excludeSwitches",["enable-automation"])
driver = webdriver.Chrome(PATH,chrome_options = option)


def filtering_links(min_follower, max_follower, number):
    if number >= min_follower and  number <= max_follower:
        return True

def scraping_search_page(min_f = 10000000, max_f= 0):
    count = 1
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        if count == 15:
            break
        count += 1

    epr = driver.find_elements(By.ID, "content-section")
    list_of_channels = []
    for i in epr:

        try:
            try:
                print(i.find_element(By.ID, "main-link").get_attribute("href"))
                full_number = 0
                sub = i.find_element(By.ID, "subscribers").text.split("подпи")[0]
                if "тыс" in i.find_element(By.ID, "subscribers").text.split("подпи")[0]:
                    # Тысячи
                    number = sub.split("тыс")[0]
                    if number.count(",") != 0:
                        comma_id = number.find(",")
                        if comma_id == 1:
                            number1 = int(number.split(",")[0]) * 1000
                            number2 = int(number.split(",")[1]) * 10
                            full_number = number1 + number2
                        elif comma_id == 2:
                            number1 = int(number.split(",")[0]) * 1000
                            number2 = int(number.split(",")[1]) * 100
                            full_number = number1 + number2
                    else:
                        full_number = int(number) * 1000
                elif "млн" in i.find_element(By.ID, "subscribers").text.split("подпи")[0]:
                    # Миллионы
                    number = sub.split("млн")[0]
                    if number.count(",") != 0:
                        comma_id = number.find(",")
                        if comma_id == 1:
                            number1 = int(number.split(",")[0]) * 1000000
                            number2 = int(number.split(",")[1]) * 10000
                            full_number = number1 + number2
                        elif comma_id == 2:
                            number1 = int(number.split(",")[0]) * 1000000
                            number2 = int(number.split(",")[1]) * 100000
                            full_number = number1 + number2

                    else:
                        full_number = int(number) * 1000
                else:
                    # Сотни/ десятки
                    full_number = sub
                status = filtering_links(min_f, max_f,full_number )
                if status:
                    list_of_channels.append(i.find_element(By.ID, "main-link").get_attribute("href"))
            except:
                print("Pass")
        except:
            print(i)
    return list_of_channels

def channel_crawler(list_of_channels):
    channel_info_list = []
    for channel in list_of_channels:
        time.sleep(randint(2,5))
        driver.get(channel+"/about")
        full_list= channel_scraping()
        if full_list != 0:
            channel_info_list.append(full_list)
            with open("results.txt", "a", encoding="utf-8")as file:
                file.write(str(full_list)+"\n")
                file.flush()
            print(channel_info_list)

def channel_scraping():
    try:
        name_of_channel = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/ytd-channel-name/div/div/yt-formatted-string").text
    except:
        name_of_channel = "No name"

    try:
        country_of_channel = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[1]/div[4]/table/tbody/tr[2]/td[2]/yt-formatted-string").text
    except:
        country_of_channel= "No country"

    try:
        email = driver.find_element(By.XPATH, '//*[@id="details-container"]/table/tbody/tr[1]/td[2]/yt-formatted-string/a').text
    except:
        email = "No Email"
    # if email == "No Email":
    #     try:
    #         description = driver.find_element(By.ID, "description-container").text
    #         if "gmail.com" in description:
    #             email = description
    #     except:
    #         email = "No Email"
    if email == "войдите в аккаунт":
        email = "Chanel have email"
    else:
        email = "Chanel doesn't have email"

    socials = driver.find_elements(By.CLASS_NAME, "yt-simple-endpoint.style-scope.ytd-channel-about-metadata-renderer")
    channel_dict = {}
    channel_dict[name_of_channel] = {"Country": country_of_channel, "Email":email, "Link":driver.current_url}
    for social in socials:
        channel_dict[social.text] = social.get_attribute("href")
    if email == "Chanel doesn't have email" or email == "No Email":
        return 0
    else:
        return channel_dict





def main():
    try:
        driver.get("https://www.youtube.com/results?search_query=fitness&sp=EgIQAg%253D%253D")
        driver.implicitly_wait(10)
        yes = driver.find_elements(By.CLASS_NAME, "style-scope.ytd-button-renderer.style-primary.size-default")
        yes[2].click()
        time.sleep(3)

        list_of_channels = scraping_search_page(1000, 200000)
        channel_crawler(list_of_channels)



    except Exception as ex:
        print(ex)
        driver.close()
    finally:
        driver.close()


if __name__ == '__main__':
    main()

