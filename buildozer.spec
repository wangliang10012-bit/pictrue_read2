[app]

# 应用标题
title = Test App

# 包名
package.name = testapp

# 包域名
package.domain = com.test

# 源代码目录
source.dir = .
source.main_entrypoint = test_kivy.py

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas

# 应用版本
version = 1.0

# 依赖包
requirements = python3,kivy==2.3.0,pyjnius==1.6.1

# 屏幕方向
orientation = portrait

# 全屏模式（Android 15 建议启用）
fullscreen = 1

# Android API 版本
android.api = 34
android.minapi = 21
android.ndk_api = 21

# 架构
android.archs = arm64-v8a

# 权限（添加基本权限）
android.permissions = INTERNET,VIBRATE

# Wakelock（防止屏幕休眠）
android.wakelock = True

# 应用描述
android.app_description = Test Application

# 允许备份
android.allow_backup = True

# 包名（完整）
android.package_name = com.test.testapp

# 作者
author = Test Author


[buildozer]

# 日志级别
log_level = 2

# Root 警告
warn_on_root = 1

# 构建目录
build_dir = ./.buildozer

# 输出目录
bin_dir = ./bin

# p4a 分支
p4a.branch = master
