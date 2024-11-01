from pathlib import Path
from mkdocs.utils import log
import shutil

from .generator import Generator


class Filer:
    def __init__(self):
        self.generator = Generator()
    
    def run(self, serve, source_path: Path, dest_path: Path, source_lang, target_lang):
        t_file_s = list(source_path.rglob('*'))
        for file in t_file_s:
            t_relative_path = file.relative_to(source_path)
            t_target_path = dest_path.joinpath(t_relative_path)

            if not t_target_path.exists() or file.stat().st_mtime > t_target_path.stat().st_mtime:
                if file.is_dir():
                    t_target_path.mkdir(parents=True, exist_ok=True)
                else:
                    t_target_path.parent.mkdir(parents=True, exist_ok=True)
                    if t_target_path.suffix == '.md':
                        log.info(f'Generate {file} to {t_target_path}')
                        self.generator.make(serve, file, t_target_path, source_lang, target_lang)
                    else:
                        log.info(f'Copy {file} to {t_target_path}')
                        shutil.copy2(file, t_target_path)
