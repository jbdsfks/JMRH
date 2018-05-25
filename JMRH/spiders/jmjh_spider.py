import scrapy
import re
from JMRH.items import JmrhItem


class JmjhSpider(scrapy.Spider):
    name = "jmjh"
    allowed_domains = ["jmjh.miit.gov.cn"]
    start_urls = [
        "http://jmjh.miit.gov.cn/loadModuleWebMessage.action?moduleId=222&typeId=1060"     #国家
        # "http://jmjh.miit.gov.cn/loadModuleWebMessage.action?moduleId=222&typeId=1408"   #部门
    ]

    def parse(self, response):
        for ZCUrl in response.xpath('//a[contains(@href,"newsInfoWebMessage.action")]/@href').extract():
            url = "http://jmjh.miit.gov.cn/" + ZCUrl
            # time.sleep(5)
            yield scrapy.Request(url, callback=self.newsMessage)

        next_page = response.xpath('//input[contains(@value,"下一页")]/@onclick').extract_first().split('\'')[1]
        if next_page:
            yield scrapy.Request("http://jmjh.miit.gov.cn/loadModuleWebMessage.action"+next_page, self.parse)

    def newsMessage(self, response):
        title = response.xpath('//div[contains(@id,"con_t")]/text()').extract_first().replace(' ', '')
        times = response.xpath('//span[contains(@id,"con_time")]/text()').extract_first().replace(' ', '')
        source = response.xpath('//td[contains(@align,"center")]').extract()[1].split("：")[-1].split(" ")[0] \
            .replace(' ', '')
        url = response.url
        content = response.xpath('//div[contains(@id,"con_con")]').extract_first()
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

    # def newsMessage(self, response):
    #     title = response.xpath('//div[contains(@id,"con_t")]/text()').extract_first()
    #     time = response.xpath('//span[contains(@id,"con_time")]/text()').extract_first()
    #     source = response.xpath('//td[contains(@align,"center")]').extract()[1].split("：")[-1].split(" ")[0]
    #     content = response.xpath('//div[contains(@id,"con_con")]').extract_first() \
    #         .replace('\r', '') \
    #         .replace('\t', '') \
    #         .replace('\n', '') \
    #         .replace(' ', '')
    #     yield JmrhItem(
    #         _1_title=title,
    #         _2_time=time,
    #         _3_source=source,
    #         _4_content=content
    #     )
