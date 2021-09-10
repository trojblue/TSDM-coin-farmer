# TSDM-coin-farmer

天使动漫(tsdm39.net) 多账户自动签到+打工, 支持服务器部署或者锁屏运行




## 部署

从clone到签到完成需要约10分钟

**下载repo:**

```bash
git clone https://github.com/Trojblue/TSDM-coin-farmer
cd TSDM-coin-farmer
pip3 install -r requirements.txt
```

**获取cookie:**

1. 在电脑上[配置selenium driver](https://selenium-python.readthedocs.io/installation.html#drivers) (填写验证码需要图形界面)
2. 在`/src`文件夹新建`settings.py`, 按照`/doc`文件夹里的例子进行修改 
3. `python farmer.py -r` 刷新所有账户的cookie

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

在`/src/settings.py`批量填好需要的账号密码, 刷新cookie后运行

```python
TSDM_CREDENTIALS = [["user1", "pswd1"], ["user2", "pswd2"]]
```

<br>

**S1论坛 自动刷在线时间:**

在`/src/settings.py`批量填好需要的账号密码
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

**手动填写cookie:**

例子见`/doc/cookies.json.example`

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

2021.9.11: 增加日志记录, 优化在服务器上使用的稳定性

<br>

## 其他

- 需要`urllib3==1.25.11`,
  因为[这个bug](https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname)

- `credentials.py`怕账户泄露也可以不用, 它只是登录的时候自动把账户密码填进输入框, 改一下代码自己手动填也一样

- selenium模式下可能会报各种warning, 能正常签到的话无视就好 

- 因为某些神必原因post模式打工有时候会工作失败, 建议手动重试一次, 或者用selenium

- 服务器上使用selenium模式打工, 需要先设置成headless模式: 在`/src/actions`中 `get_webdriver()`添加headless旗帜

- 没有条件在pc上获取cookie的话, 可以尝试手动配置: 见`doc/cookies.json.example`

## TODO
1. 增加云函数适配
2. 随机浏览s1页面
3. s1和eatASMR自动签到
