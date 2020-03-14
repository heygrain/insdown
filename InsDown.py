import re
import requests
import os
import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(description='InsDown by Grain.\nUsage:\n \
                                     python InsDown.py --code="B4zhlcljUPA" --path="./save"  \
                                     --proxy=proxy.json --retry=3')
    parser.add_argument("--code", default=None,
                        help="code of the Instagram post.")
    parser.add_argument("--path", default='./save',
                        help="Path where you save your downloads.")
    parser.add_argument("--proxy", default='proxy.json',
                        help="Proxy setting. You need to configurate proxy.json.")
    parser.add_argument("--retry", type=int, default=3, 
                        help="Number of retries when connection or downloading fails.")
    return parser.parse_args()


def terminate():
    print("Terminated.")
    os._exit(0)


if __name__ == "__main__":

    args = parse_args()
    n = args.retry + 1

    # set proxy
    print("Setting proxy...")
    try:
        with open(args.proxy) as f:
            proxy = json.load(f)
        if proxy['use_proxy']:
            proxy_str = "{}://{}:{}".format(proxy['protocol'],
                                            proxy['address'],
                                            proxy['port'])
            proxy = {
                "http": proxy_str,
                "https": proxy_str
            }
        else:
            proxy = None
    except:
        proxy = None

    # acquire source address
    if not args.code:
        print("Please input the code of the instagram post you want to download.")
        terminate()
    print('Acquiring picture / video address...')
    code = args.code
    url = "https://www.instagram.com/p/{}/".format(code)
    for i in range(n):
        try:
            res = requests.get(url, proxies=proxy)
            break
        except:
            if i == n - 1:
                print("All attempts to connect to Instagram have failed.\nCheck your network and proxy settings.")
                terminate()
            print("Connection to Instagram failed, retrying...")
    pic_re = r'"display_url":"(.*?)"'
    vid_re = r'"video_url":"(.*?)"'
    res_url = re.findall(vid_re, res.text)
    res_url += re.findall(pic_re, res.text)
    res_url = list(set(res_url))
    res_url = [tmp.encode('utf-8').decode('unicode_escape') for tmp in res_url]
    del res

    # set download path
    file_path = args.path
    # 是否有这个路径
    if not os.path.exists(file_path):
        # 创建路径
        os.makedirs(file_path)

    # download and write file
    k = len(res_url)
    failed = []
    for j in range(k):
        res_u = res_url[j]
        print("Start to download ({}/{})...".format(j + 1, k))
        suf = r'.*[.](.*?)[?]'
        suffix = re.findall(suf, res_u)[0]
        if suffix == 'mp4':
            print("It's a video and it may take some time...")
        for i in range(n):
            try:
                r = requests.get(res_u, proxies=proxy, stream=True)
                break
            except:
                if i == n - 1:
                    print("All attempts to download the resource ({}/{}) have failed.".format(j + 1, k))
                    print("You may try open the url {} with a browser to download it.".format(res_u))
                    failed.append(j)
                else:
                    print("Fail to download, retrying ({}/{})...".format(j + 1, k))
        print("Just need a few moments...")
        # 拼接图片名（包含路径）
        pathname = '{}{}{}({}).{}'.format(file_path, os.sep, code, j + 1, suffix)
        with open(pathname, 'wb') as f:
            f.write(r.content)
        del r
        print("Download complete. \nFind it here: {}".format(pathname))
    print("All done. {} out of {} succeeded.".format(k - len(failed), k))
    if len(failed):
        print("\nFor failed ones, you can copy their links and try to download them using a browser.")
        print("The links of the failed ones:")
        for item in failed:
            print(res_url[item])
        print()
    terminate()
