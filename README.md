# MKDocs Material Langly Plugin

A MkDocs plugin that does something.

## Work in Progress



## Changelog and Features

### 0.1.0 - Initial Release
  
- Insert an "index.html" with redirection to the target language by browser language.
- Configure MKDocs and the Material Theme for each build in the respective language.
- Optional language switch that is configured automatically.
- Set all open translations to draft mode during serve mode to minimize access to the translation API.
- Also search the page content to find additional translations created with third-party plugins such as mkdocs-strings.
- Save all translations in one JSON file per page to minimize access to the translation api and enable manual changes.
- Converts Markdown to HTML, translates and converts back to get text formatting like `code`, `strong` and `em`.
- Get fixed words in code tags with temporary HTML attributes.
- Navigation translation