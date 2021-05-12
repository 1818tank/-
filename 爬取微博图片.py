import requests
import re
from urllib import request
import os

#构造请求头
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',

}

user_id = input('请输入要爬取的微博用户id:')
container_id = f'107603{user_id}'


#定义一个函数，获取博主的名字
def Get_username(user_id):
    res = requests.get(url = f'https://m.weibo.cn/api/container/getIndex?uid={int(user_id)}&containerid={int(container_id)}',headers = headers)
    data = res.text
    return re.findall("screen_name:(.*?)",data)  

#定义一个函数，根据第一个json请求的url得到初始since_id参数
def Get_first_since_id():
    res = requests.get(url = f'https://m.weibo.cn/api/container/getIndex?uid={int(user_id)}&containerid={int(container_id)}',headers = headers)
    data = res.text
    return re.findall('since_id":(.*?)}',data)
    

#定义一个函数，根据一个since_id的到下一个since_id
def Get_next_since_id(since_id):
    next_url = f'https://m.weibo.cn/api/container/getIndex?uid={user_id}&containerid={container_id}&since_id={int(since_id[0])}'
    res = requests.get(url = next_url,headers = headers)
    data = res.text
    return re.findall('since_id":(.*?)}',data)

   
#定义一个函数，根据一个since_id，获取一个页面中的图片链接
def Get_pic_link_list(since_id):
    url = f'https://m.weibo.cn/api/container/getIndex?uid={user_id}&containerid={container_id}&since_id={int(since_id[0])}'
    print(url)
    res = requests.get(url = url,headers = headers)
    data = res.text
    pic_link_list = re.findall('"size":"large","url":"(.*?)",',data)
    return pic_link_list

#定义一个函数，下载一个链接列表中所有的链接对应的图片
def Download_pic(link_list,pic_path):
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
    for link in link_list:
        request.urlretrieve(link,pic_path + f"/{link.split('/')[-1]}") 

#更正链接列表中字符的函数
def correct_str(link_list):
    i = 0
    for link in link_list:
        link_list[i] = re.sub('\\\/\\\/','//',link)
        link_list[i] = re.sub('\\\/','/',link)
        i = i + 1


#主函数
mb_name = input('请输入博主名字：')
SINCE_ID = Get_first_since_id()
print(SINCE_ID)
i = 1
while not (SINCE_ID == []):
    LINK_LIST = Get_pic_link_list(SINCE_ID)
    SINCE_ID = Get_next_since_id(SINCE_ID)
    correct_str(LINK_LIST)
    print(LINK_LIST)
    print(f'正在下载第{i}页图片...')
    Download_pic(LINK_LIST,f'F:/{mb_name}')
    print(f'第{i}页图片下载完成！')
    i = i + 1
print('======================================================================================')
print('下载任务完成!')











