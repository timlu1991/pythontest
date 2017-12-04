# coding:utf-8
import codecs
import time


class DataOutput(object):
    def __init__(self):
        self.datas = []
        self.filepath = 'baike_%s.html'%(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) )
        self.output_head(self.filepath)

    def output_end(self, filepath):
        '''
        输出html结束
        :param filepath:文件储存路径
        :return:
        '''
        fout=codecs.open(filepath,'a',encoding='utf-8')
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas)>10:
            self.output_html(self.filepath)

    def output_head(self, filepath):
        '''
        将html头写进去
        :param filepath:
        :return:
        '''
        fout=codecs.open(filepath,'w',encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        fout.close()

    def output_html(self, filepath):
        '''
        将数据写入html文件中
        :param filepath:
        :return:
        '''
        fout=codecs.open(filepath,'a',encoding='utf-8')
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>"%data['url'])
            fout.write("<td>%s</td>"%data['title'])
            fout.write("<td>%s</td>"%data['summary'])
            fout.write("</tr>")
        self.datas=[]
        fout.close()
