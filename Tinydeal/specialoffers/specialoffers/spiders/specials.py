import scrapy


class SpecialsSpider(scrapy.Spider):
    name = 'specials'
    allowed_domains = ['web.archive.org']
    item_count=0

    def start_requests(self):
        yield scrapy.Request(url='https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html', callback=self.parse, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'})

    def parse(self, response):
        for x in response.xpath("//ul[@class= 'productlisting-ul']/div/li"):
            Name= x.xpath(".//a[@class='p_box_title']/text()").get()
            link = response.urljoin(x.xpath(".//a[@class= 'p_box_title']/@href").get())
            discounted_p= x.xpath(".//div[@class='p_box_price']/span[1]/text()").get()
            price= x.xpath(".//div[@class='p_box_price']/span[2]/text()").get()
            yield{
                "Product":Name,
                "P_link": link,
                "Discount":discounted_p,
                "price":price,
                "item_count":SpecialsSpider.item_count,
                "header":response.request.headers['user-agent']
            }
        
        new_page = response.xpath("//a[@class='nextPage']/@href").get()
        if new_page:
            SpecialsSpider.item_count+=1
            yield scrapy.Request(url=new_page, callback= self.parse, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'})


