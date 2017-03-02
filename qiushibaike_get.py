#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
# import urllib
import re
import thread
import time


# ----------- 加载处理糗事百科 -----------
class Spider_Model:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False

        # 将所有的段子都扣出来，添加到列表中并且返回列表

    def GetPage(self, page):
        my_url = "http://m.qiushibaike.com/hot/page/" + page
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        headers = {'User-Agent': user_agent, 'Referer': 'http://www.qiushibaike.com/'}
        req = urllib2.Request(my_url, headers=headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        # encode的作用是将unicode编码转换成其他编码的字符串
        # decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("utf-8")

        # 找出所有class="content"的div标记
        # re.S是任意匹配模式，也就是.可以匹配换行符
        # myItems = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>', unicodePage, re.S)
        myItems = re.findall('<div.*?class="content">\s*?<span>(.*?)</span>\s*?</div>', unicodePage, re.S)
        items = []
        for item in myItems:
            # item 中第一个是div的标题，也就是时间
            # item 中第二个是div的内容，也就是内容
            # items.append([item[0].replace("\n", ""), item[1].replace("\n", "")])
            items.append(item.replace('<br/>', '').replace(' ', ''))
        return items

        # 用于加载新的段子

    def LoadPage(self):
        # 如果用户未输入quit则一直运行
        while self.enable:
            # 如果pages数组中的内容小于2个
            if len(self.pages) < 2:
                try:
                    # 获取新的页面中的段子们
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except:
                    print '无法链接糗事百科！'
            else:
                time.sleep(2)

    def ShowPage(self, nowPage, page):
        num = 1
        for items in nowPage:
            # print u'第%d页' % page, items[0], items[1]
            print u'第%d页:第%d条->' % (page, num), items
            num += 1
            myInput = raw_input()
            if myInput == "quit":
                self.enable = False
                print '退出程序，谢谢使用!'
                break

    def Start(self):
        self.enable = True
        page = self.page

        print u'正在加载中请稍候......'

        # 新建一个线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage, ())

        # ----------- 加载处理糗事百科 -----------
        while self.enable:
            # 如果self的page数组中存有元素
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage, page)
                page += 1


                # ----------- 程序的入口处 -----------

if __name__ == '__main__':
    print u"""
    ---------------------------------------
       操作：输入quit退出阅读糗事百科
       功能：按下回车依次浏览今日的糗百热点
    ---------------------------------------
    """

    print u'请按下回车浏览今日的糗百内容：'
    raw_input(' ')
    myModel = Spider_Model()
    myModel.Start()
# myModel = Spider_Model()
# for pag in range(1,5):
#     pagedata = myModel.GetPage(str(pag))
#     print '\n\n'.join(pagedata)