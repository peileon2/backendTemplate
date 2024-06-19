# Fastapi

## 结构

### models

用于存储数据库结构，并迁移，方便orm调用

* SKU
* USER
* ...

USER的模型可由fastapi-users继承

### schemas

用于存储用户输入模型

* base
* create
* update
* delete

### controller

用于使用orm封装`models`的crud，便于`api`中联合使用不同的models

### Api

与用户交互，将`controller`中的不同model的操作封装成一个，并采用schema与用户交互

* login
* crud-models

权限认证：

* 一个用户一天内不能请求创建API超过10次
* 只有登陆后的用户，才能允许创建请求
* 超级用户可以删除别的user

### utils

* 用于编写业务内容
* 工厂类

## 包管理

### poetry

取代pip进行包管理

* 简洁
* 干净

### orm

现决定采用SQLAlchemy==异步版==

* 社区丰富，查错，从Gpt找答案方便
* 支持`fastapi-users`
* 支持迁移时自定义主键

### fastapi-users

* 集成了users的所有操作

* 避免重复造轮子

### pydantic & typing

* 数据校验

### email

* 采用阿里云发送email以及验证码等信息

### jwt

* 进行id传送
* 免登录

### sentry_sdk

* 用户监视错误
* 暂时不用

## 数据库

### mysql

* 开发环境采用本地数据库
* 运行环境采用阿里云服务器

### redis

项目过小不采用

## Api

### 用户系统

* 注册
* 登录
* 修改密码
* 注销用户
* 忘记密码

### 业务系统

* 计算快递费
* 保存各参数信息
* 保存费用文档信息
