from django.core.management.base import BaseCommand, CommandError
from politiburo.site_scraper import *

class Command(BaseCommand):
    help = 'Runs the scraper of site content'

    def handle(self, *args, **options):
        site_urls = get_url_list()
        get_site_content(site_urls)
