import argparse
import os
import requests
import json
import sys

def set_args():
    parser = argparse.ArgumentParser(
                    description="Send request to index files")
    parser.add_argument('-u', '--url', help='URL to index files', required=True)
    parser.add_argument('-d', '--dir', help='directory in S3 bucket that is to be indexed', required=True)
    parser.add_argument('-es', '--esversion', help='Elastic search version to index', required=True)
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
    dir = args.dir
    esversion = args.esversion
    headers = args.headers
    full_url = os.path.join(url, dir, esversion)
    response = send_request(full_url, headers)
    if not(response.ok):
        print(response.text)
        sys.exit(1)
    elif response.ok:
        sys.exit(0)


if __name__ == "__main__":
    main()

