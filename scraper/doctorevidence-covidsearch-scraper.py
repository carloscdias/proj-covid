import scrapy
import json
from csv import DictReader

class DoctorEvidenceCovidSearchScraper(scrapy.Spider):
    name = 'covid-search.doctorevidence'
    start_urls = ['https://covid-search.doctorevidence.com/']
    download_timeout = 999999999999

    def parse(self, response):
        # variável que armazena os dados do usuário
        auth_pattern = r'\bvar\s+userProfile\s*=\s*(\{.*?\})\s*;\n'
        # varável que armazena dos dados de busca exibidos na página
        signals_pattern = r'\bvar\s+signals\s*=\s*(\[\{.*?\}\])\s*;'
        
        # Para fazer o download do conteúdo, precisamos passar um cookie com o
        # token dessa variável
        auth = response.css('script[type="text/javascript"]').re_first(auth_pattern)
        auth_token = json.loads(auth)['auth-token']

        json_data = response.css('script[type="text/javascript"]').re_first(signals_pattern)
        for el in json.loads(json_data):
            query = el['query']['query/normalized-blunt']

            # Download dos dados em csv da query obtida na página de busca
            yield scrapy.Request(
                    url = 'https://covid-search.doctorevidence.com/api/articles/export',
                    method = 'post',
                    body = '["^ ","~:blunt","{}","~:format","csv","~:order","new","~:order-direction","desc","~:limit",1048576]'.format(query),
                    cookies = { '.ASPXAUTHSSO': auth_token },
                    callback = self.parse_file,
                    headers = { 'content-type': 'application/transit+json' },
                    cb_kwargs={ 'title': el['title'] },
            )

    def parse_file(self, response, title):
        yield { title: list(DictReader(response.text)) }

