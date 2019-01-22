import os
import re
from concurrent.futures import ThreadPoolExecutor

import requests

host_url = 'https://www.pearvideo.com/popular_loading.jsp?reqType=1&start={start}'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}


def get_index(start_number):
    res = requests.get(host_url.format(start=start_number), headers=headers)
    return res.text


def parser_index(text):
    res = re.findall('<a href="(.*?)" class="actplay">', text)
    res = ['https://www.pearvideo.com/' + i for i in res]
    print(res)
    return res


def get_detail(html_text):
    # 获得视频的下载地址
    if re.search(r'srcUrl="(.*?\.mp4)"', html_text):
        download_index = re.search(r'srcUrl="(.*?\.mp4)"', html_text).group(1)

        # 获取标题
        title = re.search('<h1 class="video-tt">(.*?)</h1>', html_text).group(1)

        dic = {
            'download_index': download_index,
            'title': title
        }
        print('成功链接到[%s]视频文件' % title)
        return dic
    else:
        download_index = re.search(r'srcUrl="(.*?\.m3u8)"', html_text).group(1)

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
    if not os.path.exists('down_popular_videos'):
        os.mkdir('down_popular_videos')
    file_path = os.path.join('down_popular_videos', title) + '.mp4'
    with open(file_path, 'wb') as f:
        f.write(video_bytes)
    print(file_path + '下载成功!')


if __name__ == '__main__':
    pool = ThreadPoolExecutor(10)
    for i in range(10):
        text = get_index(i*10)
        url_list = parser_index(text)
        for url in url_list:
            response = requests.get(url, headers=headers).text
            content_dic = get_detail(response)
            # get_video(content_dic['download_index'],content_dic['title'])
            # 开启多线程快速的爬取数据
            pool.submit(get_video, content_dic['download_index'], content_dic['title'])
    # text = get_index(0)
    # url_list = parser_index(text)
    # for url in url_list:
    #     response = requests.get(url, headers=headers).text
    #     print(url)
    #     content_dic = get_detail(response)
    #     # get_video(content_dic['download_index'],content_dic['title'])
    #     # 开启多线程快速的爬取数据
    #     pool.submit(get_video, content_dic['download_index'], content_dic['title'])
