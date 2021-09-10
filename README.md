# TSDM-coin-farmer

天使动漫(tsdm39.net) 多账户自动签到+打工, 支持服务器部署或者锁屏运行

## 安装

1. 下载repo:

```bash
git clone https://github.com/Trojblue/TSDM-coin-farmer
cd TSDM-coin-farmer
pip install -r requirements.txt
```

2. [配置selenium driver](https://selenium-python.readthedocs.io/installation.html#drivers) (用于获取cookie, 服务器上只进行挂机任务不需要这步)

## 使用

1. `python farmer.py -r` 刷新所有账户的cookie

2. `python farmer.py -n` 立刻打工/签到并开始定时任务


```
usage: farmer.py [-h] [-s | -r] [-n]

optional arguments:
  -h, --help      show this help message and exit
  -s, --selenium  运行: 使用selenium模式(不填默认用post模式)
  -r, --reset     刷新cookie
  -n, --now       立刻运行打工和签到
```

## 高级使用
**天使动漫 多账户打工/签到:**

在`src`文件夹里`settings.py`, 按照以下格式填好需要的账号密码:

```python
TSDM_credentials = [['user1', 'pswd1'],
                    ['user2', 'pswd2']
                    ]
```

<br>

**S1论坛 自动刷在线时间:**

在`src`文件夹里`settings.py`,  把`enable_s1_read = False` 改成`True`





## 结构

- `farmer.py`: 主程序
- `actions.py`: cookie/工具类函数
- `v1_selenium.py`: selenium方式相关函数
- `v2_request.py`: post方式相关函数


- `settings.py`, `cookies.json`: 存储登录信息, ***请不要上传***


cookies.json:
```
{
"用户名1": [
        {cookie1},
        {cookie2},
        ....
      ],
      
"用户名2": [ ]
}

```


## 更新
2021.8.23: 增加stage1st的刷在线时间功能, 改一改可扩展成任意discuz论坛的刷在线时间功能

使用方法: 在`settings.py`增加变量`S1_CREDENTIALS`, 格式同tsdm

获取cookie后在farmer.py, `do_parse()`里取消关于s1的注释行

没打算做成正式功能所以不怎么正经

不确定是否能刷时间, 得过几天看小时有没有增加

## 其他

- 需要`urllib3==1.25.11`,
  因为[这个bug](https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname)

- `credentials.py`怕账户泄露也可以不用, 它只是登录的时候自动把账户密码填进输入框, 改一下代码自己手动填也一样

- selenium模式下可能会报各种warning, 能正常签到的话无视就好 

- 因为某些神必原因post模式打工有时候会工作失败, 建议手动重试一次, 或者用selenium





TODO:
1. 去掉文件依赖
2. 增加文件日志
3. 增加更多的except (稳定性)
4. 增加文件型设置
5. 合并所有cookies.json到同一个文件
6. s1随机页面阅读
