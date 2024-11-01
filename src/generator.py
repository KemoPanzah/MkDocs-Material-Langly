import re
from pathlib import Path
from mkdocs.utils import log

from .localizer import Localizer

class Generator:
    def __init__(self):
        self.localizer = Localizer()

    def make(self, serve, source_path: Path, dest_path: Path, source_lang, target_lang):
        
        t_md_target = []

        with open(source_path, 'r', encoding='utf-8') as file:
            t_md_source = file.readlines()

        self.localizer.prune_data(dest_path)

        t_content_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')

        for i, line in enumerate(t_md_source):
            t_content_match = t_content_pattern.finditer(line)
            
            if t_content_match:   
                for match in t_content_match:
                    line = line.replace(match.group(0), self.localizer.translate(serve, dest_path, match.group(1), source_lang, target_lang))
            
            t_md_target.append(line)
        
        self.localizer.save_data()
        
        with open(dest_path, 'w', encoding='utf-8') as file:
            file.writelines(t_md_target)
            


                