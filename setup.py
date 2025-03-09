from setuptools import setup, find_packages
from pathlib import Path

t_root = Path(__file__).parent
long_description = (t_root / "README.md").read_text(encoding='utf-8')

setup(
    name='mkdocs-material-langly',
    version='0.1.2',
    description='The Langly plugin for MkDocs is a plugin that provides language support and translations for websites created with MkDocs using the Material theme. It enables easy management of multilingual content and automatic translation of texts to reach a wider audience. It deliberately does not comply with any of the current translation standards, but takes a completely unique but open approach.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='mkdocs, material, language, translation, multi-language, multi-lingual, deepl',
    url='https://www.decore.dev/en/sub/mkdocs_material_langly/',
    author='Kemo Panzah',
    author_email='info@decore.dev',
    license='MIT',
    python_requires='>=3.11.4',
    install_requires=[
        'mkdocs>=1.0.4',
        'mkdocs-material>=9.5.41',
        'markdownify>=0.13.1',
        'beautifulsoup4>=4.12.3',
        'deepl>=1.19.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'langly = src.plugin:Langly'
        ]
    }
)