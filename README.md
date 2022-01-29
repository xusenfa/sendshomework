# 2022我的运维寒假学习  



## 学习⽬标

1. 学习python基本语法
2. 学习python⾯向对象编程
3. 学习flask框架
4. 使⽤python爬取华⼤新闻第⼀⻚所有新闻的标题与链接（即要求对爬取到的数据进⾏处理）
5. 使⽤flask将爬取的结果展⽰到⾃⼰的站点上并对新闻数据实时更新

## 具体要求

1. python语法是基础要求熟练使⽤
2. 爬⾍不限制过滤html的⼯具和⽅式,可以使⽤beautifulsoup库也可以使⽤正则,亦或是其他⼯具
3. 使⽤git对项⽬进⾏管理,并添加README.md和.gitignore文件
4. 使⽤nginx反向代理flask⾄{IP或域名}/hdxw
6. 使⽤nginx配置{IP或域名}/为静态显⽰这是华⼤新闻的站点
    具体表现为使⽤静态映射⼀个index.html文件,并且可以超链接⾄新闻数据⻚,同时本⽬录下应包含⼀个
    相同内容的index.md,并配置该文件不可访问

### 0.准备

这里使用DigitalOcean的Centos 7系统

先安装好必需的软件

```shell
yum -y update
yum -y install git
curl -fsSL https://get.docker.com | bash -s docker
systemctl enable docker.service && init 6
```

### 1.获取所需文件

由于本项目所有文件都存储在github上，所以先克隆项目到本地

首先上传私钥id_rsa到/root/.ssh

然后设置私钥权限

```shell
chmod 600 /root/.ssh/id_rsa
```

配置git

```shell
git config --global user.name "MoeSakura"
git config --global user.email q211798501@hotmail.com
```

克隆存储库

```
cd / && git clone git@github.com:xusenfa/sendshomework.git
```



### 2.部署

本次项目所有服务均可在同一容器上部署，故使用Dockerfile自建镜像

```shell
cd /sendshomework
先手动上传SSL证书至/root/sendshomework/nginx/certificates
mkdir /sendshomework/nginx/logs #手动创建网站日志目录
docker build . -t spider-flask-nginx:1.0
docker run -itd --network host -v /sendshomework:/sendshomework --name sendshomework --restart unless-stopped spider-flask-nginx:1.0
```

部署完成！可打开 https://sendshomework.moesakura.cc 查看效果

### 3.总结

  由于DigitalOcean的Centos 7 系统的系统防火墙默认关闭，转而使用网页设定防火墙规则，所以本次就不需要开放端口。

  要求中所有目标都已经完成，其中对数据实时更新是用crontab定时任务每5分钟爬取一次华大新闻页面。
