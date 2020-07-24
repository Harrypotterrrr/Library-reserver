# 图书馆自动抢座预约系统


![](https://img.shields.io/badge/language-python3.6+-green.svg) ![](https://img.shields.io/badge/author-Haolin_Jia-blue.svg) ![](https://img.shields.io/badge/platform-Windows|Linux|OSX-yellow.svg) ![](https://img.shields.io/badge/license-MIT-orange.svg) 

## Overview

由于疫情原因，北京市图书馆仅开放有限个数的座位，使得每日晚8点预约第三天后的座位有时变得很困难，但可以利用程序跳过手机验证码以及微信小程序直接申请

## Quickstart    

一步生成预约单和二维码

```shell
python main.py --reserve
```

如下图，和平台一致的预约信息和二维码图片生成至`./record`目录下

![](./pic/demo.jpg )

## Feature

- 稳定、快速、操作简单：无需使用微信小程序以及无需预约时的手机验证码

- 支持生成进入图书馆所需的预约票据信息和二维码图片

- 身份信息安全

- 支持朝阳区图书馆小庄馆、朝阳区图书馆劲松馆的自动预约。（暂不支持首都图书馆的预约，由于疫情原因，西城区图书馆和东城区图书馆暂不开放）

## Usage

### Step 1: Installation

```shell
pip install -r requirement.text
# 并检查 python版本: python --version 需要等于或高于 3.6
```

### Step 2: Configuration


修改`./config.json`的`chaoyang`中`payload`字段， 其中**粗体字**为必须修改项，其他可均保留默认值：

- **`name`**: **姓名**，身份唯二识别的键值
- **`idcard`**: **身份证号**，身份的唯二试别的键值
- `phone`: 手机号，非关键，建议修改
- `sex`: 性别，非关键，建议修改
- `add`: 户口所在区，非关键，可保持默认
- **`addrs`**: **居住地址**，尽量详细，否则可能因为地址过短过于简单而预约失败
- `tiwen`: 体温，无需修改，（吐槽：这个是图书馆预约平台的程序员起的变量名）
- **`date`**: **预约时间**
- `time`: 值只能为“上午”或者“下午”，表示预约图书馆时间为上午或下午， 留空默认表示上下午均需预约
- `site`: 值只能为“小庄馆”或者“劲松馆”，预约图书馆名称，默认为劲松馆
- `seat`: 座位号，eg. D4    
- `openid`: openid是微信号id的唯一识别标志，默认为空，表示程序会自动为你申请一个虚拟id用来预约图书馆座位，一旦申请请勿删除或更改openid值，否则会导致预约信息丢失。此外如果你通过api得到你微信的id可以填入，此时预约信息会同步到你的手机，本程序也不会申请虚拟id
- 其余留空即可

### Step 3: Get Started

```shell
python main.py --reserve
```
至此`./record`目录下应当已经生成进入图书馆所需的预约信息和二维码图片

此外，程序可以取消预约, `order`值为`./record/check_list.json`文件中，希望取消预约的对应order的值

```shell
python main.py --cancel <order>
```

如果需要更新预约信息，可以使用`--update`参数

```shell
python main.py --update
```

重新生成预约单和二维码图片

```shell
python main.py --qrcode
```

可帮助多位好友预约，只需创建多个`config.json`，例如`config.bak.json`

```shell
python main.py --config ./config.bak.json --reserve
```

## Issues

- Mac等OSX操作系统的可能遇到没有·Deng.ttf·字体的potential bug, 尝试修改`ticket.py`中包含`Deng`的字段至`/system/font`中包含字体即可
- 通过Usage的文档，有人可能已经意识到这个预约平台有一个critical level的漏洞，此处提醒各位请勿利用平台漏洞和本程序做损害他人利益的事情！只要自己预约上开开心心去图书馆就好啦
- 指定的座位号预约存疑，可能被系统忽略