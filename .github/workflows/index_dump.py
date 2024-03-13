import argparse
import os
import requests
import json
import sys

def set_args():
    parser = argparse.ArgumentParser(
                    description="Send request to index data dump")
    parser.add_argument('-u', '--url', help='URL to index dump file', required=True)
    parser.add_argument('-f', '--file', help='name of dump file to be indexed', required=True)
    parser.add_argument('-e', '--dataenv', help='data env to retrieve dump file from', required=True)
    parser.add_argument('-he', '--headers', help='key:value json string; headers to authenticate request', required=True, type=json.loads)
    args = parser.parse_args()
    return args

def send_request(url, headers):
    try:
        response = requests.get(url,headers=headers)
    except requests.exceptions.RequestException as e:
        raise e
    return response

def main():
    args = set_args()
    url = args.url
    filename = args.file
    dataenv = args.dataenv
    headers = args.headers
    full_url = os.path.join(url, filename, dataenv)
    print(full_url)
    response = send_request(full_url, headers)
    if not(response.ok):
        print(response.text)
        sys.exit(1)
    elif response.ok:
        print(response.text)
        sys.exit(0)


if __name__ == "__main__":
    main()

