# -*- coding: utf-8 -*-
import scrapy

class ArchiveItCollectionSpider(scrapy.Spider):
    name = 'ArchiveItCollection'
    allowed_domains = ['archive-it.org']
    start_urls = ['https://archive-it.org/collections/13529/']

    def parse(self, response):
        # para cada elemento na lista de resultados
        for el in response.css('#search-results > div.result-item'):
            # os dois primeiros atributos 'url' são o título e a url respectivamente
            title = el.css('h3.url::text').re_first(r'\s*Title:\s*(.*)')
            # pula o item caso não haja título
            # algumas vezes quando a página não foi acessada pelo archive-it
            # o item só possui o atributo URL
            if not title:
                continue

            title = title.strip()
            url = el.css('h3.url > a::text').get()
            descrition = el.css('p::text').get().strip()
            language, top_level_domain = None, None
            metadata = [t.strip() for t in el.css('.moreMetadata > p > a::text').getall()]
            if len(metadata) == 2:
                language, top_level_domain = metadata

            yield {
                    'title': title,
                    'url': url,
                    'description': descrition,
                    'language': language,
                    'top-level domain': top_level_domain,
            }

        # próxima página
        yield from response.follow_all(css = '#pageNext', callback = self.parse)


