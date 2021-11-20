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
        break

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
            oneline = line.strip().split(';')
            username = oneline[0]
            password = oneline[1]
            url = oneline[2].split('|')[0].strip()
            resultOne = scrapOnePage(url, username, password)
            print(resultOne)
            result.append(resultOne)
        output_file.writelines(result)
        output_file.close()
        input_file.close()
    except:
        print("Unknown format file")

def scrapOnePage(url, username, password):
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
                time.sleep(2)
                # //*[@id="wpbody-content"]/div[5]/ul/li[1]/a/span
                driver.get(url + "/edit.php?post_type=shop_order")
                time.sleep(2)
                orderEl = driver.find_element(By.XPATH, '//*[@id="wpbody-content"]/div[5]/ul/li[1]/a/span')
                if orderEl != None:
                    nOrders = orderEl.text.replace('(', '').replace(')', '')
                    driver.close()
                    return username + ";" + password + ";" + url + " | Orders: " + nOrders + "\n"
                driver.close()
                return username + ";" + password + ";" + url + " | No orders page\n"
            else:
                return username + ";" + password + ";" + url + " | Invalid credential\n"
        else:
            return username + ";" + password + ";" + url + "| can not reach login page\n"
    except:
        return username + ";" + password + ";" + url + " | can not reach the site\n"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
