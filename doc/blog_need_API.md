﻿# API document

This is a document of blog web's API.It services for blog.

## 广告
广告相关合约并没有设计完，等待合约设计完成  
解决方案：  
- 发布广告时 资源类型固定为2（可更改）  
- 服务端在查数据时 发现类型（type）为2时 认定为广告  
- 服务器从链上查询到为广告时 做相关保存  
- 在/post/blog/info中 如果用户查询的是广告 则记录  
- 当记录量达到一定数目时 批量发送钱

## 日志

## 取消账户
因为合约取消代币  
所以没有注册发钱的功能 ——>考虑取消账户部分
原本功能：注册发钱，资源入库(形成列表 给用户批量看)
未来设想功能: 资源入库(形成列表 给用户批量看)，看广告给钱。

## js解密
考虑上传时加密内容

## 考虑上传计费

##  使用python SDk
将 receipt_watcher.py 替换为使用python SDK

