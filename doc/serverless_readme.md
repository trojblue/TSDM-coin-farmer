# 云函数版使用:

部署需要约20分钟

<br>

首先获取`cookies.json`: 

- 账户多推荐设置好`settings.py`后在电脑上执行`python farmer.py -r`, 见主页readme
- 账户少可以在浏览器里获取`s_gkr8_xxx_auth` 和`s_gkr8_xxx_saltkey` 后手动填入`/doc/cookies.json.example`例子里

<br>

然后在腾讯云新建一个函数服务: [这里](https://console.cloud.tencent.com/scf/list)

1. 选择"**自定义创建**" → 依次选择: **事件函数, 代码部署, python3.6, 在线编辑**
2. 复制`SCF_sign.py` ([这里](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/dist/SCF_sign.py)) 的内容到底下编辑器里的`index.py`中 
3. 复制`cookies.json`到云函数同目录
4. 高级配置不用动
5. 触发器配置: **默认流量, 定时触发, 自定义触发周期, 无附加信息, 立即启用**
   1. 签到触发周期: `5 9 * * *` (每天9点05分)

<br>

**截图:**

![](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/scf_1.png?raw=true)

![](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/scf_2.png?raw=true)

<br>

<br>

回到[函数服务页](https://console.cloud.tencent.com/scf/list), 复制刚才创建好的函数服务, 再用`SCF_work.py`([这里](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/dist/SCF_work.py)) 的内容替换`index.py`原有代码

触发器配置: 其他不变, **修改触发周期**: 

- 打工触发周期: ` 5 2,9,16 * * *` 
- 每天3次, 2点9点16点; 受限于腾讯云的cron设置不支持每6小时5分钟运行一次, 只能这样了

![](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/scf_3.png?raw=true)

<br>

配置完成, 运行情况可以在腾讯云 函数管理 - "日志查询"一栏看到

