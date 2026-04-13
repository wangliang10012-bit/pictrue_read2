[app]

# 应用标题
title = TestApp

# 包名
package.name = testapp

# 包域名
package.domain = org.kivy.test

# 源代码目录
source.dir = .
source.main_entrypoint = test_kivy.py

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas

# 应用版本
version = 1.0

# 依赖：不要锁定 Python 小版本！
requirements = python3,kivy==2.2.1

# 屏幕方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android API 版本
android.api = 34
android.minapi = 24
android.ndk_api = 24

# 架构
android.archs = arm64-v8a

# 权限
android.permissions =

# 应用描述
android.app_description = Test Application

# 允许备份
android.allow_backup = True

# 包名
android.package_name = org.kivy.test.testapp

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
