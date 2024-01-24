from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from GetEmailCode import *


class SetEmailCode(GetEmailCode):

    def __init__(self, client: Client):
        super().__init__(client)
        self.client = client
        self.driver = self.client.driver

    def get_code(self):
        return self.client.info["verify_code"][0]

    def fill_element(self):
        try:
            el = self.driver.find_element("name", 'email_confirmation_code')
            if el.get_attribute("value"):
                el.send_keys(Keys.CONTROL + "a")
                time.sleep(0.5)
                el.send_keys(Keys.DELETE)
            time.sleep(2)
            el.send_keys(self.get_code())
            time.sleep(2)
            el.send_keys(Keys.ENTER)
            return True

        except (NoSuchElementException, TimeoutException) as e:
            print(f"[-] SetEmailCode.fill_element(): Element Already Filled? ")

    def SetEmailCode_Handler(self):
        try:
            self.fill_element()
            self.final()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"[-]Error: Account.CreateAjax.handle(): error: {e}")
        except Exception as e:
            print(f"[-]Error: Account.CreateAjax.handler(): error: {e}")

    def final(self):
        try:
            xpath_expression = '//div[@role="button" and @tabindex="-1" and @aria-disabled="true"]'
            element = self.driver.find_element(By.XPATH, xpath_expression)
            while True:
                # Get the tabindex attribute
                tabindex = element.get_attribute('tabindex')

                # Check if the tabindex is -1
                if tabindex is not None and int(tabindex) == -1:
                    time.sleep(6)
                    continue
                else:
                    return True
        except (NoSuchElementException, TimeoutException) as e:
            return True
        except Exception as e:
            print(f"[-] Error: SetEmailCode.final(): error: {e}")
