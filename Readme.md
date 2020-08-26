## 安装步骤
1.安装django包
```
   pip install django
   pip install django==1.10.3
   pip install -i https://pypi.douban.com/simple/ django==1.10.3
```

2.生成工程项目
```
  django-admin startproject  demo
```

3.创建应用
```
   cd demo
   python manage.py startapp sign
```

4.在demo>settings.py中注册应用
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sign',
]
```

5.注册路由
   导入应用views文件
   注册路由信息
```python
    from sign import views

    urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    ]
```

6 创建admin数据库表：
```
python manage.py migrate
```

6.创建模板文件夹：templates
  创建： index.html
``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>demo</title>
</head>
<body>
<h1>发布会管理</h1>
<form method="post" action="/login/">
    <input name="username" type="text" placeholder="username"><br>
    <input name="password" type="text" placeholder="password"><br>
    <button id="btn" type="submit">登录</button>
    {% csrf_token %}
    {{ error }}
</form>
</body>
</html>
```

5.运行项目
```
 python manage.py runserver 127.0.0.1 8080
```

   
   
## 后台管理
1. 创建后台超级管理员账号密码
```
   python manage.py createsuperuser
``` 

## 新建数据库
1. models文件中定义表结果
2. admin 文件中注册
3. 执行表生成命令：

```
python manage.py makemigrations sign
python manage.py migrate
```
## 使用bootstrap3
### 安装Django-bootstrap3 
``` 
   pip install Django-bootstrap3
``` 
在setting 中注册bootstrap3 应用:
``` 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sign',
    'bootstrap3',
]
``` 
    
    
    
   
   
  
  