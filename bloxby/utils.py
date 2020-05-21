import re
from zipfile import ZipFile

import bs4
from django.core.files.base import ContentFile


LINK_PATTERN = '[\.*?\/?\w+/\-_]*\.[\w+]{2,}'


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
                asset = TemplateAsset.objects.get(initial_path=href)
                link['href'] = asset.file.url
                if '.css' in href:
                    css_assets.append(asset)
            except TemplateAsset.DoesNotExist:
                pass

    html_content = soup.prettify()
    # Find all other asset embeddings in the HTML
    links = re.findall(LINK_PATTERN, html_content)
    for link in links:
        search_path = link.replace('../', '')
        search_path = search_path.split('?')[0]
        search_path = search_path.split('#')[0]
        if search_path.endswith('.html'):
            try:
                p = Page.objects.get(template=page.template, name=search_path)
                html_content = html_content.replace(link, p.absolute_url())
            except Page.DoesNotExist:
                pass
        else:
            try:
                ta = TemplateAsset.objects.get(template=page.template, initial_path=search_path)
                html_content = html_content.replace(link, ta.file.url)
            except TemplateAsset.DoesNotExist:
                pass

    name = page.html.name.split('/')[-1]
    page.html.delete()
    page.html.save(name, ContentFile(html_content.encode('utf-8')))

    if css_assets:
        for asset in css_assets:
            css_content = asset.file.read().decode('utf-8')
            links = re.findall(LINK_PATTERN, css_content)
            for link in links:
                nl = link.replace('../', '')
                try:
                    link_inside = TemplateAsset.objects.get(initial_path=nl, template=asset.template)
                    css_content = css_content.replace(link, link_inside.file.url)
                except TemplateAsset.DoesNotExist:
                    print(f'Link {nl} inside css is not registered.')
            name = asset.file.name.split('/')[-1]
            asset.file.delete()
            asset.file.save(name, ContentFile(css_content.encode('utf-8')))


def extract_zip(input_zip):
    input_zip = ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}
