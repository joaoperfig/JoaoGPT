# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Main Function
if __name__ == '__main__':


    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #Change chrome driver path accordingly
    chrome_driver = "C:/chromedriver/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    print (driver.title)


    time.sleep(60)
    driver.close()
    driver.quit()
