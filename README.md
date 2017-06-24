# CountMod10
在线信用卡校验工具（flask练手项目），使用Bootstrap+Flask+uwsgi部署

# 预览
![](https://ohrhuwrbc.qnssl.com/17-6-24/18650500.jpg)

# 部署
1. 启动uwsgi端
```bash
uwsgi -i config.ini
```
在启动完这条命令之后就会在/tmp 目录下生成一个uwsgi的管道文件

2. 配置Nginx转发请求
在Nginx的配置文件中加入
```
server {
    listen 8000;
    location / {
       include uwsgi_params;
       uwsgi_pass unix:/tmp/uwsgi.sock;
   }
}
```
重启nginx，访问http://ip:8000 即可
