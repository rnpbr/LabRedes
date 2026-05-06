# Contribute

## :material-tools: Tools

This project was developed using the following tools:

* <a target="_blank" href="https://python-poetry.org/">poetry</a> for dependency management
* <a target="_blank" href="https://github.com/taskipy/taskipy">taskpy</a> for task automation
* <a target="_blank" href="https://www.mkdocs.org/">mkdocs</a> for documentation
* <a target="_blank" href="https://squidfunk.github.io/mkdocs-material/">mkdocs-material</a> for documentation theme
* <a target="_blank" href="https://commitizen-tools.github.io/commitizen/">commitizen</a> for standardizing commit messages

## :fontawesome-solid-user-gear: How to Contribute

First of all, thank you for being part of this project! Your help is very welcome.

To contribute to the project, follow the steps below:

1. Clone the repository to your local machine:

```bash
git clone https://git.rnp.br/redes-abertas/docs.git
```

2. Install project dependencies:

First, install pipx to install poetry, documentation <a target="_blank" href="https://pypa.github.io/pipx/">here</a>

Now, install poetry, which is the project's dependency manager:

```bash
pipx install poetry
```

Now, inside the project folder, install the project dependencies:

```bash
poetry install
```

Done, now you have all the project dependencies installed.

## Folder Structure

The project is organized as follows:

```mermaid
flowchart TD
    A[./] --> B[docs]
    B --> C[pt]
    B --> D[en]
    B --> E[img]
    C --> F[Ferramentas]
    C --> G[Guias]
    C --> H[inventarios]
    C --> I[Laboratórios]
    C --> J[Templates]
```

Where each folder has the following function:

- `docs`: contains the project documentation, written in Markdown.
- `pt`: contains the documentation in Portuguese.
- `en`: contains the documentation in English.
- `img`: contains the images used in the documentation.
- `Ferramentas`: contains the tools that have been tested and documented in the labs.
- `Guias`: contains the configuration guides for the labs and more specific uses of the labs.
- `inventarios`: contains the lab inventories in the Netbox import format.
- `Laboratórios`: contains the labs that have been tested and documented in network topologies.
- `Templates`: contains the Netreplica templates for vendors not yet supported by default.

### :simple-googledocs: docs

The project documentation is written in Markdown and is located in the docs folder. To contribute,
edit the existing Markdown files or create new ones, following the established folder and file structure.
Each file should include a title and a description, making it a page of the documentation.

The folder structure should follow the pattern of the corresponding section name,
with an index.md file for the section's home page. Other necessary pages should also be in Markdown.
The site organization is done automatically by MkDocs.

Example:

``` bash
docs/
    ├── Seção/
    │   ├── index.md
```

## Get Your Hands Dirty

Now that you have the dependencies installed and understand how poetry works, you can start contributing to the code,
following are some tips for contributing to the project as well as using the project's automation and standardization tools.

!!! info "Tip"
    Before you start editing the code, it is important to enter the poetry virtual environment. To do this, run the following command:

!!! warning "Attention"
    After the poetry update of 2025, the `poetry shell` command was transferred to a plugin, to work, run the following command:
    ```bash
    poetry self add poetry-plugin-shell
    ```

```bash
poetry shell
```

### :material-tools: Tools

The project has some automation and standardization tools, such as `taskpy` and `black`, which are used to automate tasks and standardize the code, respectively.
#### :material-translate: Automatic Translation

The `task translate` command is responsible for translating the Markdown files located in the `docs/pt` folder to the **English** language and saving the translations in `docs/en` using the **Gemini 2.0 Flash** model to perform the translation. It ensures that the content is translated accurately without altering the structure of the documentation and keeping all references and links intact.

#### :material-code-tags-check: How to configure and use file translation

The following are instructions for properly configuring the environment and performing translations.

---

#### **Step 1: Obtain the Gemini API Key**

To use the **Gemini** translation model, you need to obtain a free API key. Follow the steps below:

