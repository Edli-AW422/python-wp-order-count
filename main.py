# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def main():
    # read csv file
    result = []
    input_path = "./input.txt"
    output_path = "./output.txt"
    input_file = open(input_path, 'r')
    output_file = open(output_path, 'w')
    output_file.writelines([])
    op = Options()
    op.headless = True
    driver = webdriver.Chrome("./chromedriver.exe", options=op)

    for line in input_file:
        print line
        oneline = line.strip().split(';')
        username = oneline[0]
        password = oneline[1]
        url = oneline[2].split('|')[0].strip()
        resultOne = scrapOnePage(driver, url, username, password)
        print resultOne
        result.append(resultOne)
    output_file.writelines(result)
    output_file.close()
    input_file.close()

def scrapOnePage(driver, url, username, password):
    print "scrapOnePage", url, username, password
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
                print "no password input"
                return username + ";" + password + ";" + url + " | Invalid credential\n"
        else:
            print "no login page"
            return username + ";" + password + ";" + url + "| can not reach login page\n"
    except:
        return username + ";" + password + ";" + url + " | unexpected error\n"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
