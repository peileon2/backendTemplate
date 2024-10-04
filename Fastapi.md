# Fastapi

## 结构

### models  

用于存储数据库结构，并迁移，方便orm调用

* SKU

| key    | type   |
| ------ | ------ |
| id     | int    |
| name   | string |
| width  | float  |
| height | float  |
| length | float  |
| weight | float  |

* USER

| key           | type        |
| ------------- | ----------- |
| fastapi-users | class       |
| sku           | List(class) |
| deliveryFees  | list(class) |

* DliveryFees

| key      | type        |
| -------- | ----------- |
| id       | int         |
| name     | str         |
| baserate | list[class] |
| ahs      | list[class] |
| rdc      | list[class] |
| os       | list[class] |
|          |             |

USER的模型可由fastapi-users继承

### schemas

用于存储用户输入模型

* base
* create
* update
* delete

##### 类型1--不包含字项

1. select-schema
   1. 不含id
   2. 不含关系
   3. 包含其他字段（不敏感）
2. create-schema
   1. 不含id（自增）
   2. 不含外键id（无外键）
   3. 包含
3. update-schema

##### 类型2--包含子项

1. select-schema
   1. 不包含id
   2. 不含关系
   3. 包含子项字段
2. create-schema
   1. 不含id
   2.  不含外键id（controller内部运转，不由外界传入）
   3. 包含其他字段
3. update-schema

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

### alembic

```
alembic revision --autogenerate -m "first" 
```

```
alembic upgrade head
```

迁移数据库

1. 配置数据库
2. 生成version
3. 根据verison迭代

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
  * 输入长宽高，毛重即可计算，无需权限验证
  * 保存

* 保存各参数信息
  * 根据id批量保存
  * 批量根据父表，改变子表
* 保存费用文档信息



### CURD JSON

* UPDATE JSON

更新操作：

1. baserate采用类似sku的curd
2. 其余子项修改，全部采用删除，然后新建
3. 目前bug（一对多的更新相当麻烦）

```json
{
    "name": "Updated Delivery Fee Name",
    "base_rates": [
        {
            "id": 1, 
            "rate_weight": 10,
            "zone": 2,
            "fees": 15.75
        },
        {
            "id": 2,
            "rate_weight": 20,
            "zone": 3,
            "fees": 25.50
        }
    ],
    "das_items": [
        {
            "id": 1, 
            "das_type": 1, 
            "gd_hd_type": 1,  
            "res_comm_type": 1,
            "fees": 30.00
        }
    ],
    "oversizes": [
        {
            "id": 1,  
            "gd_hd_type": 2,  
            "fees": 50.00
        }
    ],
    "ahs_items": [
        {
            "id": 1,  
            "ahs_type": 1,  
            "gd_hd_type": 1, 
            "res_comm_type": 2,  
            "fees": 40.00
        }
    ],
    "rdc_items": [
        {
            "id": 1,  
            "gd_hd_type": 2,  
            "fees": 20.00
        }
    ],
    "demand_item": {
        "DIM": 100,
        "peak_os_charge": 5.00,
        "peak_rdc_charge": 3.50,
        "fuel_rate": 1.25,
        "id": 1  
    }
}
```

* CREATE JSON

```json
{
  "name": "New Delivery Fee Name",
  "base_rates": [
    {
      "rate_weight": 15,
      "zone": 1,
      "fees": 10.50
    },
    {
      "rate_weight": 25,
      "zone": 2,
      "fees": 20.75
    }
  ],
  "das_items": [
    {
      "das_type": 1,
      "gd_hd_type": 1,
      "res_comm_type": 1,
      "fees": 25.00
    }
  ],
  "oversizes": [
    {
      "gd_hd_type": 2,
      "fees": 30.00
    }
  ],
  "ahs_items": [
    {
      "ahs_type": 2,
      "gd_hd_type": 1,
      "res_comm_type": 2,
      "fees": 35.00
    }
  ],
  "rdc_items": [
    {
      "gd_hd_type": 1,
      "fees": 15.00
    }
  ],
  "demand_item": {
    "DIM": 200,
    "peak_os_charge": 4.00,
    "peak_rdc_charge": 2.50,
    "fuel_rate": 1.10
  }
}

```

### 数据校验

1. zone必须是2~8且只能是2~8

## 服务器

### 跨域

### 日志

### 测试

### 打包

### 上传

## 规划

### 补全业务

1. Fedex、
   1. 查出sku，得到它的所有属性
   2. 筛选出对应的HD&gd，

2. 其余运费

### Pyqt

### 服务器

