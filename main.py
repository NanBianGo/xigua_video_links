import base64
import json
import re
import os
import requests

headers = {
    "cookie": "贴入自己西瓜视频的Cookie",
    "Referer": "https://www.ixigua.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.75 Safari/537.36"
}


def downloadFile(url, name):
    print(f'开始下载: {name}')
    resp = requests.get(url, headers=headers)
    if not os.path.exists('movie'):
        os.mkdir('movie')
    with open(f'movie/{name}', mode='wb') as f:
        f.write(resp.content)
    print(f'完成下载: {name}')


def printVideoInfo(title, videoUrl, audioUrl):
    print("=============================================")
    print("视频标题:", title)
    print("视频地址:", videoUrl)
    print("音频地址:", audioUrl)
    print("=============================================")


def main(url):
    resp = requests.get(url=url, headers=headers)
    resp.encoding = 'utf-8'
    if resp.status_code == 200:
        res_html = resp.text
        if 'pseries_more_v2' not in url:
            json_str = re.findall('window._SSR_HYDRATED_DATA=(.*?)</script>', res_html)[0]
            json_str = json_str.replace('undefined', 'null')
            json_data = json.loads(json_str)
            video_url = \
                json_data['anyVideo']['gidInformation']['packerData']['video']['videoResource']['dash'][
                    'dynamic_video'][
                    'dynamic_video_list'][-1]['main_url']
            audio_url = \
                json_data['anyVideo']['gidInformation']['packerData']['video']['videoResource']['dash'][
                    'dynamic_video'][
                    'dynamic_audio_list'][-1]['main_url']
            title = json_data['anyVideo']['gidInformation']['packerData']['video']['title']
            title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title).replace(" ", "")
            video_url = base64.b64decode(video_url).decode()
            audio_url = base64.b64decode(audio_url).decode()
            printVideoInfo(title, video_url, audio_url)
        else:
            json_data = json.loads(res_html)
            for item in json_data['data']:
                title = item['title']
                # backup_url_1
                video_url = item['preloadVideoResource']['dynamic_video']['dynamic_video_list'][-1][
                    'backup_url_1']
                audio_url = item['preloadVideoResource']['dynamic_video']['dynamic_audio_list'][-1][
                    'backup_url_1']
                video_url = base64.b64decode(video_url).decode()
                audio_url = base64.b64decode(audio_url).decode()
                title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title).replace(" ", "")
                printVideoInfo(title, video_url, audio_url)
                # downloadAll(video_url, audio_url, title)


if __name__ == '__main__':
    while True:
        try:
            inContent = input("输入：")
            if inContent == "exit":
                os.close(0)
            else:
                print("解析视频内容中...")
                main(inContent)
        except (RuntimeError, RuntimeWarning) as err:
            print("异常：", err)
            continue
