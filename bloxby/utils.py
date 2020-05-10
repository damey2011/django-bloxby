import re

import bs4
from django.core.files.base import ContentFile


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
    # for script in soup.find_all('script'):
    #     if script.get('src'):
    #         src = script['src']
    #         try:
    #             asset = TemplateAsset.objects.get(initial_path=src)
    #             script['src'] = asset.file.url
    #         except TemplateAsset.DoesNotExist:
    #             pass
    # for img in soup.find_all('img'):
    #     if img.get('src'):
    #         src = img['src']
    #         try:
    #             asset = TemplateAsset.objects.get(initial_path=src)
    #             img['src'] = asset.file.url
    #         except TemplateAsset.DoesNotExist:
    #             pass
    #
    # # Fix the inner links
    # for a in soup.find_all('a'):
    #     if a.get('href') and a.get('href') not in ['#', 'javascript:void(0);', 'javascript:;']:
    #         link = a['href']
    #         try:
    #             p = Page.objects.get(name=link)
    #             a['href'] = p.absolute_url()
    #         except Page.DoesNotExist:
    #             pass

    html_content = soup.prettify()
    # Find all other asset embeddings in the HTML
    links = re.findall('[\.*?\/?\w+/\-_]*\.[\w+]{2,}', html_content)
    for link in links:
        if link.endswith('.html'):
            try:
                p = Page.objects.get(template=page.template, name=link)
                html_content = html_content.replace(link, p.absolute_url())
            except Page.DoesNotExist:
                pass
        else:
            try:
                ta = TemplateAsset.objects.get(template=page.template, initial_path=link.replace('../', ''))
                html_content = html_content.replace(link, ta.file.url)
            except TemplateAsset.DoesNotExist:
                pass

    name = page.html.name.split('/')[-1]
    page.html.delete()
    page.html.save(name, ContentFile(html_content.encode('utf-8')))

    if css_assets:
        css_link_pattern = 'url\("?[\.*?\/?\w+/\-_]*\.[\w+]{2,}'
        for asset in css_assets:
            css_content = asset.file.read().decode('utf-8')
            links = re.findall(css_link_pattern, css_content)
            for link in links:
                nl = re.sub('url\("?', '', link).lstrip('../')
                try:
                    link_inside = TemplateAsset.objects.get(initial_path=nl, template=asset.template)
                    css_content = css_content.replace(link, f'url({link_inside.file.url}')
                except TemplateAsset.DoesNotExist:
                    print(f'Link {nl} inside css is not registered.')
            name = asset.file.name.split('/')[-1]
            asset.file.delete()
            asset.file.save(name, ContentFile(css_content.encode('utf-8')))
