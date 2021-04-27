from util.webRequest import WebRequest
import re
csdnWebSite="https://blog.csdn.net/"
csdnUserName = "hubaoquanu"

content = WebRequest().get(csdnWebSite+csdnUserName, timeout=10)
# https://blog.csdn.net/hubaoquanu/article/details/68490596
articles = re.findall(csdnWebSite+csdnUserName+'/article/details/\d*', content.text)
print(articles)