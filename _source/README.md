# How this site is built

Every page is generated from the files in this folder. GitHub Pages does not publish folders
whose names start with an underscore, so nothing here appears on the live site.

| File | What it holds |
|---|---|
| `papers.yaml` | One entry per paper: title, authors, venue, links, abstract, plain-language summary, study-at-a-glance table, topics, BibTeX key |
| `topics.yaml` | The seven research topics and their descriptions |
| `home.yaml` | Home page bio, positions, education, media highlights |
| `pages/*.html` | Content of About, Contact, Media, Resources, Data, and Experiments |
| `build.py` | The generator |

## Adding or changing a paper

1. Edit `papers.yaml` (copy an existing entry as a template).
2. From the repository root run `python _source/build.py` (needs `pip install pyyaml`).
3. Commit everything that changed.

The build rewrites every page, `papers.bib`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, and `robots.txt`,
so the site, the citations, and the files AI tools read always agree.
