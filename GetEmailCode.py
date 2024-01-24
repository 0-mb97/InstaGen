import time

import requests
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, TimeoutException
import Client


def extract_code_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    subj_divs = soup.find_all('div', class_='fem subj_div_45g45gg')
    time_divs = soup.find_all('div', class_='fem time_div_45g45gg')
    last_time = None
    if subj_divs:
        # Extract the text content of the last element
        last_subject = subj_divs[0].text.strip()

        # Extract the number from the subject (assuming it's always at the beginning)
        last_number = ''.join(c for c in last_subject if c.isdigit())
        # print("Last number: ", last_number)
        if time_divs:
            last_time = time_divs[0].text.strip()
        # print(f"last number: {last_number} : last_time : {last_time}")
        print(f"[+] INFO: Verification Code : {last_number}")
        return last_number, last_time
    else:
        print("[+] INFO: GetEmailCode.extract_code_from_html(): Element not found in HTML. Retrying..")
        return None


class GetEmailCode:
    def __init__(self, client: Client):
        self.last_code = None
        self.client = client
        self.varify_mail = self.get_modify_mail()
        self.request = {
            "url": 'https://email-fake.com/',
            "headers": self.get_header(),
            "proxy": self.client.proxy
        }
        self.last_response = None

    def get_modify_mail(self):
        mail, domain = self.client.get_mail().split("@")
        return f'{domain}%2F{mail}'

    def update_code(self):
        self.client.info["verify_code"] = self.last_code

    def get_code_from_fake_email(self):
        ovpn = False
        for i in range(3):
            time.sleep(5)
            if not self.send_request():
                print("start ovpn and decrese the loop by one")
                self.client.start_ovpn()
                ovpn = True
                i -= 1
                continue
            if not self.handle_request():
                continue
            self.update_code()
            if ovpn:
                self.client.stop_ovpn()
            return True
        return False

    def resend_code(self):
        try:
            element_to_click = self.client.driver.find_element("xpath", '//div[text()="Resend code."]')

            element_to_click.click()
            return True
        except (NoSuchElementException, TimeoutException) as e:
            print(f"[-] GetEmailCode.resend_code(): {e}")
            raise Exception

    def send_request(self):
        if self.client.info["conf"]["ovpn_active"]:
            print(f"proxy is on, the value of self.client.info[conf][ovpn_active] is : {self.client.info['conf']['ovpn_active']}")
            proxy = None
        else:
            proxy = self.request["proxy"]
        for i in range(5):
            try:
                self.last_response = requests.get(url=self.request["url"], headers=self.request["headers"],
                                                  proxies=proxy, verify=False, timeout=30)
                return True
            except (requests.RequestException, TimeoutError) as e:
                print(f"Request error: etEmailRequest().send(). maybe timeout:  {e}")
                time.sleep(8)
                continue
            except OSError as e:
                print(f"[-] ERROR GetEmailRequest().send_request() : {e}")
                time.sleep(8)
                continue
        return False

    def is_code_new(self):
        return self.last_code[1] != self.client.info["verify_code"][1]

    def handle_request(self):
        status = self.last_response.status_code
        if status == 200:
            # return value is tuple[code][date]
            self.last_code = extract_code_from_html(self.last_response.text)
            if self.last_code:
                return self.is_code_new()
            else:
                return False
        elif status == 500:
            return False
        else:
            print(f"Request failed with status code {status}.")
            raise Exception(f"[-] GetEmailCode.handle_request(): Unknown status code: {status}")

    def get_header(self):
        return {
            'Host': 'email-fake.com',
            'User-Agent': self.client.driver.execute_script('return navigator.userAgent;'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            "Cookie": f"surl={self.varify_mail}",
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': "no-cache",
            'Cache-Control': 'no-cache'
        }

    def GetEmailCode_Handler(self):
        for i in range(2):
            for j in range(3):
                res = self.get_code_from_fake_email()
                if res:
                    return True
            self.resend_code()
            continue

#
# def main():
#     ovpn_path = "nikto13-il1.vpnjantit-udp-2500.ovpn"
#     mitm = "127.0.0.1:8082"
#     proxy = {
#         'http': f'http://{mitm}',
#         'https': f'http://{mitm}',
#         'no_proxy': 'localhost,127.0.0.1'  # excludes
#     }
#     driver = get_driver()
#     cl = Client.Client(driver, ovpn_path=ovpn_path, proxy=proxy)
#     em = EmailSignUp(cl)
#     em.EmailSignUp_Handler()
#
#     bd = Birthday(cl)
#     bd.Birthday_Handler()
#
#     ge = GetEmailCode(cl)
#     ge.GetEmailCode_Handler()
#
#
# if __name__ == '__main__':
#     main()
