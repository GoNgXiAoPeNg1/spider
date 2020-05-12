# coding:utf-8
import os
import re
import urllib
import shutil
import requests
import itertools
import pdb

# ------------------------ Hyperparameter ------------------------
main_folder = 'D:\\tencent\\code\\mytest\\data'		# 存放图片的主目录
main_dir = 'today\\'					# 在主目录下设置子目录
"""
1. 如有多个关键字，需用空格进行分隔。
2. 每个关键字会单独存一个文件夹。
"""
keyword_lst = ['虐杀动物', '切肉 卖肉', '动物伤口']

# 设定保存后的图片格式
save_type = '.jpg'
# 每个关键字需要爬取的图片数量
max_num = 1200

# ------------------------ URL decoding ------------------------
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# ------------------------ Encoding ------------------------
def decode(url):
    for key, value in str_table.items():
        url = url.replace(key, value)
    return url.translate(char_table)

# ------------------------ Page scroll down ------------------------
def buildUrls(keyword):
    word = urllib.parse.quote(keyword)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=6))
    return urls

re_url = re.compile(r'"objURL":"(.*?)"')

# ------------------------ Get imgURL ------------------------
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

# ------------------------ Download imgs ------------------------
def downImgs(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
         
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == '4':
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print(e)
        return False
    with open(filename + save_type, 'wb') as f:
        f.write(res.content)

# ------------------------ Check save dir ------------------------
def mkDir(dst_dir):
    try:
        shutil.rmtree(dst_dir)
    except:
        pass
    os.makedirs(dst_dir)


# ------------------------ Pull Img ------------------------
def pull_img(cur_keyword, save_dir):

    print('\n\n', '= = ' * 10, ' keyword Spider 「{}」'.format(cur_keyword), ' = =' * 10, '\n\n')
    mkDir(save_dir)
     
    urls = buildUrls(cur_keyword)
    idx = 0
    for url in urls:
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        # Ending if no img
        if len(imgUrls) == 0:
            break
        for url in imgUrls:
            downImgs(url, save_dir, '{:>05d}'.format(idx + 1))
            print('  {:>05d}'.format(idx + 1))
            idx += 1
            if idx >= max_num:
                break
        if idx >= max_num:
            break
    print('\n\n', '= = ' * 10, ' Download ', idx, ' pic ', ' = =' * 10, '\n\n')



if __name__ == '__main__':
    
    for cur_keyword in keyword_lst:
        save_dir = main_folder + main_dir + cur_keyword
        pull_img(cur_keyword, save_dir)
 
