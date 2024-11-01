import re
import shutil

from mkdocs.commands.build import build
from mkdocs.utils import log
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from pathlib import Path

from .localizer import Localizer


class Langly(BasePlugin):

    config_scheme = (
        ('source', config_options.Type(dict, required=True )),
        ('targets', config_options.Type(list, default=[])),
        ('delimiter', config_options.Type(str, default='[[,]]')),
    )

    def __init__(self):
        self.enabled = True
        self.serve = False
        self.source_lang = None
        self.target_lang_s = []
        self.target_lang = None
        self.site_url = None
        self.site_dir = None

    def generate(self, src_path, markdown):
        t_content_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')
        t_content_match = t_content_pattern.finditer(markdown)
        t_content_found_s = t_content_pattern.findall(markdown)
        if t_content_found_s:   
            t_localizer = Localizer(src_path, self.source_lang, self.target_lang)
            for match in t_content_match:
                markdown = markdown.replace(match.group(0), t_localizer.translate(self.serve, match.group(1)))
            t_localizer.save_data()
        return markdown
    
    def on_startup(self, command, dirty):
        pass

    def on_config(self, config):
        if not self.site_url:
            self.site_url = config['site_url']

        if self.site_dir is None: 
            self.site_dir = config['site_dir']
        
        if not self.source_lang:
            self.source_lang = self.config['source']['lang']
        
        if not self.target_lang_s:
            self.target_lang_s.append(self.source_lang)
            for target in self.config['targets']:
                self.target_lang_s.append(target['lang'])
            
        return config
    
    def on_pre_build(self, config):
        self.target_lang = self.target_lang_s.pop(0)
        config['site_dir'] = str(Path(self.site_dir).joinpath(self.target_lang[:2]))
        config.theme['language'] = self.target_lang[:2]
        if self.site_url:
            config['site_url'] = self.site_url + self.target_lang[:2]
    
    def on_files(self, files, config):
        return files

    def on_pre_page(self, page, config, files):
        if page.title:
            pass
        return page
    
    def on_page_markdown(self, markdown, page, config, files):
        markdown = self.generate(page.file.src_path, markdown)
        return markdown
    
    def on_page_content(self, html, page, config, files):
        return html

    def on_post_build(self, config):   
        if self.target_lang_s:
            build(config)
        else:
            config['site_url'] = self.site_url
            config['site_dir'] = self.site_dir
    
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