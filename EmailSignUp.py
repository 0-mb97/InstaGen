import json
import random
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Client import Client


class EmailSignUp:

    def __init__(self, client: Client):
        self.client = client
        self.driver = client.driver

        self.errors = {"press_again": False,
                       "change_username": False,
                       "start_ovpn": False,
                       "start_activate": False
                       }

        # self.buttons = {
        #     "register_button": 'button[type="submit"]'
        # }

    def press_submit(self):
        try:

            time.sleep(random.uniform(1, 2))
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            button.click()
            return True

        except Exception as e:
            raise Exception(f"[-] EmailSignUp.press_submit():  unknown exception : {e}")

    def fill_element(self, key):

        value = self.client.info["login"][key]
        el = self.driver.find_element("name", key)
        if el.get_attribute("value"):
            el.send_keys(Keys.CONTROL + "a")
            el.send_keys(Keys.DELETE)

        el.send_keys(value)
        time.sleep(random.uniform(4, 6))

    def fill_all_form(self):
        for key, value in self.client.info["login"].items():
            self.fill_element(key)

    def start_error_handler(self):

        is_activate = self.errors["start_activate"]
        try:
            error_div = self.driver.find_element(By.CLASS_NAME, 'error-code')
            if "429" in error_div.text:
                if is_activate:
                    raise Exception("signup page not load. after start vpn")
                else:
                    self.client.start_ovpn()
                    self.errors["start_activate"] = True
                    return False
            else:
                print(f"signup page not load. error_code {error_div}")
                raise Exception("signup page not load. after start vpn")
        except Exception as e:
            if "facebook" in self.driver.current_url:
                # need to create rotate function in order to change the ip address
                raise Exception("[-] ERROR: facebook in url")
            if "phone" in self.driver.current_url:
                return False
            else:
                raise Exception(f"[-] EmailSignUp.start():  unknown exception : {e}")

    def start(self):
        try:
            time.sleep(1)
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_a9--"))
            )

            # Click the button using Action Chains
            ActionChains(self.driver).move_to_element(button).click().perform()

        except (TimeoutException, NoSuchElementException):
            pass
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
            return True
        except (NoSuchElementException, TimeoutException):
            return self.start_error_handler()
        except Exception as e:
            raise Exception(f"[-] EmailSignUp.start():  unknown exception : {e}")

    def is_finish(self):
        try:
            time.sleep(2)
            # WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            # print("button is clickable")
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
            return False
        except (NoSuchElementException, TimeoutException):
            return True
        except Exception as e:
            raise Exception(f"[-] EmailSignUp.start():  unknown exception : {e}")

    def check_for_ssl_error(self):
        try:
            error_message = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "ssfErrorAlert")))
            time.sleep(random.randrange(1, 2))
            return error_message

        except (NoSuchElementException, TimeoutException):
            return True
        except Exception as e:
            raise Exception(f"[-] EmailSignUp.check_for_ssl_error():  unknown exception : {e}")

    def error_handler(self):
        press_again = self.errors["press_again"]
        change_username = self.errors["change_username"]
        start_ovpn = self.errors["start_ovpn"]

        try:
            if not press_again:
                print("Trying to press again")
                self.errors["press_again"] = True
                return True

            res = self.check_for_ssl_error()
            if res is True:
                if not change_username:
                    print("Trying to change username")
                    self.client.set_username()
                    self.fill_element("username")
                    self.errors["change_username"] = True
                    return True
                elif not start_ovpn:
                    print("Trying to start vpn")
                    self.client.start_ovpn()
                    self.errors["start_ovpn"] = True
                    return True
                else:
                    print(f"[-] EmailSignUp.error_handler():  unknown exception")
                    raise Exception(f"[-] EmailSignUp.error_handler():  unknown exception")

            else:
                print(f"[!] Warning: EmailSignUp.error_handler():ssl_error_message : {res.text}\nDon\'t worry, I will "
                      f"fix it.")
                key = self.client.set_by_key(res.text.lower())
                self.fill_element(key)
                return True
        except Exception as e:
            raise Exception(f"[-] EmailSignUp.error_Handler():  unknown exception : {e}")

    def EmailSignUp_Handler(self):
        max_tries = 3
        try:
            for i in range(2):
                self.driver.get("https://www.instagram.com/accounts/emailsignup/")
                if not self.start():
                    continue
                self.fill_all_form()
                for i in range(max_tries):
                    try:
                        if not self.press_submit():
                            continue
                        if self.is_finish():
                            print("Your Credential: in case the account will be activate, i will save it to "
                                  "account.txt file")
                            print(json.dumps(self.client.info["login"], indent=2))
                            return True
                        else:
                            self.error_handler()
                            continue
                    except Exception as e:
                        raise Exception(f"[-] EmailSignUp.Handler():  unknown exception : {e}")
        except WebDriverException as e:
            print(f"[-] ERROR: Check the connection or mitm? . exception: {e}")
            raise
        except Exception as e:
            raise Exception(f"[-] ERROR: driver.get_driver():  unknown exception : {e}")
        finally:
            self.client.stop_ovpn()
