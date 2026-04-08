import os
import sys
import traceback
from datetime import datetime


class AndroidLogger:
    """Android 端日志记录器，将日志保存到文件"""

    def __init__(self):
        self.log_file = None
        self.is_android = sys.platform == 'android'

    def setup(self):
        """初始化日志文件"""
        if self.is_android:
            try:
                from jnius import autoclass
                Environment = autoclass('android.os.Environment')
                storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
                log_dir = os.path.join(storage_path, 'finance_app_logs')

                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.log_file = os.path.join(log_dir, f'app_log_{timestamp}.txt')

                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.write(f"=== 应用启动日志 ===\n")
                    f.write(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"平台: {sys.platform}\n")
                    f.write(f"Python 版本: {sys.version}\n")
                    f.write(f"工作目录: {os.getcwd()}\n")
                    f.write("=" * 50 + "\n\n")

                print(f"日志文件已创建: {self.log_file}")
            except Exception as e:
                print(f"创建日志文件失败: {e}")

    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        print(log_entry.strip())

        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_entry)
            except:
                pass

    def log_error(self, error_msg, exception=None):
        """记录错误信息"""
        self.log(error_msg, "ERROR")
        if exception:
            tb_str = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.log(tb_str, "TRACEBACK")


# 创建全局日志实例
logger = AndroidLogger()
