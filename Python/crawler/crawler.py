import pika
import requests
from bs4 import BeautifulSoup
from hdfs import InsecureClient
import happybase
import multiprocessing

class DistributedCrawler:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')
        self.hbase_conn = happybase.Connection('localhost')
        self.hbase_table = self.hbase_conn.table('web_data')

    def start_consuming(self):
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_url,
            auto_ack=True
        )
        self.channel.start_consuming()

    def process_url(self, ch, method, properties, body):
        url = body.decode()
        print(f"Processing URL: {url}")

        # 1. 网页下载
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return

        # 2. 存储原始数据到HDFS
        hdfs_path = f"/webpages/{hash(url)}.html"
        with self.hdfs_client.write(hdfs_path) as writer:
            writer.write(response.content)

        # 3. 解析数据
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ''
        content = soup.get_text()

        # 4. 存储结构化数据到HBase
        self.hbase_table.put(
            url.encode('utf-8'),
            {
                'meta:title': title.encode('utf-8'),
                'content:raw': content.encode('utf-8')
            }
        )

        # 5. 提取新链接（示例）
        new_links = [a['href'] for a in soup.find_all('a', href=True)]
        # 将新链接发送回消息队列（需实现去重）

if __name__ == "__main__":
    # 启动3个进程模拟分布式
    processes = []
    for queue in ['queue1', 'queue2', 'queue3']:
        p = multiprocessing.Process(
            target=DistributedCrawler(queue).start_consuming
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()