import random
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class Birthday:
    def __init__(self, client):
        self.client = client
        self.elements = {
            'select[title="Day:"]': random.randint(1, 27),
            'select[title="Month:"]': random.randint(1, 11),
            'select[title="Year:"]': random.randint(24, 35)
        }

    def fill_elements(self):
        for key, value in self.elements.items():
            select_element = self.client.driver.find_element("css selector", key)
            select = Select(select_element)
            time.sleep(random.randrange(2, 3))
            select.select_by_index(value)
            time.sleep(random.randrange(2, 3))

    def press_button(self):
        try:
            b = WebDriverWait(self.client.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//button[@type="button" and contains(text(), "Next")]'))
            )
            b.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False
        except Exception as e:
            raise Exception(f"[-] Birthday.press_button():  unknown exception : {e}")

    def final(self):
        return not self.press_button()

    def Birthday_Handler(self):
        try:
            self.start()
            self.fill_elements()
            for i in range(2):
                if self.press_button():
                    time.sleep(2)
                    break
                else:
                    continue
            if self.final():
                return True
            else:
                raise f"[-] ERROR: Birthday.birthday_handler():  button still shows after click two times"
        except Exception as e:
            pass

    def start(self):
        try:
            WebDriverWait(self.client.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//button[@type="button" and contains(text(), "Next")]'))
            )
            return True
        except (NoSuchElementException, TimeoutException):
            raise Exception("[-] ERROR: Birthday.start(): Cant find element. check the signup page ")
        except Exception as e:
            raise Exception(f"[-] Birthday.start():  unknown exception : {e}")

#
# def main():
#     ovpn_path = "nikto13-il1.vpnjantit-udp-2500.ovpn"
#     driver = get_driver()
#     cl = Client(driver, ovpn_path=ovpn_path)
#     em = EmailSignUp(cl)
#     em.EmailSignUp_Handler()
#
#     bd = Birthday(cl)
#     bd.Birthday_Handler()
#
#
# if __name__ == '__main__':
#     main()
