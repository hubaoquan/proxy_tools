from util.webRequest import WebRequest
import requests
import re
import json
import time
csdnWebSite="https://blog.csdn.net/"
csdnUserName = "hubaoquanu"
# 只刷大于该Blog ID的Blog
MIN_BLOG_ID=105890062

# 下载首页，一般新发表的文章在首页 https://blog.csdn.net/hubaoquanu/
content = WebRequest().get(csdnWebSite+csdnUserName, timeout=10)
# 提取文章URL
articles = re.findall(csdnWebSite+csdnUserName+'/article/details/\d*', content.text)
articles = articles.__reversed__()
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'referer':'https://blog.csdn.net/hubaoquanu/'
}

proxy_server_json = WebRequest().get("https://hubaoquan.cn:5010/get_all/", timeout=10)

proxy_server_list_dict = json.loads((proxy_server_json.text))
proxy_server_list = []

for  proxy_server_dict in proxy_server_list_dict:
    proxy_server_list.append(dict(proxy_server_dict)['proxy'])

for articleUrl in articles:
    blogid = int(str(articleUrl).split("details/")[1])
    # 控制访问文章的区间，由于文章是按先后顺序发表，id也随之增长
    if blogid>MIN_BLOG_ID:
      print(articleUrl)
      for proxy_server in proxy_server_list:
          proxies={
              'http':proxy_server,
              'https':proxy_server
          }
          try:
            result = requests.head(url=articleUrl,headers=header,proxies=proxies,timeout=3)
            print(result)
          except:
            print("error : "+proxy_server)
            # 报错说明该代理服务器不能使用，移除该服务器
            # requests.head(url="https://hubaoquan.cn:5010/delete?proxy="+proxy_server,headers=header)
            # proxy_server_list.remove(proxy_server)
          else:
           time.sleep(0.1)
