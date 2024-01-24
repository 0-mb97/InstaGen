from CreateAccountFunctions import generate_new_fake_mail
import GenerateAcount as account
import OpenVPNManager
from OpenVPNManager import OpenVPNManager
from driver import get_driver


class Client:
    def __init__(self, proxy: str = None, ovpn_path=None, passwd=None):

        self.fill_register_login_dict = {}
        self.proxy = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
            'no_proxy': 'localhost,127.0.0.1',
        } if proxy else None
        self.ovpn = OpenVPNManager(config_path=ovpn_path, password=passwd) if ovpn_path else None
        self.info = {
            "conf": {
                "ovpn_active": False

            },
            "login": {
                "emailOrPhone": None,
                "fullName": None,
                "username": None,
                "password": None,
            },
            "verify_code": ["", ""]
        }
        self.driver = get_driver(self.proxy)
        self.generate_user_login()

    def generate_user_login(self):
        self.set_mail()
        self.set_username()
        self.set_password()
        self.set_fullName()

    def set_username(self):
        self.info["login"]["username"] = account.username()

    def set_mail(self):
        value = generate_new_fake_mail(self.proxy)
        if value:
            self.info["login"]["emailOrPhone"] = value
        else:
            raise Exception("[-] ERROR: CreateAccountFunctions().generate_new_fake_mail() response with None")

    def get_mail(self):
        return self.info["login"]["emailOrPhone"]

    def set_fullName(self):
        self.info["login"]["fullName"] = account.generatingName()

    def set_password(self):
        self.info["login"]["password"] = account.generatePassword()

    def set_by_key(self, key):
        if "username" in key:
            self.set_username()
            return "username"
        elif "mail" in key:
            self.set_mail()
            return "emailOrPhone"
        else:
            print("[-] Error: Client.set_by_key(): Unknown key : {key}")
            raise Exception("[-] Error: Client.set_by_key(): Unknown key : {key}")

    def start_ovpn(self):
        if self.ovpn:
            self.ovpn.start()
            self.info["conf"]["ovpn_active"] = True

    def stop_ovpn(self):
        if self.ovpn:
            if self.info["conf"]["ovpn_active"]:
                self.ovpn.stop()
                self.info["conf"]["ovpn_active"] = False

    def print_register_login(self):
        return f"{self.fill_register_login_dict['username']}:{self.fill_register_login_dict['password']}:{self.fill_register_login_dict['fullName']}:{self.fill_register_login_dict['emailOrPhone'][0]}"
