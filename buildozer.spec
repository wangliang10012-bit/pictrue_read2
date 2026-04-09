[app]

# 应用标题
title = TestApp

# 包名
package.name = testapp

# 包域名
package.domain = com.testapp

# 源代码目录
source.dir = .
source.main_entrypoint = test_kivy.py

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas

# 应用版本
version = 1.0

# 依赖（稳定版本组合）
requirements = python3==3.11.9,kivy==2.2.1

# 屏幕方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android API 版本（vivo Android 15 兼容性最好的版本）
android.api = 34
android.minapi = 24
android.ndk_api = 24
android.sdk = 34
android.ndk = 27c

# 架构（vivo X200 是 64 位）
android.archs = arm64-v8a

# 权限（vivo 需要明确声明）
android.permissions = INTERNET,VIBRATE,WAKE_LOCK

# 禁用电池优化（vivo 重要配置）
android.add_android_manifest_entries =
    <uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS" />

# Wakelock
android.wakelock = True

# 应用描述
android.app_description = Test Application

# 允许备份
android.allow_backup = True

# 调试模式（开发阶段启用）
android.debug = True

# 包名
android.package_name = com.testapp.testapp

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
