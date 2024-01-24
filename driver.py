import random
from seleniumwire import webdriver


def request_interceptor(requests):
    # change useragent for each packet
    if "instagram" in requests.url:
        new_headers = {}

        if "User-Agent" in requests.headers:
            del requests.headers["User-Agent"]
            new_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            new_headers['User-Agent'] = f"{new_user_agent}"

        if "sec-ch-ua" in requests.headers:
            del requests.headers["sec-ch-ua"]
            new_sec_ch_ua = '"Chromium";v="108", "Google Chrome";v="108", "Not=A?Brand";v="99"'
            new_headers['sec-ch-ua'] = f"{new_sec_ch_ua}"

        if 'sec-ch-ua-platform' in requests.headers:
            del requests.headers["sec-ch-ua-platform"]

            new_sec_ch_ua_platform = 'win10'
            new_headers['sec-ch-ua-platform'] = f"{new_sec_ch_ua_platform}"

        if 'sec-ch-ua-full-version-list' in requests.headers:
            del requests.headers["sec-ch-ua-full-version-list"]
            new_sec_ch_ua_full_version = '"Chromium";v="108.0.0.0", "Google Chrome";v="108.0.0.0", "Not=A?Brand";v="99.0.0.0"'
            new_headers['sec-ch-ua-full-version-list'] = f"{new_sec_ch_ua_full_version}"

        # Manually update the SeleniumWire headers
        for key, value in new_headers.items():
            requests.headers[key] = value


def get_driver(proxy):

    # Selenium WebDriver proxy settings
    if not proxy:
        seleniumwire_options = {}
    else:
        print(f"[+] INFO: Setting Proxy: Done.")
        seleniumwire_options = {
            'proxy': proxy,
            # 'connection_timeout': 60,  # Disable connection timeout
            'verify_ssl': False  #
        }
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    # Chrome options for Selenium WebDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-webrtc")
    chrome_options.add_argument("--use-mock-location")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-error")
    chrome_options.add_argument(f"--window-size={random.randint(800, 1400)},{random.randint(600, 1000)}")


    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options,seleniumwire_options=seleniumwire_options)
    driver.request_interceptor = request_interceptor
    driver.delete_all_cookies()
    driver.execute_script(
        "Object.defineProperty(navigator, 'userAgent', {value: arguments[0], configurable: true});",
        user_agent
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print("[+] INFO: Generating fake User-Agent: ",driver.execute_script("return navigator.userAgent;"))

    return driver
