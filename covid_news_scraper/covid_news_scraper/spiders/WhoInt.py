# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from RISparser import read

class WhoIntSpider(scrapy.Spider):
    name = 'WhoInt'
    allowed_domains = ['www.who.int', 'search.bvsalud.org']
    start_urls = ['https://www.who.int/emergencies/diseases/novel-coronavirus-2019/global-research-on-novel-coronavirus-2019-ncov/']

    def parse(self, response):
        # link para a página de busca
        search_page = response.css('a[aria-label="WHO COVID-19 Database"]::attr(href)').get()
        # parâmetros para baixar os resultados da pesquisa num formato simplificado
        # optou-se por ris ao invés de csv porque em csv os dados são entregues incompletos
        params = {
                'output': 'ris',
                'count': -1,
        }
        download_url = '{}?{}'.format(search_page, urlencode(params))
        self.logger.info('Assembled download url: ' + download_url)

        yield response.follow(download_url, callback = self.parse_file)

    def parse_file(self, response):
        data = self.fix_ris_data(response.text.splitlines())
        for entry in read(data):
            yield entry

    # o leitor de ris precisa que a entrada que finaliza a saída
    # contenha um espaço depois do caracter '-', caso contrário, o
    # arquivo é recusado esta função corrige o output do site
    def fix_ris_data(self, text_lines):
        return list(map(lambda x: x if x != 'ER  -' else 'ER  - ', text_lines))