1. Go to <a target="_blank" href="https://aistudio.google.com/apikey">Google AI Studio</a>.
2. Log in to a valid Google account.
3. Click **Create API key**.
4. Copy the generated key to use in the project.

!!! info "Info"
    More about the Google Gemini API implementation can be found in the <a target="_blank" href="https://ai.google.dev/gemini-api/docs/get-started/tutorial?lang=python">Official Documentation</a>.

---

#### **Step 2: Configure the `.env` file**

In the project directory, you will find a file called `.env.example`. It will serve as a template to create your `.env` file containing sensitive settings, such as the API key.

1. Make a copy of the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

2. Open the `.env` file in any text editor and enter the Gemini key:

```
GEMINI_API_KEY=your-key-here
```

Replace `your-key-here` with the key obtained in Step 1.

---

#### **Step 3: Run the translation**

After configuring the API key in the `.env` file, simply run the command below to start the translation:

```bash
poetry run task translate
```

This command will:
- Translate all Markdown files (.md) found in `docs/pt`.
- Create and save the translations in the `docs/en` folder, maintaining the same directory structure as the source folder.

!!! warning "Note"
    The command will ignore files that are already translated and have not been changed.

---

!!! info "Attention"
    - The command **does not translate folder names currently**. Only the content of the files will be translated.
    - All links and internal references in the documentation will be maintained correctly, without unwanted changes.

---

#### **Additional functionality: Change detection**

The script checks if there have been any modifications to the original files before performing a new translation. This ensures that:

* Only files that **have not been translated** or that **have been changed** will have the translation updated.
* Already translated files will remain unchanged if there is no need for translation.

---

!!! info "About the translation"
    The translation uses the **Gemini 2.0 Flash** model, which performs highly accurate and reliable translation. However, as automatic models are subject to error depending on the context, a final review of the translated content is always recommended.

---

#### **Tips for contributing to the translation**

- Edit the original files (in `docs/pt`) whenever you make changes to the documentation.
- After making changes, run the `task translate` command again to update the translated content in English.

With this, the translation of your documentation will always be synchronized with the original language.

#### :material-code-tags-check: Documentation

The project documentation is written in Markdown and is located in the docs folder, following the structure of existing folders, subfolders and files.
where all standardization is recommended by <a target="_blank" href="https://www.mkdocs.org/">mkdocs</a> and <a target="_blank" href="https://squidfunk.github.io/mkdocs-material/">mkdocs-material</a>, so to view the documentation locally, run the following command:

```bash
poetry run task docs
```

!!! info "Tip"
    To contribute to the documentation, you can edit the Markdown files directly or create new files as needed, following the structure of existing folders, subfolders and files.

!!! info "Tip"
    You can use any feature available in mkdocs for customizations, to learn more access the documentation below:

Useful links:

- <a taget="_blank" href="https://squidfunk.github.io/mkdocs-material/reference/admonitions/">mkdocs-admonitions</a>: documentation for admonitions (documentation annotations)
- <a taget="_blank" href="https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#search">mkdocs-emojis</a> : documentation for emojis
- <a taget="_blank" href="https://mermaid.js.org/syntax/flowchart.html">mermaid</a> : documentation for mermaid (markdown flowchart)

#### Commits :material-code-tags-check:

The project uses `commitizen` to standardize commit messages. To create a commit, run the following command:

!!! Warning "Observation"
    You must be inside the poetry virtual environment, if not, run the following command:
     ```bash
     poetry shell
     ```

```bash
poetry run task commit
```

Now just fill in the requested information and the commit will be made in a standardized way. After the commit, you can push to the remote repository.

## I didn't find what I need here

If you haven't found what you need, you can open an <a target="_blank" href="https://git.rnp.br/redes-abertas/docs/-/issues">issue in the project</a> reporting what you can't do or what needs to be better documented.

## Continuous Improvement

This document can be improved by anyone who is interested in improving it. So, feel free to provide more tips to people who also want to contribute :heart:

without altering the structure of the documentation. and without adding anything and not altering the links or references.