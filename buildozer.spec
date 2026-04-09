[app]

# 应用标题
title = Test App

# 包名
package.name = test_app

# 包域名
package.domain = org.test

# 源代码目录
source.dir = .
source.main_entrypoint = test_kivy.py

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas

# 应用版本
version = 1.0.0

# 最小依赖（只保留必需的）
requirements = python3,kivy==2.2.1

# 屏幕方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android 权限
android.permissions = INTERNET

# Android API 版本（使用稳定版本）
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.archs = arm64-v8a

# 跳过 SDK 更新
android.skip_update = False

# 应用描述
android.app_description = Test Application

# 允许备份
android.allow_backup = True

# 背景颜色
android.background_color = #ffffff

# 包名（完整）
android.package_name = org.test.test_app

# 作者
author = Test

# 邮箱
author.email = test@test.com


[buildozer]

# 日志级别（提高到2以便调试）
log_level = 2

# Root 警告
warn_on_root = 1

# 构建目录
build_dir = ./.buildozer

# 输出目录
bin_dir = ./bin

# p4a 分支（使用稳定分支）
p4a.branch = master
