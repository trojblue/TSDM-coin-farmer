# TSDM-coin-farmer

天使动漫(tsdm39.net) 多账户自动签到+打工, 支持服务器部署或者锁屏运行




## 部署

下载repo:

```bash
git clone https://github.com/Trojblue/TSDM-coin-farmer
cd TSDM-coin-farmer
pip install -r requirements.txt
```

**获取cookie:**

- 在电脑上 [配置selenium driver](https://selenium-python.readthedocs.io/installation.html#drivers) (如果之前没配置过的话)
- `python farmer.py -r` 刷新所有账户的cookie
  - 这步需要填写验证码, 所以服务器上做不了

**部署:**

- `python farmer.py -n` 立刻打工/签到并开始定时任务


```
usage: farmer.py [-h] [-s | -r] [-n]

optional arguments:
  -h, --help      show this help message and exit
  -s, --selenium  运行: 使用selenium模式(不填默认用post模式)
  -r, --reset     刷新cookie
  -n, --now       立刻运行打工和签到
```

<br>

### 高级使用

**多账户打工/签到:**

在`src`文件夹里`settings.py`, 填好需要的账号密码:

```python
TSDM_CREDENTIALS = [['user1', 'pswd1'],
                    ['user2', 'pswd2']] # 把变量TSDM_CREDENTIALS取消注释
```

<br>

**S1论坛 自动刷在线时间:**

在`src`文件夹里`settings.py`, 填好需要的账号密码:
```python
S1_CREDENTIALS = [["user1", "pswd1"]] # 把变量S1_CREDENTIALS取消注释

enable_s1_read = True  # 把这行改成True
```

<br>

**服务器部署:**

1. 在电脑上获取cookie+测试, 确认可以运行
2. 在服务器上clone repo并安装所需库
3. 复制`cookies.json`和`settings.py`到服务器同目录下
4. `python farmer.py -n` 立刻打工/签到并开始定时任务

<br>


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
6. s1随机页面阅读
