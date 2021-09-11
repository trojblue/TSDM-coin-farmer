# TSDM-coin-farmer

天使动漫(tsdm39.net) 多账户自动签到+打工, 支持PC/Server/腾讯云函数

- 腾讯云函数版: 见 [这里](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/serverless_readme.md)

<br>


## 使用

从clone到签到完成需要约10分钟

**下载repo:**

```bash
git clone https://github.com/Trojblue/TSDM-coin-farmer
cd TSDM-coin-farmer
pip3 install -r requirements.txt
```

**打工/签到:**

1. 在电脑上[配置selenium driver](https://selenium-python.readthedocs.io/installation.html#drivers) (填写验证码需要图形界面)
2. `python farmer.py -r` 刷新cookie, 未配置`settings.py`时支持单个账户
3. `python farmer.py -n` 立刻打工/签到并开始定时任务

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

在`/src`文件夹新建`settings.py`, 按照`/doc`文件夹里的[例子](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/settings.py.example)进行修改, 刷新cookie后运行

```python
TSDM_CREDENTIALS = [["user1", "pswd1"], ["user2", "pswd2"]]
```

<br>

**S1论坛 自动刷在线时间:**

在`/src/settings.py`批量填好需要的账号密码, 修改`enable_s1_read`变量为`True`, 刷新cookie后运行
```python
S1_CREDENTIALS = [["user1", "pswd1"]] # 把变量S1_CREDENTIALS取消注释
enable_s1_read = True  # 把这行改成True
```

<br>

**服务器部署:**

1. 在电脑上获取cookie+测试, 确认可以运行
2. 在服务器上clone repo并安装所需库
3. 复制`cookies.json`和`settings.py`到服务器相同目录下
4. `python farmer.py -n` 立刻打工/签到并开始定时任务

<br>

**Selenium模式:**
- 用selenium模拟点击来签到/打工, 适用于post模式失效的情况 
- `python farmer.py -s -n`
- 也可以获取cookie后在设置headless参数, 来在无图形界面的服务器上运行↓
- 服务器上运行的话添加这两行到`actions.py → get_webdriver()`:
```python
options.add_argument('--headless')
options.add_argument('--disable-gpu')
```

<br>

**手动填写cookie:**

- 例子见[这里](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/cookies.json.example)

<br>


## 结构

- `farmer.py`: 主程序
- `actions.py`: cookie/工具类函数
- `v1_selenium.py`: selenium方式相关函数
- `v2_request.py`: post方式相关函数
- `dlc_xxx.py`: 各种额外功能
- `farmer.log`: 提issue的时候可以复制相关log帮助解决


- `settings.py`, `cookies.json`: 存储登录信息, ***请不要上传***


cookies.json:
```
{
"用户名1": [
        {cookie1},
        {cookie2},
        ....
      ],
"用户名2": [...]
}
```


## 更新
2021.8.23: 增加stage1st的刷在线时间功能, 改一改可扩展成任意discuz论坛的刷在线时间功能

使用方法见上, 没打算做成正式功能所以不怎么正经

<br>

2021.9.10: 增加日志记录, 优化在服务器上使用的稳定性

<br>

2021.9.11: 增加腾讯云函数支持

<br>

## 其他

- 需要`urllib3==1.25.11`,
  因为[这个bug](https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname)

- 服务器上使用selenium模式打工, 需要先设置成headless模式: 在`/src/actions`中 `get_webdriver()`添加headless旗帜

- 没有条件在pc上获取cookie的话, 可以尝试手动配置: 见`doc/cookies.json.example`

## TODO
2. 随机浏览s1页面
3. s1和eatASMR自动签到