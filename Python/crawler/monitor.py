import psutil
import time

class CrawlerMonitor:
    @staticmethod
    def get_crawler_status():
        status = {}
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            if 'python' in proc.info['name'] and 'crawler' in proc.info['cmdline']:
                status[proc.info['pid']] = {
                    'status': proc.info['status'],
                    'cpu_percent': psutil.cpu_percent(),
                    'memory_mb': psutil.virtual_memory().used / 1024 / 1024
                }
        return status