# TSDM-coin-farmer

![](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/farmer2.png)

天使动漫(tsdm39.net) 多账户自动签到+打工, 支持PC/Server/腾讯云函数

新增s1刷在线时间支持

<br>


## 使用

1. **腾讯云函数版**: 见 [这里](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/serverless_readme.md), 相比本地运行更稳定, *比较推荐*

<br>

2. **本地** (服务器/电脑/安卓手机): 见[这里](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/server_readme.md)

<br>

## 结构

- `farmer.py`: 主程序
- `actions.py`: cookie/工具类函数
- `dlc_xxx.py`: 各种额外功能
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

2022.2.10: 增加eatASMR的自动签到 (本地&云函数)DLC

2021.12.1: 增加s1刷阅读的云函数版本

<br>

2021.9.10: 增加日志记录, 优化在服务器上使用的稳定性
2021.9.11: 增加腾讯云函数支持

<br>

2021.8.23: 增加stage1st的刷在线时间功能, 改一改可扩展成任意discuz论坛的刷在线时间功能

<br>

## 其他

- 需要`urllib3==1.25.11`,
  因为[这个bug](https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname)

- 服务器上使用selenium模式打工, 需要先设置成headless模式: 在`/src/actions`中 `get_webdriver()`添加headless旗帜

- 没有条件在pc上获取cookie的话, 可以尝试手动配置: 见`doc/cookies.json.example`

## TODO
2. 随机浏览s1页面
3. s1和eatASMR自动签到