# TSDM-coin-farmer

天使动漫(tsdm39.net) 多账户自动签到+打工, 支持服务器部署或者锁屏运行


## 结构
- `farmer.py`: 主程序
- `actions.py`: 签到/打工相关函数
- `cookie.py`: cookie相关函数
- `v2_request.py`: post方式相关函数
- `credentials.py`, `cookies.json`: 存储登录信息, ***请不要上传***

credentials.py的结构: 用一个变量存储账户密码
```python
TSDM_credentials = [ ['user1', 'pswd1'],
                     ['user2', 'pswd2']
                    ]
```


## 使用

1. 在`src`文件夹新建`credentials.py`, 按照上面的格式填好需要的账号密码
2. `python farmer.py -r` 刷新所有账户的cookie
3. 再次运行: `python farmer.py`开始定时任务, 在6小时后开始第一轮打工

如果需要立刻打工/签到,可以使用`-n`参数

### 可选参数
```bash
usage: farmer.py [-h] [-s | -r] [-n]

optional arguments:
  -h, --help      show this help message and exit
  -s, --selenium  运行: 使用selenium模式(默认使用POST)
  -r, --reset     运行: 刷新cookie
  -n, --now       立刻运行打工和签到
```



## 其他
- request版本需要`urllib3==1.25.11`, 因为[这个bug](https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname)

- `credentials.py`怕账户泄露也可以不用, 它只是登录的时候自动把账户密码填进输入框, 改一下代码自己手动填也一样)

- selenium模式下可能会报各种错, 能正常签到的话无视就好 
