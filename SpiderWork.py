# coding:utf-8
from multiprocessing.managers import BaseManager

from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser


class SpiderWork(object):
    def __init__(self):
        '''
        初始化分布式进程的工作节点的连接工作
        实现第一步，使用basemanager注册获取queue的方法名称
        :return:
        '''
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        #实现第二步,连接到服务器:
        server_add='127.0.0.1'
        print ('connect to server %s....' % server_add)
        #端口和验证口令必须和服务进程一致
        self.m=BaseManager(address=(server_add,8001),authkey='baike')
        #从网络连接
        self.m.connect()
        #实现第三步:获取queue的对象：
        self.task=self.m.get_task_queue()
        self.result=self.m.get_result_queue()
        #初始化页面下载器和解析器
        self.downloader=HtmlDownloader()
        self.parser=HtmlParser()
        print 'init finish'


    def crawl(self):
        while(True):
            try:
                if not self.task.empty():
                    url=self.task.get()

                    if url=='end':
                        print '控制节点通知爬虫节点停止工作..'
                        #接着通知其他节点停止工作
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print '爬虫节点正在解析 :%s' %url.encode('utf-8')
                    content=self.downloader.download(url)
                    new_urls,data= self.parser.parser(url,content)
                    self.result.put({"new_urls":new_urls,"data":data})
            except EOFError,e:
                print "连接工作节点失败"
                return
            except Exception,e:
                print e
                print 'crawl fail'



if __name__ == '__main__':
    spider=SpiderWork()
    spider.crawl()
    