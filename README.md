# MkDocs Material Langly Plugin

The Langly plugin for MkDocs is a plugin that provides language support and translations for websites created with MkDocs using the Material theme. It enables easy management of multilingual content and automatic translation of texts to reach a wider audience. It deliberately does not comply with any of the current translation standards, but takes a completely unique but open approach.

This plugin was created to use the great Material theme and offers functionalities to e.g. internationalize the blog area.

**The only translation engine currently available is Deepl and a DeepL api key is required to use the plugin.**

## Directly supported plugins for mkdocs ##

This list includes plugins that were used directly in the development of Langly and are considered compatible.
**But it is not impossible that other plugins will also work.**

- [mkdocs-material](https://squidfunk.github.io/mkdocs-material){:target="_blank"}
- [mkdocs-strings](https://mkdocstrings.github.io){:target="_blank"}
- [mkdocs-glightbox](https://github.com/blueswen/mkdocs-glightbox){:target="_blank"}

These great plugins definitely need full support and recognition.

!!! note
    The plugin is still under development and it is recommended to read the documentation to understand the functionalities and limitations. I also ask you to report all requirements and suggested changes in the GitHub issues.

## Let's get started

To get started, a few preliminary steps are required to use the plugin.

- [x] mkdocs with installed material theme
- [x] A DeepL\-Free\-Account is required

### Installation of the plugin

To use the plugin, you must first install it. To do this, execute the following command:

```bash
pip install mkdocs-material-langly
```

### Provide Api key

To use the plugin, you need a Deepl API key. You can obtain this free of charge from the Deepl website.

After you have created the api key, create a file called `auth_key.json` in the root directory of your project and add the following content:

```json
  {
      "deepl": "DEEPL-API-KEY"
  }

```

Replace `DEEPL-API-KEY` with your own api key.

### Protect Api key

!!! danger
    Please read this section carefully and be sure to exclude the Api key in the .gitignore and also protect it in every possible way from being uploaded to the Internet.

Open the .gitignore file in the root directory and add the line `auth_key.json` to prevent the file from being uploaded by mistake. Then check online that the key cannot be found in the repo.

### Configuration of the plugin

After installation, you can activate the plugin in your `mkdocs.yml`. **Langly should be the last plugin in the list**.

!!! info
    No language\-related settings need to be made in the Material theme. This means that the `theme>language` and `extra>alternate` options are set by the plugin.

```yaml
site_url: https://<example>.com
..
..
..
plugins:
  - search
  - .
  - .
  - langly:
      lang_switch: true
      source:
          name: Deutsch
          lang: de
      targets:
        - name: English
          lang: en-us

```

In this configuration, German is set as the source language and English as the target language. You can add as many target languages as you like. However, this will affect the `serve` performance all the more. The `site_url` option should correspond to the publication address of your website so that the `sitemap` and `canonicals` function correctly.

!!! warning
    It is important to use the Deepl language codes for `source` and `target`. These can be found on the following website: [Deepl Language Codes](https://developers.deepl.com/docs/resources/supported-languages){:target="_blank"}

Once you have made the configuration, you can use the translation functions in your Markdown files.

### Using the plugin

The plugin analyzes Markdown texts and evaluates masked text passages that are enclosed with `{[` and `]}`. These `delimiter` are removed when the page is rendered and the source and target language are displayed correctly on your page. 

Proceed as follows to mask texts

`{[`Your text`]}`

The text within the masking is then automatically translated by Langly.

### A few simple examples

#### Set

`{[`This text represents your source language`]}`

#### Paragraph

`{[`This paragraph contains several sentences in your source language. It is the recommended way of masking text passages and provides Deepl with more context to deliver a better translation.`]}`
#### Enumeration with colon

- `{[`Enumeration`]}`**:**`{[`Value after the colon`]}`

## Changelog und Features

### 0.1.2

- As the algorithm uses the characters `{[` and `]}` as masking for translatable text, these characters cannot be documented directly in the text. Instead, `hints` are used, which are automatically converted to `{[` and `]}` after translation.
- Markdown export on first run of `serve`, `build` or `gh-deploy` for specified pages and languages with defined path.
- Change to pyproject.toml

### 0.1.1 - Initial Release
  
- Insert an "index.html" with redirection to the target language according to the browser language.
- Configure MKDocs and the material theme for each build in the respective language.
- Optional language switching, which is configured automatically.
- Set all open translations to draft mode during `serve` to minimize access to the translation api.
- Browse page content to find additional translations created with third\-party plugins such as `mkdocs-strings`.
- Save all translations in one JSON file per page to minimize access to the translation api and allow manual changes.
- Converts Markdown to HTML, translates and converts back to get text formatting like `code`, `strong` and `em`.
- Get fixe words in code tags with temporary HTML attributes.
- Navigation translation
- Copy the CNAME file required for gh\-deploy to the root directory of the build.
- *REPLACED* - Ignore delimiters (e.g. `{[` and `]}`) within a masking.

## Feedback and support

I am happy to receive any kind of feedback and support.

Thank you for your interest in this plugin!

Have fun translating!