import re

import bs4
from django.core.files.base import ContentFile


def replace_links(page):
    from djbloxby.bloxby.models import TemplateAsset, Page
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
    for script in soup.find_all('script'):
        if script.get('src'):
            src = script['src']
            try:
                asset = TemplateAsset.objects.get(initial_path=src)
                script['src'] = asset.file.url
            except TemplateAsset.DoesNotExist:
                pass
    for img in soup.find_all('img'):
        if img.get('src'):
            src = img['src']
            try:
                asset = TemplateAsset.objects.get(initial_path=src)
                img['src'] = asset.file.url
            except TemplateAsset.DoesNotExist:
                pass

    # Fix the inner links
    for a in soup.find_all('a'):
        if a.get('href') and a.get('href') not in ['#', 'javascript:void(0)']:
            link = a['href']
            try:
                p = Page.objects.get(name=link)
                a['href'] = p.absolute_url()
            except Page.DoesNotExist:
                pass

    html_content = soup.prettify()
    # Find all other asset embeddings in the HTML

    name = page.html.name.split('/')[-1]
    page.html.delete()
    page.html.save(name, ContentFile(html_content))

    if css_assets:
        css_link_pattern = 'url\("?[\w+\/\.]*\.[\w+]*'
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
            asset.file.save(name, ContentFile(css_content))
