"""
  This is used to test automated end to end using browser
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver import Edge
from msedge.selenium_tools import (
  Edge,
  EdgeOptions
)
from selenium.webdriver.support.ui import Select
import time

class EndToEndTesting(StaticLiveServerTestCase):
  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.baseUrl = "http://127.0.0.1:3000"
    options = EdgeOptions()
    options.use_chromium = True
    cls.browser = Edge(options=options, executable_path="C:\\different_users\\Tombra\\Python\\Python Projects\\web\\Selenium\\msedgedriver.exe")
    cls.browser.implicitly_wait(10)
    # set the values to use for login
    cls.category = "ADMIN"
    cls.email = "tombra4ril@gmail.com"
    cls.password = "tombra4ril"

  @classmethod
  def tearDownClass(cls):
    cls.selenium.quit()
    super().tearDownClass()

  def test_login(self):
    self.browser.get(f"{self.baseUrl}")
    # get elements
    category = self.browser.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/form/div[2]/select')
    email = self.browser.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/form/div[3]/input')
    password = self.browser.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/form/div[4]/input')
    login = self.browser.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/form/div[5]/input')
    # enter inputs
    category = Select(category)
    category.select_by_visible_text("ADMIN")
    time.sleep(0.5)
    email.clear()
    for _ in self.email:
      email.send_keys(_)
      time.sleep(0.1)
    time.sleep(0.5)
    password.clear()
    for _ in self.password:
      password.send_keys(_)
      time.sleep(0.1)
    time.sleep(0.5)
    login.click()

    # quit testing
    time.sleep(10)
    self.browser.quit()