# xwd-cms
我的CMS。使用Django框架。

项目——mysite。

应用 | 说明
---|---
tinysite | 微站，网站的核心

# 环境
python 3.6.5

## 创建并切换python虚拟开发环境

    pip3 install virtualenv
    virtualenv dev
    . ./dev/bin/activate

> 执行 deactivate 退出python虚拟环境

## 安装项目依赖的python包

    pip3 install -r requirements.txt


# 源码工程创建过程

## 创建项目
- 进入项目存放目录——mysite
- 创建项目mysite

        django-admin startproject mysite


## 创建应用
- 进入manage.py文件所在目录——mysite

        python manage.py startapp tinysite

编写应用。


# [使用uWSGI和nginx来设置Django和你的web服务器](http://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/tutorials/Django_and_nginx.html)

## 关于域名和端口
在这个教程中，我们将假设你的域名为 example.com 。用你自己的FQDN或者IP地址来代替。

从头到尾，我们将使用8000端口作为web服务器的公开端口，就像Django runserver默认的那样。当然，你可以使用任何你想要的端口，但是我已经选了这个，因此，它不会与web服务器可能已经选择的任何端口冲突。

## 安装uwsgi
### 安装uwsgi到你的virtualenv中

    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple uwsgi

记住，你将需要安装Python开发包。对于Debian，或者Debian衍生系统，例如Ubuntu，你需要安装的是 pythonX.Y-dev ，其中，X.Y是你Python的版本。

### 测试
创建test.py文件，写入内容：

    # test.py
    def application(env, start_response):
        start_response('200 OK', [('Content-Type','text/html')])
        return [b"Hello World"] # python3
        #return ["Hello World"] # python2

部署它到HTTP端口8000

    uwsgi --http :8000 --wsgi-file test.py

选项表示:
- http :8000: 使用http协议，端口8000
- wsgi-file test.py: 加载指定的文件，test.py

访问 http://example.com:8000 ，看到页面返回 "Hello World"，说明服务正常。


### 测试你的Django项目
确保你的Django项目实际上正常工作：

    python3 manage.py runserver 0.0.0.0:8000

而如果正常，则使用uWSGI来运行它:

    uwsgi --http :8000 --module mysite.wsgi

- module mysite.wsgi: 加载指定的wsgi模块


## 安装Nginx

ubuntu:

    sudo apt-get install nginx
    sudo /etc/init.d/nginx start    # start nginx

centos:

    yum install epel-release
    yum install nginx
    systemctl start nginx

现在，通过在一个web浏览器上通过端口80访问它，来检查nginx是否正常。
正常的话，可以看到nginx的相关信息页面。


## 为你的站点配置nginx
你会需要 uwsgi_params 文件，可用在uWSGI发行版本的 nginx 目录下，或者从 https://github.com/nginx/nginx/blob/master/conf/uwsgi_params 找到。

将其拷贝到你的项目目录中。一会儿，我们将告诉nginx引用它。

现在，创建一个名为mysite_nginx.conf的文件，然后将这个写入到它里面:

    # mysite_nginx.conf

    # the upstream component nginx needs to connect to
    upstream django {
        # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
        server 127.0.0.1:8001; # for a web port socket (we'll use this first)
    }

    # configuration of the server
    server {
        # the port your site will be served on
        listen      8000;
        # the domain name it will serve for
        server_name .example.com; # substitute your machine's IP address or FQDN
        charset     utf-8;

        # max upload size
        client_max_body_size 75M;   # adjust to taste

        # Django media
        location /media  {
            alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
        }

        location /static {
            alias /path/to/your/mysite/static; # your Django project's static files - amend as required
        }

        # Finally, send all non-media requests to the Django server.
        location / {
            uwsgi_pass  django;
            include     /path/to/your/mysite/uwsgi_params; # the uwsgi_params file you installed
        }
    }

这个配置文件告诉nginx提供来自文件系统的媒体和静态文件，以及处理那些需要Django干预的请求。对于一个大型部署，让一台服务器处理静态/媒体文件，让另一台处理Django应用，被认为是一种很好的做法，但是现在，这样就好了。

将这个文件链接到/etc/nginx/sites-enabled，这样nginx就可以看到它了:

ubuntu:

    sudo ln -s ~/path/to/your/mysite/mysite_nginx.conf /etc/nginx/sites-enabled/

centos:

    sudo ln -s ~/path/to/your/mysite/mysite_nginx.conf /etc/nginx/conf.d/



## 部署静态文件
在运行nginx之前，你必须收集所有的Django静态文件到静态文件夹里。首先，必须编辑mysite/settings.py，添加:

    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

然后运行

    python3 manage.py collectstatic


## 调整setting.py到生产环境状态

    调整 DEBUG=False

> 默认情况下，DEBUG参数为True，便于开发调试，在生产环境中要调整为False，避免泄露重要信息。


## 基本的nginx测试
重启nginx:

    ubuntu: sudo /etc/init.d/nginx restart
    centos: systemctl restart nginx

> 这里注意关闭selinux

要检查是否正确的提供了媒体文件服务，添加一个名为 media.png 的图像到 /path/to/your/project/project/media directory 中，然后访问http://example.com:8000/media/media.png - 如果这能正常工作，那么至少你知道nginx正在正确的提供文件服务。


