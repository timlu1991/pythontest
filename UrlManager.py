# coding=utf-8
import cPickle
import hashlib
class UrlManager(object):
    def __init__(self):
        self.new_urls=self.load_progress('new_url.txt')
        self.old_urls=self.load_progress('old_url.txt')

    def load_progress(self, path):
        print '[+] 从文件加载进度：%s' % path
        try:
            with open(path,'rb') as f:
                tmp=cPickle.load(f)
                return tmp
        except:
            print '[!] 无进度文件，创建：%s' % path
        return set()

    def add_new_url(self, url):
        '''
        将新的url加入到没爬取的URL集合中
        :param url:
        :return:
        '''
        if url is None:
            return
        m=hashlib.md5()
        m.update(url)
        url_md5=m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)



    def has_new_url(self):
        '''
        判断是否有未爬去的ｕｒｌ
        :return: 
        '''
        return self.new_url_size()!=0
    def get_new_url(self):
        '''
        获取一个未爬取的url
        :return:
        '''
        new_url=self.new_urls.pop()
        m=hashlib.md5()
        m.update(new_url)
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def old_url_size(self):
        '''
        获取已经爬取的url集合的大小
        :return:
        '''
        return  len(self.old_urls)


    def save_progress(self, path, data):
        '''
        保存进度
        :param path:
        :param data:
        :return:
        '''
        with open(path,'wb') as f:
            cPickle.dumps(data,f)

    def add_new_urls(self, urls):
        '''
        将新的urls添加到未爬去的url
        :param urls:
        :return:
        '''
        if urls is None or len(urls)==0:
            return
        for url in urls:
            self.add_new_url(url)


    def new_url_size(self):
        '''
        获取未爬取url集合的大小
        :return:
        '''
        return len(self.new_urls)
    







