import argparse
from EmailSignUp import *
from Birthday import Birthday
from AccountCreateAjax import AccountCreateAjax


def User_Preference():
    parser = argparse.ArgumentParser(description="InstaGen: Automated Avatar Creation for Instagram")
    parser.add_argument("-ov","--ovpn_path", default=None,type=str, help="Full Path to the OpenVPN file")
    parser.add_argument("-r","--root_passwd",default=None ,type=str, help="If you use ovpn, you need to enter root passwd")
    parser.add_argument("-p","--proxy", default=None,type=str, help="Proxy address and port (e.g., 127.0.0.1:8082) in case of authenticate proxy enter the pattern User:Paswwd@Host:Port")
    # Add more arguments as needed
    args = parser.parse_args()
    if args.ovpn_path and not args.root_passwd:
        print("[-] ERROR: Ovpn must run as root, You Need to enter root password")
        raise Exception
    else:
        run(ovpn_path=args.ovpn_path,root_passwd=args.root_passwd,proxy=args.proxy)


def run(ovpn_path, proxy, root_passwd):
    try:
        cl = Client(ovpn_path=ovpn_path, passwd=root_passwd, proxy=proxy)
        print("[+] INFO: Generating Avatar Credential. Done.")
        em = EmailSignUp(cl)
        em.EmailSignUp_Handler()
        print("[+] INFO: Checking Avatar Credential. Done.")
        time.sleep(random.randint(8,15))
        bd = Birthday(cl)
        bd.Birthday_Handler()
        print("[+] INFO: Setting random Avatar Birthday. Done.")
        time.sleep(random.randint(8,15))
        ac = AccountCreateAjax(cl)
        print("[+] INFO: Getting Verification Code from https://email-fake.com: Done.")
        ac.client_handler()
    except WebDriverException:
        return
    except Exception as e:
        print(f"runtime error: {e}")


if __name__ == '__main__':
    User_Preference()
