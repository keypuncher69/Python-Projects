from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
from datetime import date

todaydate = date.today()

findate = str(todaydate.day) + "/" + str(todaydate.month) + "/" + str(todaydate.year)

speed = []

def startcount():
    driver = webdriver.Chrome(executable_path="D:\Documents\AutoIt\chromedriver.exe")

    driver.get("https://www.10fastfingers.com")
    driver.maximize_window()

    driver.find_element_by_id("typing-test").click()

    time.sleep(3)
    driver.find_element_by_id("CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection").click()
    time.sleep(1)
    driver.find_element_by_id("inputfield").click()

    while len(speed) < 4:
        wait = WebDriverWait(driver, 90)
        wait.until(expected_conditions.presence_of_element_located((By.ID, "wpm")))
        speed.append(int((driver.find_element_by_id("wpm").text)[:3]))
        driver.refresh()
        time.sleep(2)

def getspeed():
    return speed

def getdate():
    return findate
