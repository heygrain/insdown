# InsDown
download Instagram pics/videos

## 代理配置
- 打开proxy.json（可以用记事本打开）
- 如果不需要代理直接将use_proxy改为false
- 需要代理，use_proxy保持true，然后根据自己的vpn修改：
```
   protocol即协议（选填socks5，http，https）
   address即本地代理ip
   port即本地代理端口
```

## 设置完代理就可以使用了
- 假设需要下载https://www.instagram.com/p/B5t_eQCjus5/
- 打开cmd，输入命令：
```
   cd "InsDown.exe所在的目录"
   InsDown --code="B5t_eQCjus5" [--retry=3 --path="./save" --proxy="proxy.json"]
```
- 以上命令方括号[]里的可以全部不敲，但有需要可以添加：
```
   retry是指连接或者下载失败时的重试次数，如果vpn不稳定可以设置稍大一些
   path是指下载文件的保存路径
   proxy是指代理设置文件json所在位置，一般不用改，修改代理设置直接在proxy.json里面修改就可以
```
