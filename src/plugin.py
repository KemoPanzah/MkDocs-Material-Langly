import re
import shutil

from jinja2 import Template
from mkdocs.commands.build import build
from mkdocs.utils import log
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.config.defaults import MkDocsConfig
from markdown import markdown as md2html
from pathlib import Path
from markdownify import MarkdownConverter

from .localizer import Localizer

index = """
<!DOCTYPE html>
<html lang="{{ source_lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0; url={{ source_lang }}/">
</head>
</html>
"""

class Langly(BasePlugin):

    config_scheme = (
        ('source', config_options.Type(dict, required=True )),
        ('targets', config_options.Type(list, default=[])),
        # ('delimiter', config_options.Type(str, default='[[,]]')),
        ('lang_switch', config_options.Type(bool, default=True)),
        ('mode', config_options.Type(str, default='manual')),
    )

    def __init__(self):
        self.enabled = True
        self.init = False
        self.serve = False
        
        self.site_url = None
        self.site_dir = None
        self.language_s = []

        self.target_lang_s = []
        self.source_lang = None
        self.target_lang = None

        self.localizer = None
        

    def configure(self, config: MkDocsConfig):
        
        if config['theme']['name'] != 'material':
            log.error('Langly is only compatible with the Material theme.')
            exit(1)

        # Save root values on first run
        if not self.init:
       
            self.site_url = config.site_url
            self.site_dir = config.site_dir

            self.language_s.append(self.config['source']['lang'])
            for target in self.config['targets']:
                self.language_s.append(target['lang'])

            self.create_index(self.config['source']['lang'])
        
            self.init = True

        # Set source and target languages
        self.source_lang = self.config['source']['lang']
        
        if not self.target_lang_s:
            self.target_lang_s = self.target_lang_s + self.language_s

        # Configure the next build
        self.target_lang = self.target_lang_s.pop(0)
        
        config.site_dir = str(Path(self.site_dir).joinpath(self.target_lang[:2]))
        
        if self.site_url:
            config['site_url'] = self.site_url + self.target_lang[:2]

        # Configure material theme
        config.theme['language'] = self.target_lang[:2]

        if self.config['lang_switch']:
            config.extra['alternate'] = []
            t_lang = {'name': self.config['source']['name'], 'lang': self.config['source']['lang'][:2], 'link': f'../{self.config["source"]["lang"][:2]}/'}
            config.extra['alternate'].append(t_lang)
            for target in self.config.data['targets']:
                t_lang = {'name': target['name'], 'lang': target['lang'][:2], 'link': f'../{target["lang"][:2]}/'}
                config.extra['alternate'].append(t_lang)

        t_blog = config.plugins.get('material/blog')
        
        if t_blog:
            t_blog.config.post_url_format = '{date}/{file}'

        return config

    def generate(self, p_content, p_type='html'):
        t_content_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')
        t_content_match = t_content_pattern.finditer(p_content)
        t_content_found_s = t_content_pattern.findall(p_content)
        if t_content_found_s:   
            t_html2md = MarkdownConverter()
            for match in t_content_match:
                t_text = match.group(1)
                if p_type == 'markdown':
                    t_text = md2html(t_text).replace('<p>', '').replace('</p>', '')
                    t_text = self.localizer.translate(self.serve, t_text)
                    t_text = t_html2md.convert(t_text)
                if p_type == 'html':
                    t_text = self.localizer.translate(self.serve, t_text)
                p_content = p_content.replace(match.group(0), t_text)
        return p_content
    
    def create_index(self, p_source_lang):
        t_template = Template(index)
        t_index = t_template.render(source_lang=p_source_lang)
        t_index_path = Path(self.site_dir).joinpath('index.html')
        t_index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(Path(self.site_dir).joinpath('index.html'), 'w') as f:
            f.write(t_index)

    def on_startup(self, command, dirty):
        pass

    def on_config(self, config):
        return self.configure(config)
    
    def on_pre_page(self, page, config, files):
        self.localizer = Localizer(page.file.src_path, self.source_lang, self.target_lang)
        return page

    def on_page_markdown(self, markdown, page, config, files):
        markdown = self.generate(markdown, 'markdown')
        return markdown
    
    def on_page_content(self, html, page, config, files):
        html = self.generate(html, 'html')
        self.localizer.save_data()
        return html

    def on_post_build(self, config):   
        if self.target_lang_s:
            build(config)
        else:
            config.site_url = self.site_url
            config.site_dir = self.site_dir
            
    def on_serve(self, server, config, builder):
        self.serve = True
        return server
    
    def on_shutdown(self):
        if self.serve:
            try:
                shutil.rmtree(self.site_dir)
                log.info(f"Directory {self.site_dir} has been removed.")
            except Exception as e:
                log.error(f"Error removing directory {self.site_dir}: {e}")