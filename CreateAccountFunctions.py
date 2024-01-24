import time
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)


def generate_new_fake_mail(proxy: dict = None):
    url = 'https://email-fake.com'
    for i in range(3):
        try:
            req = requests.get(url, proxies=proxy, verify=False, timeout=15)
            soup = BeautifulSoup(req.content, "html.parser")
            mail = soup.find_all("span", {"id": "email_ch_text"})
            print(f"[+] INFO: found mail: {url}/{mail[0].text}")
            return mail[0].text
        except (requests.RequestException, TimeoutError) as e:
            print(f"[-] ERROR: Request error: CreateAccountFunctions().generate_new_fake_mail(). maybe timeout:  {e}")
            time.sleep(4)
            continue
        except OSError as e:
            print(f"[-] ERROR CreateAccountFunctions().generate_new_fake_mail(). : {e}")
            time.sleep(4)
            continue
    return None


if __name__ == '__main__':
    generate_new_fake_mail()
