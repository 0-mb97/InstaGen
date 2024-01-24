import json
import random
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from SetEmailCode import *


class AccountCreateAjax(SetEmailCode):

    def __init__(self, client: Client):
        super().__init__(client)
        self.buttons = {"save_info_popup": EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), 'Not now')]")),
                        "allow_notification_popup": EC.element_to_be_clickable(
                            (By.XPATH, f"//*[contains(text(), 'Not Now')]")),
                        }
        self.errors = {
            "press_again": False,
            "suspended": False,
            "is_created": False,
            "print_error": False,
            "resend_code": False
        }

    def is_clickable(self, button):
        try:
            print("[?] INFO: Check if notification popup is on")
            element = WebDriverWait(self.driver, 2).until(self.buttons[button])
            element.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False
        except Exception as e:
            print(f"[-]Error: Account.CreateAjax.is_clickable(): error: {e}")

    def extract_error(self):
        xpath_expression_base = '//span[contains(@class, "x1lliihq") and contains(@class, "x1plvlek") and contains(@class, "xryxfnj") and contains(@class, "x1n2onr6") and contains(@class, "x193iq5w") and contains(@class, "xeuugli") and contains(@class, "x1fj9vlw") and contains(@class, "x13faqbe") and contains(@class, "x1vvkbs") and contains(@class, "x1s928wv") and contains(@class, "xhkezso") and contains(@class, "x1gmr53x") and contains(@class, "x1cpjm7i") and contains(@class, "x1fgarty") and contains(@class, "x1943h6x") and contains(@class, "x1i0vuye") and contains(@class, "xvs91rp") and contains(@class, "xo1l8bm") and contains(@class, "xkmlbd1") and contains(@class, "x2b8uid") and contains(@class, "x1tu3fi") and contains(@class, "x3x7a5m") and contains(@class, "x10wh9bi") and contains(@class, "x1wdrske") and contains(@class, "x8viiok") and contains(@class, "x18hxmgj")][@dir="auto"]'
        try:
            span_element = self.driver.find_element(By.XPATH, xpath_expression_base)
            print("[!] Warning : ", span_element.text)
        except (NoSuchElementException, TimeoutException):
            print("[-] No error in page")
        except Exception as e:
            print(f"[-] SetEmail.extract_error():  unknown exception : {e}")

    def save_to_file(self, file=None):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(file, "a") as f:
                f.write(json.dumps(f'{self.client.info["login"]} | {formatted_datetime}'))
                f.write("\n")
            if "accounts" in file:
                print("[+] Saving Credential to file")
        except Exception as e:
            print(f"[-] ERROR in AccountCreatedAjax.save_to_file(): {e}")
        return True

    def error_handler(self):
        try:
            for i in range(2):
                try:
                    if self.is_suspended():
                        print("[-] ERROR: Account Suspended")
                        return False
                    if self.is_clickable("save_info_popup"):

                        return True
                    self.extract_error()
                    if self.is_username_in_url():
                        print("[+] INFO: Avatar Successfully Created. Done.")
                        print("[+] INFO: Credentials saved into account.txt")
                        return True
                    if "not found" in self.driver.title.lower():
                        print("[-] ERROR: Account Suspended")
                        return False
                    else:
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    self.resend_code()
                    print("sending code again")
                    self.send_code_again()
                    continue
                except Exception as e:
                    print(f"[-] ERROR : AccountCreatedAjax.error_handler : {e} ")

        except Exception as e:
            print(f"[-] ERROR : AccountCreatedAjax.error_handler . first try: {e} ")

    def client_handler(self):
        try:
            self.GetEmailCode_Handler()
            print("[+] INFO: Getting Verification Code from https://email-fake.com: Done.")
            time.sleep(random.randint(8, 15))
            self.SetEmailCode_Handler()
            print("[+] INFO: Setting Verification Code from https://email-fake.com: Done.")
            if self.error_handler():
                print("[+] INFO: Avatar Successfully Created. Done.")
                print("[+] INFO: Credentials saved into account.txt")
                self.save_to_file("account.txt")
            else:
                print("[-] ERROR: Avatar account created but got suspended.")
                print("[-] ERROR: Try to run again with proxy or OpenVpn file(.ovpn). See You Again.")
        except Exception as e:
            print(e)
        finally:
            self.driver.quit()

    def is_suspended(self):
        print("[?] INFO: check if client suspended by url")
        if "suspended" in self.driver.current_url:
            return True

    def is_username_in_url(self):
        print("[?] Check if username_in_url")
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(f"https://www.instagram.com/{self.client.info['login']['username']}")
        time.sleep(2)
        if self.client.info['login']['fullName'] in self.driver.title:
            return True
        return False

    def send_code_again(self):
        print("resend the code")
        self.resend_code()
        self.get_code_from_fake_email()
        self.fill_element()


