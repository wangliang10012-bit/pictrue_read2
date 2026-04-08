import os
import sys
import traceback
from datetime import datetime


class AndroidLogger:
    """Android 端日志记录器，将日志保存到文件"""
    
    def __init__(self):
        self.log_file = None
        self.is_android = sys.platform == 'android'
        self.log_messages = []  # 内存缓冲区
        
    def setup(self):
        """初始化日志文件"""
        try:
            if self.is_android:
                # Android 15 适配：使用应用私有目录
                try:
                    from jnius import autoclass
                    
                    # 方法1：尝试使用外部存储（可能需要权限）
                    try:
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
                        
                        # 写入之前缓冲的日志
                        for msg in self.log_messages:
                            try:
                                with open(self.log_file, 'a', encoding='utf-8') as f:
                                    f.write(msg + '\n')
                            except:
                                pass
                        self.log_messages = []
                        
                    except Exception as e1:
                        print(f"外部存储日志失败: {e1}，尝试应用私有目录")
                        
                        # 方法2：使用应用私有目录（不需要权限）
                        PythonActivity = autoclass('org.kivy.android.PythonActivity')
                        activity = PythonActivity.mActivity
                        
                        # 获取应用私有外部存储目录
                        external_files_dir = activity.getExternalFilesDir(None)
                        if external_files_dir:
                            log_dir = os.path.join(external_files_dir.getAbsolutePath(), 'logs')
                            
                            if not os.path.exists(log_dir):
                                os.makedirs(log_dir)
                            
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            self.log_file = os.path.join(log_dir, f'app_log_{timestamp}.txt')
                            
                            with open(self.log_file, 'w', encoding='utf-8') as f:
                                f.write(f"=== 应用启动日志 (私有目录) ===\n")
                                f.write(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                f.write(f"平台: {sys.platform}\n")
                                f.write(f"Python 版本: {sys.version}\n")
                                f.write(f"日志路径: {self.log_file}\n")
                                f.write("=" * 50 + "\n\n")
                            
                            print(f"私有目录日志文件已创建: {self.log_file}")
                            
                            # 写入缓冲日志
                            for msg in self.log_messages:
                                try:
                                    with open(self.log_file, 'a', encoding='utf-8') as f:
                                        f.write(msg + '\n')
                                except:
                                    pass
                            self.log_messages = []
                        else:
                            raise Exception("无法获取应用私有目录")
                            
                except Exception as e:
                    print(f"Android 日志初始化完全失败: {e}")
                    self.log_file = None
            else:
                # 非 Android 平台，使用当前目录
                log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.log_file = os.path.join(log_dir, f'app_log_{timestamp}.txt')
                
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.write(f"=== 应用启动日志 (Desktop) ===\n")
                    f.write(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"平台: {sys.platform}\n")
                    f.write(f"Python 版本: {sys.version}\n")
                    f.write("=" * 50 + "\n\n")
                
                print(f"桌面端日志文件已创建: {self.log_file}")
        except Exception as e:
            print(f"日志系统初始化完全失败: {e}")
            self.log_file = None
    
    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # 控制台输出
        print(log_entry)
        
        # 文件输出
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_entry + '\n')
            except:
                pass
        else:
            # 如果文件未初始化，保存到内存缓冲区
            self.log_messages.append(log_entry)
    
    def log_error(self, error_msg, exception=None):
        """记录错误信息"""
        self.log(error_msg, "ERROR")
        if exception:
            tb_str = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.log(tb_str, "TRACEBACK")


# 创建全局日志实例
logger = AndroidLogger()
