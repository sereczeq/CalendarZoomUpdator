from typing import List

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Mail_Finder:

    def __init__(self, path, login, password):
        self.PATH = path
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        print("opening website...")
        self.driver = webdriver.Chrome(self.PATH, chrome_options=options)
        self.login = login
        self.password = password
        self.login_to_website()

    def login_to_website(self):
        self.driver.get(
                "https://s.student.pwr.edu.pl/iwc_static/c11n/login_student_pwr_edu_pl.html?lang=pl&3.0.1.3"
                ".0_16070546&svcs=abs,mail,calendar,c11n")
        self.driver.find_element_by_id("username").send_keys(self.login)
        self.driver.find_element_by_id("password").send_keys(self.password)
        self.driver.find_element_by_id("signin_label").click()
        print("logged in...")

    def click_on_mail(self, index):
        try:
            xpath = "/html/body/div[1]/div[2]/div[6]/div[3]/div/div[3]/div/div[3]/div[1]/div/table/tbody/tr[" + str(
                    index) + "]"
            element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))

            element.click()
        except (StaleElementReferenceException, TimeoutException):
            print("[ERROR] could not click on index:", index)
            # self.driver.quit()

    def switch_to_mail_frame(self):
        self.driver.switch_to.frame(self.driver.find_element_by_id("iwc_widget_mail_IframeMessagePane_0_iframe"))

    def switch_to_main_frame(self):
        self.driver.switch_to.default_content()

    def read_mail(self):
        element = WebDriverWait(self.driver, 20).until(
                ec.element_to_be_clickable((By.XPATH,
                                            "html/body/div[1]/div[1]")))
        children = element.find_elements_by_css_selector("*")

        mail_text = ""
        for child in children:
            string = child.text
            if len(string) > 10:
                mail_text += string
        return mail_text

    def read_mails(self, how_many):
        mails: List[str] = []
        self.click_on_mail(2)
        for i in range(2, how_many):
            print("reading mail number:", i)
            self.switch_to_mail_frame()
            try:
                mails.append(self.read_mail())
            except TimeoutException:
                print("[ERROR] mail could not be loaded:", i)
                self.switch_to_main_frame()
                self.click_on_mail(2)
            self.switch_to_main_frame()
            ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
        print("read all", how_many, "mails")
        return mails
