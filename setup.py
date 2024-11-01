from setuptools import setup, find_packages


setup(
    name='mkdocs-material-langly',
    version='0.1.0',
    description='A language tool for MkDocs Material theme',
    long_description='A language tool for MkDocs Material theme',
    keywords='mkdocs, material, language, translation',
    url='',
    author='Jean Rohark',
    author_email='no@mail',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.0.4',
        'mkdocs-material>=9.5.41'
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