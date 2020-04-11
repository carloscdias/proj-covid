# -*- coding: utf-8 -*-
import scrapy


class CovidsearchdoctorevidencespiderSpider(scrapy.Spider):
    name = 'CovidSearchDoctorEvidenceSpider'
    allowed_domains = ['https://covid-search.doctorevidence.com/']
    start_urls = ['http://https://covid-search.doctorevidence.com//']

    def parse(self, response):
        pass
