# coding=utf-8
import re
import urlparse

from bs4 import BeautifulSoup


class HtmlParser(object):
    def parser(self, url, content):
        '''
        用于解析网页内容抽取url和数据
        :param url: 下载页面的url
        :param content: 下载页面的内容
        :return: 返回url和数据
        '''
        if url is None or content is None:
            return
        soup=BeautifulSoup(content,'html.parser',from_encoding='utf-8')
        news_urls=self._get_new_urls(url,soup)
        news_data=self._get_new_data(url,soup)
        return news_urls,news_data

    def _get_new_urls(self, url, soup):
        '''
        抽取新的url集合
        :param url: 下载页面的url
        :param soup:
        :return: 返回新的url结合
        '''
        new_urls=set()
        links=soup.find_all('a',href=re.compile(r'/item/.*'))#想了解一个对象，首先了解这个对象的方法。
        for link in links:
            #提取href属性
            new_url=link['href']
            #拼接完整网址
            new_full_url=urlparse.urljoin(url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        '''
        抽取有效数据
        :param url: 下载页面的url
        :param soup:
        :return:
        '''
        data={}
        data['url']=page_url
        title=soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div', class_='lemma-summary')
        # 获取到tag中包含的所有文版内容包括子孙tag中的内容,并将结果作为Unicode字符串返回
        data['summary'] = summary.get_text()
        return data



