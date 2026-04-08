[app]

# 应用标题
title = 我的资产

# 包名
package.name = finance_app

# 包域名
package.domain = org.create_app

# 源代码目录
source.dir = .
# 在它下面添加：
source.main_entrypoint = main_kivy.py

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas,ttc,jpeg
source.include_patterns = icons/*
# 应用版本
version = 1.0.0

# 依赖包
requirements = python3,kivy==2.3.0,pillow,pyjnius,requests,urllib3,chardet,idna,certifi,hostpython3,setuptools,cython

# 屏幕方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android API 版本
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk_api = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

# 跳过 SDK 更新
android.skip_update = False

# 应用描述
android.app_description = 我的资产管理应用

# 允许备份
android.allow_backup = True

# 背景颜色
android.background_color = #f5f5f5

# 包名（完整）
android.package_name = org.create_app.finance_app

# 作者
author = Your Name

# 邮箱
author.email = your@email.com

# 网址
author.website = https://example.com


[buildozer]

# 日志级别
log_level = 2

# Root 警告
warn_on_root = 1

# 构建目录
build_dir = ./.buildozer

# 输出目录
bin_dir = ./bin

# 固定 p4a 版本（解决 aidl 问题）
# p4a.branch = release-2022.12.20
