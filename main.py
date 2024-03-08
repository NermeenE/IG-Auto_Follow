from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv('.env')
USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")

FOLLOWERS_ACCT = "couponingwithnicole_"


chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

class IgFollower():
  def __init__(self):
    self.driver = webdriver.Chrome(options=chrome_options)
    self.driver.get("https://www.instagram.com/accounts/login/")
    self.driver.maximize_window()
    sleep(3)
  
  def login(self):
    username = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    username.send_keys(USERNAME)
    password = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
    password.send_keys(PASSWORD, Keys.ENTER)
    sleep(3.5)

    # Save-login info prompt: off
    save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
    if save_login_prompt:
        save_login_prompt.click()
    sleep(3.5)

    turn_off_notifications = self.driver.find_element(By.XPATH,'/html/body')
    turn_off_notifications.send_keys(Keys.TAB + Keys.TAB + Keys.ENTER)

  def locate_followers(self):
    sleep(4.5)
    self.driver.get(f"https://www.instagram.com/{FOLLOWERS_ACCT}/followers")
    sleep(4)

    #wait until path is present
    f_body = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_aano']")))

    # Scroll through followers 
    for i in range(3):
      try:
          f_body = self.driver.find_element(By.XPATH, "//div[@class='_aano']")
          self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", f_body)
          sleep(4)
      except StaleElementReferenceException:
          print("StaleElementReferenceException: Element is no longer attached to the DOM.")

  def follow(self):
     all_follow_btns = self.driver.find_elements(By.CSS_SELECTOR,"._aano button")

     followers_followed = 0

     for btn in all_follow_btns:
        try:
           btn.click()
           sleep(1.3)
           
           followers_followed += 1

           if followers_followed >= 15:
               print(f"{followers_followed} followed")
               break
        except ElementClickInterceptedException:
           cancel_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
           cancel_btn.click()


ig_bot = IgFollower()
ig_bot.login()
ig_bot.locate_followers()
ig_bot.follow()
ig_bot.driver.quit()
