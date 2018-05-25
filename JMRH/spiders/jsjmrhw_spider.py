import scrapy
import re
from JMRH.items import JmrhItem


class JsjmrhwSpider(scrapy.Spider):
    name = "jsjmrhw"
    allowed_domains = ["jsjmrhw.org"]
    start_urls = [
        # 国家
        # "http://www.jsjmrhw.org/gjzc-1.aspx",
        # "http://www.jsjmrhw.org/gjzc-2.aspx"
        "http://www.jsjmrhw.org/dfzc.aspx"   #省内
    ]

    def parse(self, response):
        for ZCUrl in response.xpath('//a[contains(@target,"_blank")]/@href').re('/\d+.aspx'):
            url = "http://www.jsjmrhw.org" + ZCUrl
            # time.sleep(5)
            yield scrapy.Request(url, callback=self.newsMessage)

    def newsMessage(self, response):
        title = response.xpath('//td[contains(@height,"50")]/text()').extract_first()
        times = response.xpath('//span[contains(@class,"td12")]/text()').extract_first().split("：")[-1]
        source = ""
        url = response.url
        content = response.xpath('//div[contains(@id,"ctl00_ContentPlaceHolder1_cont_Show")]').extract_first()
        content = content.replace('\r', '') \
            .replace('\t', '') \
            .replace('\n', '').replace(' ', '').replace('　', '')
        dr = re.compile(r'<[^>]+>', re.S)
        content = dr.sub('', content)
        # content = ""
        # time.sleep(5)
        return JmrhItem(
            title=title,
            time=times,
            source=source,
            url=url,
            content=content
        )