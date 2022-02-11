## S1刷阅读:

1. 在电脑上用selenium获取cookie (或者手动填), 执行`dlc_stage1st.py`里的相关函数; 获得`cookie.json`

2. 复制`/dist/SCF_s1.py`到腾讯云函数, 用类似的办法部署;
3. 复制`cookie.json`到云函数相同目录下
4. 部署, 设置触发周期

办法和tsdm云函数部署的类似, 可以参考 [这里](https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/serverless_readme.md); 触发周期按照需要自己调整, 我设置的是半小时一次; 建议改掉`s1_sample_post`变量来自定义反复刷新的页面, 也可以自己写个List随机访问, 我这里是固定访问同一个网页





## EatASMR:

部署办法同上, 用`dlc_eatasmr.py`登录后获取cookie, 再部署到云函数, 或者自己看相关文件写成本地运行

不同组件(tsdm, s1, eatasmr)的cookie可以放在同一个`cookies.json`文件里, 但目前不同站之间不能有相同的用户名. 否则要单独各自建一个文件, 不然会覆写掉相同用户名的cookie记录.

或者获取完一个用户名的cookie后把`cookies.json`里的用户名改成不重复的项目; 直接改在云函数版里没关系, 但本地selenium运行会出错.