## nginx和uWSGI以及test.py
让nginx对 test.py 应用说句”hello world”吧。

    uwsgi --socket :8001 --wsgi-file test.py

这几乎与之前相同，除了这次有一个选项不同：
- socket :8001: 使用uwsgi协议，端口为8001

同时，已经配置了nginx在那个端口与uWSGI通信，而对外使用8000端口。访问:

    http://example.com:8000


## 使用Unix socket而不是端口
目前，我们使用了一个TCP端口socket，因为它简单些，但事实上，使用Unix socket会比端口更好 - 开销更少。

编辑 mysite_nginx.conf, 修改它以匹配:

    server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    # server 127.0.0.1:8001; # for a web port socket (we'll use this first)

然后重启nginx.

再次运行uWSGI:

    uwsgi --socket mysite.sock --wsgi-file test.py

这次， socket 选项告诉uWSGI使用哪个文件。

在浏览器中尝试访问http://example.com:8000/。

### 如果那不行
检查nginx错误日志(/var/log/nginx/error.log)。如果你看到像这样的信息:

    connect() to unix:///path/to/your/mysite/mysite.sock failed (13: Permission denied)

那么可能你需要管理这个socket上的权限，从而允许nginx使用它。

尝试(有效):

    uwsgi --socket mysite.sock --wsgi-file test.py --chmod-socket=666 # (very permissive)

或者(664权限不够，还是会报错):

    uwsgi --socket mysite.sock --wsgi-file test.py --chmod-socket=664 # (more sensible)

你可能还必须添加你的用户到nginx的组 (可能是 www-data)，反之亦然，这样，nginx可以正确地读取或写入你的socket。

值得保留nginx日志的输出在终端窗口中滚动，这样，在解决问题的时候，你就可以容易的参考它们了。


## 使用uwsgi和nginx运行Django应用
运行我们的Django应用：

    uwsgi --socket mysite.sock --module mysite.wsgi --chmod-socket=664

现在，uWSGI和nginx应该不仅仅可以为一个”Hello World”模块服务，还可以为你的Django项目服务。



## 配置uWSGI以允许.ini文件
我们可以将用在uWSGI上的相同的选项放到一个文件中，然后告诉 uWSGI使用该文件运行。这使得管理配置更容易。

创建一个名为 `mysite_uwsgi.ini` 的文件:

    # mysite_uwsgi.ini file
    [uwsgi]

    # Django-related settings
    # the base directory (full path)
    chdir           = /path/to/your/project
    # Django's wsgi file
    module          = project.wsgi
    # the virtualenv (full path)
    home            = /path/to/virtualenv

    # process-related settings
    # master
    master          = true
    # maximum number of worker processes
    processes       = 10
    # the socket (use the full path to be safe
    socket          = /path/to/your/project/mysite.sock
    # ... with appropriate permissions - may be needed
    # chmod-socket    = 664
    # clear environment on exit
    vacuum          = true

然后使用这个文件运行uswgi：

    uwsgi --ini mysite_uwsgi.ini # the --ini option is used to specify a file

再次，测试Django站点是否如预期工作。


## 系统级安装uWSGI
目前，uWSGI只装在我们的虚拟环境中；出于部署需要，我们将需要让它安装在系统范围中。

停用你的虚拟环境:

    deactivate

然后在系统范围中安装uWSGI:

    sudo pip3 install uwsgi

    # Or install LTS (long term support).
    pip install http://projects.unbit.it/downloads/uwsgi-lts.tar.gz

uWSGI的wiki描述了几种 [installation procedures](https://uwsgi-docs.readthedocs.io/en/latest/). 在系统级安装 uWSGI之前，值得考虑下要选择哪个版本，以及最合适的安装方法。

再次检查你是否仍然能如之前那样运行uWSGI:

    uwsgi --ini mysite_uwsgi.ini # the --ini option is used to specify a file

> 按照这一节的步骤没有调通，可能是由于我的系统python环境是2.7的，而我的python虚拟开发环境是3.6的。不过我在uwsgi命令前加上了我的虚拟环境的路径，也就是使用的是虚拟环境的uwsgi，成功运行了。


## Emperor模式
uWSGI可以运行在’emperor’模式。在这种模式下，它会监控uWSGI配置文件目录，然后为每个它找到的配置文件生成实例 (‘vassals’)。

每当修改了一个配置文件，emperor将会自动重启 vassal.

    # create a directory for the vassals
    sudo mkdir /etc/uwsgi
    sudo mkdir /etc/uwsgi/vassals
    # symlink from the default config directory to your config file
    sudo ln -s /path/to/your/mysite/mysite_uwsgi.ini /etc/uwsgi/vassals/
    # run the emperor
    uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

你或许需要使用sudo来运行uWSGI:

    sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

选项表示:
- emperor: 查找vassals (配置文件)的地方
- uid: 进程一旦启动后的用户id
- gid: 进程一旦启动后的组id

检查站点；它应该在运行。


## 系统启动时运行uWSGI
最后一步是让这一切在系统启动的时候自动发生。

对于许多系统来说，最简单 (如果不是最好的)的方式是使用 rc.local 文件。

编辑 /etc/rc.local 然后在”exit 0”行前添加:

    /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log

应该就这样！

> 指定用户和用户组这一块，还没搞懂。我是在root用户下开发的，只有指定root是运行正常的。


## [进一步的配置](http://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/tutorials/Django_and_nginx.html#id18)
点击链接查看
