import requests
import re
import time
import os
class VueCrawl:
    headers = {
        'Referer': 'https://vuejs.bootcss.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    # 网站根目录
    base_url = 'https://vuejs.bootcss.com'
    # v2版本根索引目录
    index_url = 'https://vuejs.bootcss.com/v2/'
    # 爬取目标
    targets = ['style-guide', 'api', 'cookbook', 'examples', 'guide']
    # 存放文档的根目录
    base_dir = os.path.abspath('')+"\\out\\vuefiles"

    # 提取url的正则表达式
    url_pattern = re.compile(r"<a\s+[^>]*href=\"([^#>\"]*)\"[^>]*>([^<]*)</a>")
    # 提取css的正则表达式
    css_pattern = re.compile(r"<link\s+[^>]*stylesheet[^>]*\s+href=\"([^#>\"]*)\"[^>]*>")
    # 提取js的正则表达式
    js_pattern = re.compile(r"<script\s+[^>]*src=\"([^>\"]*)\"[^>]*>\s*</script>")
    # 提取img的正则表达式
    img_pattern = re.compile(r"<img\s+[^>]*src=\"([^>\"]*)\"[^>]*>")
    # 由于爬取到的静态资源可能重复，所以用set存放
    css_set = set()
    js_set = set()
    img_set = set()
    # 抓取资源文件失败时记录错误信息
    error_info = []

    @staticmethod
    def download(abspath, content):
        """存储资源文件，参数content为二进制形式"""
        with open(abspath, 'wb')as f:
            f.write(content)

    def fix_pagesurl(self, content):
        """修正链接路径为相对路径，否则爬下来的链接不会指向正确的位置"""
        res_text = content.decode('utf-8', errors='ignore')
        css_search_res = self.css_pattern.findall(res_text)
        # css链接到base_dir目录的css文件夹下
        for item in css_search_res:
            if not item.startswith(('http://', 'https://')):
                self.css_set.add(item)
                res_text = res_text.replace(item, "../.." + item)

        js_search_res = self.js_pattern.findall(res_text)
        # js链接到base_dir目录的js文件夹下
        for item in js_search_res:
            if not item.startswith(('http://', 'https://')):
                self.js_set.add(item)
                res_text = res_text.replace(item, "../.." + item)

        img_search_res = self.img_pattern.findall(res_text)
        # 图片链接到base_dir目录的images文件夹下
        for item in img_search_res:
            if not item.startswith(('http://', 'https://')):
                self.img_set.add(item)
                res_text = res_text.replace(item, "../.." + item)

        url_search_res = self.url_pattern.findall(res_text)
        # 文档链接到当前文件夹下
        for item in url_search_res:
            item_url = item[0]
            if not item_url.startswith(('http://', 'https://')) and (
                    item_url.startswith("\\v2\\") and item_url.endswith('.html')):
                res_text = res_text.replace(item_url, "./" + item_url.split('/')[-1])
        return res_text.encode('utf-8')

    def crawl_pages(self, target):
        """根据target [style-guide','api','cookbook','examples','guide']这几个主要部分爬取"""
        url_set = set()

        url_search_res = self.url_pattern.findall(init_text)
        for item in url_search_res:
            item_url = item[0]
            if not item_url.startswith(('http://', 'https://')) and (
                    item_url.startswith("\\v2\\" + target) and item_url.endswith('.html')):
                url_set.add(item_url)

        # 下载每个部分的首页
        VueCrawl.download(self.base_dir + '\\v2\\' + target + '\\index.html', content=self.fix_pagesurl(init_r.content))

        # 对首页部分所有判定有效的链接进行下载
        for item in url_set:
            try:
                filename = item.split('/')[-1]
                res = requests.get(self.base_url + item, headers=self.headers)
                print(str(res.status_code) + ":" + res.url)
                res_content = res.content
                VueCrawl.download(self.base_dir + '\\v2\\' + target + '\\' + filename,
                                  content=self.fix_pagesurl(res_content))
                print('download file %s' % filename)
                time.sleep(2)
            except:
                info = 'download file %s faild' % item
                print(info)
                self.error_info.append(info)

    def download_staticfiles(self):
        """下载静态资源文件"""
        for item in self.js_set | self.img_set | self.css_set:
            try:
                res_content = requests.get(self.base_url + item, headers=self.headers).content
                self.download(self.base_dir + item, res_content)
                time.sleep(1)
            except:
                info = 'download file %s faild' % item
                print(info)
                self.error_info.append(info)

    def main(self):
        """主体部分 首先爬文档，之后下载静态资源文件"""
        for target in self.targets:
            self.crawl_pages(target)

        self.download_staticfiles()


if __name__ == '__main__':
    init_r = VueCrawl().main()

