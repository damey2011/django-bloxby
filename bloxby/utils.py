import re
import logging
from zipfile import ZipFile

import bs4
import requests
from django.conf import settings
from django.core.files.base import ContentFile

LINK_PATTERN = '(?:https?://)?[\.*?\/?\w+/\-_]{1,}\.[\w+]{2,}'

CSS_LINK_PATTERN = 'url\((?:https?://)?[./]*?[\'"]?[\w+/.]*[?\w+]*[\'"]?\)'

logger = logging.getLogger(__name__)


def replace_links(page):
    from bloxby.models import TemplateAsset, Page
    """Replace the links in the page here"""
    soup = bs4.BeautifulSoup(page.html.read(), 'html.parser')
    css_assets = []
    for link in soup.find_all('link'):
        if link.get('href'):
            # Stylesheets, fonts, favicon
            href = link['href']
            try:
                asset = TemplateAsset.objects.get(initial_path=href, template=page.template)
            except TemplateAsset.DoesNotExist:
                asset = None
            except TemplateAsset.MultipleObjectsReturned:
                asset = TemplateAsset.objects.filter(initial_path=href, template=page.template).first()
            if asset:
                link['href'] = asset.file.url
                if '.css' in href:
                    css_assets.append(asset)
    html_content = soup.prettify()
    # Find all other asset embeddings in the HTML
    links = re.findall(LINK_PATTERN, html_content)
    for link in links:
        initial_link = link
        if '://' in link:
            continue
        search_path = link.replace('../', '')
        search_path = search_path.split('?')[0]
        search_path = search_path.split('#')[0]
        if search_path.endswith('.html'):
            try:
                p = Page.objects.get(template=page.template, name=search_path)
                html_content = html_content.replace(link, p.absolute_url(''))
            except Page.DoesNotExist:
                pass
        else:
            try:
                ta = TemplateAsset.objects.get(template=page.template, initial_path=search_path)
                html_content = html_content.replace(link, ta.file.url)
            except TemplateAsset.DoesNotExist:
                if initial_link.startswith('/'):
                    logger.info(f'Initial link {initial_link} is not found.')
                    continue
                new_link = f'{settings.BLOXBY_BUILDER["url"]}/{initial_link}'
                try:
                    resp = requests.head(new_link)
                    if resp.status_code == 200 and bool(resp.content):
                        html_content = html_content.replace(initial_link, new_link)
                except Exception as e:
                    logger.info(f'Even link {new_link} is not valid.')
                    pass

    name = page.html.name.split('/')[-1]
    page.html.delete()
    page.html.save(name, ContentFile(html_content.encode('utf-8')))

    if css_assets:
        for asset in css_assets:
            css_content = asset.file.read().decode('utf-8')
            links = re.findall(CSS_LINK_PATTERN, css_content)
            for link in links:
                nl = link.replace('../', '').lstrip('url(').rstrip(')').strip('\'').strip('"').strip('.').strip('/')
                nl = nl.split('?')[0]
                try:
                    link_inside = TemplateAsset.objects.get(initial_path=nl, template=asset.template)
                    css_content = css_content.replace(link, f'url({link_inside.file.url})')
                except TemplateAsset.DoesNotExist:
                    print(f'Link {nl} inside css is not registered.')
            name = asset.file.name.split('/')[-1]
            asset.file.delete()
            asset.file.save(name, ContentFile(css_content.encode('utf-8')))


def extract_zip(input_zip):
    input_zip = ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}
