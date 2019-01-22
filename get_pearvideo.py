import os
import re
from concurrent.futures import ThreadPoolExecutor

import requests

host_url = 'https://www.pearvideo.com/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}


def get_index():
    res = requests.get(host_url, headers=headers)
    return res.text


def parser_index(text):
    res = re.findall('<a href="(.*?)" class="vervideo-lilink actplay">', text)
    res = [host_url + i for i in res]

    return res


def get_detail(html_text):
    # 获得视频的下载地址
    download_index = re.search(r'srcUrl="(.*?\.mp4)"', html_text).group(1)

    # 获取标题
    title = re.search('<h1 class="video-tt">(.*?)</h1>', html_text).group(1)

    dic = {
        'download_index': download_index,
        'title': title
    }
    print('成功链接到[%s]视频文件' % title)
    return dic


def get_video(video_url, title):
    video_bytes = requests.get(video_url).content
    if not os.path.exists('down_pearvideos'):
        os.mkdir('down_pearvideos')
    file_path = os.path.join('down_pearvideos', title) + '.mp4'
    with open(file_path, 'wb') as f:
        f.write(video_bytes)
    print(file_path + '下载成功!')


if __name__ == '__main__':
    pool = ThreadPoolExecutor(10)
    text = get_index()
    url_list = parser_index(text)
    for url in url_list:
        response = requests.get(url, headers=headers).text
        content_dic = get_detail(response)
        # get_video(content_dic['download_index'],content_dic['title'])
        # 开启多线程快速的爬取数据
        pool.submit(get_video, content_dic['download_index'], content_dic['title'])
