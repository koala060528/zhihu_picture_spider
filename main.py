import requests
import json
import os
from bs4 import BeautifulSoup
import sys
import urllib.request
import urllib.parse


class Crawler:
    _question_id = ''
    _anonymous_index = 0
    _answer_index = 0
    _limit = 5
    _offset = 0
    _path = ''
    _flag = True
    _cookies = {
        '_zap': '5a59ba26-0314-4870-9785-a9e07dcf5a68',
        'd_c0': 'ABBs9a8gQg2PTrZll1svlanOJCa9_gzBDqQ=|1520556053',
        '__DAYU_PP': 'By7bEzRReNZ6bZiyFeqyffffffff848c84d3b24e',
        'q_c1': 'a861468183674c3ba1b186d0bbcc9d1f|1528072041000|1519700044000',
        'tgw_l7_route': 'b3dca7eade474617fe4df56e6c4934a3',
        '_xsrf': '39555403-0a0a-4d5e-9d99-b97a04f518a5',
        'l_n_c': '1',
        'l_cap_id': 'NGE5ZGQ2ZjU3YjhlNDU4Njg4YmUxMThlNWRjYzJiNDE=|1529909499|7b0b338ad21e3dc69d3c734cfda725363ba78b9e',
        'r_cap_id': 'NGNiMjU0YmZmMTY4NDQ4NmIxOWY1ZTg4NGJkOWJlYjk=|1529909499|b621571191a9c583d069fb1cf2054309f13b605b',
        'cap_id': 'YjEzM2M1ZjFiYzIxNDUwOTk3MTdhYjlhZDk3NjgzMTQ=|1529909499|36c9ba9cc9a92f0afa4c9456d739ad3cc5169335',
        'n_c': '1',
        'capsion_ticket': '2|1:0|10:1529909736|14:capsion_ticket|44:NWMwODI2ZjVkY2JkNDBmNWI1NzZmNGIwODE1OTAxZGQ=|05deb1eae5365fe6a7baea85a168aa8875dc00af2ed8d388f9487c6b858aea42',
        'z_c0': '2|1:0|10:1529909789|4:z_c0|92:Mi4xYklPTUNnQUFBQUFBRUd6MXJ5QkNEU1lBQUFCZ0FsVk5IZUFkWEFCRzFxeTNQQ3BBQXNVeEhvUmR4YjhFYUVTQlZB|272e8b186ff3bb6efc03295bc44f69ad4fc0d50ac15e30b3ac6f215e6b786726',
        '__utma': '51854390.1030854294.1527822359.1527822359.1529909895.2',
        '__utmb': '51854390.0.10.1529909895',
        '__utmc': '51854390',
        '__utmz': '51854390.1529909895.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmv': '51854390.100--|2=registration_date=20180625=1^3=entry_date=20180227=1'
    }

    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/53',
        'referer': 'https: // www.zhihu.com / question / 37709992',
        'accept': 'application / json, text / plain, * / *',
        'accept - encoding': 'gzip, deflate, br',
        'accept - language': 'zh - CN, zh;q = 0.9',

    }

    def __init__(self, question_id, limit=5, offset=0):
        self._question_id = question_id
        self._limit = limit
        self._offset = offset
        # 创建存储目录
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', question_id)
        if not os.path.exists(path):
            os.makedirs(path)
        self._path = path

    def get_js(self, limit, offset):
        res = requests.get(
            'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}&sort_by=default'.format(
                self._question_id, str(limit), str(offset)), headers=self._headers, cookies=self._cookies)
        data = json.loads(res.text)
        if self._flag:
            print('本题下共有{0}个回答'.format(data.get('paging').get('totals')))
            self._flag = False
        for ans in data.get('data'):
            print('正在抓取第{0}个答案，答主是：{1},赞同数：{2},评论数：{3}'.format(
                self._answer_index, ans.get('author').get('name'), ans.get('voteup_count'), ans.get('comment_count')))
            self._answer_index += 1
            self.get_img_url(ans.get('content'), ans.get('author').get('name'))

        if not data.get('paging').get('is_end'):
            self._offset += self._limit
            self.get_js(limit=self._limit, offset=self._offset)

    def get_img_url(self, h5, author):
        soup = BeautifulSoup(h5, "html.parser")
        tags = soup.findAll('noscript')
        index = 0
        for tag in tags:
            print('获取图片tag')
            url = tag.contents[0].attrs.get('data-original')
            if url is None:
                url = tag.contents[0].attrs.get('src')
            print('获取url:{0}'.format(url))
            self.save_img(url=url, author=author, index=index)
            index += 1

    def save_img(self, url, author, index):
        if url is None:
            return
        ext = url.split('/')[-1].split('.')[-1]
        if author != "匿名用户":
            filename = os.path.join(self._path, author + '-' + str(index) + '.' + ext)
        else:
            filename = os.path.join(self._path, author + '-' + str(self._anonymous_index) + '.' + ext)
            self._anonymous_index += 1
        if not os.path.exists(filename):
            # img = requests.get(url, stream=True)
            req = urllib.request.Request(url)
            img = urllib.request.urlopen(req).read()
            # if img.status_code == 200:
            print('正在保存：{0}'.format(filename))
            open(file=filename, mode='wb').write(img)
            # else:
            #     print('下载失败，错误代码：{0}'.format(img.status_code))

    def start(self):
        self.get_js(limit=self._limit, offset=self._offset)


if __name__ == '__main__':
    sys.setrecursionlimit(10000)  # 设置递归深度
    crawler = Crawler(question_id='37709992', limit=10, offset=0)
    crawler.start()
