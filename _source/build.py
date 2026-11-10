#!/usr/bin/env python3
"""Build rawleyheimer.com from the files in _source/.

Run from the repository root:   python _source/build.py
Requires Python 3.8+ and PyYAML (pip install pyyaml).

Inputs  _source/papers.yaml   one entry per paper (the only file to edit when adding a paper)
        _source/topics.yaml   research topics
        _source/home.yaml     home page text, positions, media highlights
        _source/pages/*.html  About, Contact, Media, Resources, Data, Experiments (content only)
Outputs every .html page, papers.bib, llms.txt, llms-full.txt, sitemap.xml, robots.txt
"""
import html, json, re, sys
from pathlib import Path
import yaml

SRC = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SRC.parent
BASE = 'https://rawleyheimer.com'
UPDATED, UPDATED_ISO = 'November 2026', '2026-11-09'
ME = 'Rawley Z. Heimer'
EMAIL = 'rawley.heimer@asu.edu'
CV = 'Heimer_CV.pdf'
PROFILES = {
    'Google Scholar': 'https://scholar.google.com/citations?user=4D_V_kkAAAAJ',
    'SSRN': 'https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=1805935',
    'ASU profile': 'https://search.asu.edu/profile/4304866',
    'RePEc': 'https://authors.repec.org/pro/phe481',
    'Becker Friedman Institute': 'https://bfi.uchicago.edu/scholar/rawley-heimer/',
}
NAV = [('Research', 'research.html'), ('Media', 'media.html'), ('Resources', 'resources.html'),
       ('About', 'about.html'), ('Contact', 'contact.html')]

papers = yaml.safe_load((SRC / 'papers.yaml').read_text(encoding='utf-8'))
topics = yaml.safe_load((SRC / 'topics.yaml').read_text(encoding='utf-8'))
home = yaml.safe_load((SRC / 'home.yaml').read_text(encoding='utf-8'))
papers.sort(key=lambda p: p['order'])
T = {t['slug']: t for t in topics}
PAPER = {p['slug']: p for p in papers}
for p in papers:
    for t in p['topics']:
        assert t in T, f"{p['slug']}: unknown topic {t}"
written = []

# ---------------------------------------------------------------- helpers
def esc(s): return html.escape(str(s), quote=True)

def names(lst):
    lst = list(lst)
    if len(lst) <= 1: return ''.join(lst)
    if len(lst) == 2: return f'{lst[0]} and {lst[1]}'
    return ', '.join(lst[:-1]) + ', and ' + lst[-1]

def last_first(n):
    parts = n.split(' ')
    return parts[-1] + ', ' + ' '.join(parts[:-1])

def surnames(p):
    s = [a.split(' ')[-1] for a in p['authors']]
    return s[0] + ' et al.' if len(s) > 3 else names(s)

def coauthors(p): return [a for a in p['authors'] if a != ME]

def group(p):
    if p['kind'] == 'working': return 'working'
    if p['kind'] in ('guide', 'policy'): return 'other'
    return 'published'

GROUPS = [('published', 'Published papers'), ('working', 'Working papers'), ('other', 'Guides and policy writing')]

def url(path): return BASE + '/' + path

SITE_HOSTS = ('https://rawleyheimer.com', 'http://rawleyheimer.com', 'https://www.rawleyheimer.com')
def new_tab(doc):
    """Links to other sites and to the CV open in a new tab."""
    def fix(m):
        tag, href = m.group(0), m.group(1)
        external = href.startswith(('http://', 'https://')) and not href.startswith(SITE_HOSTS)
        if (external or href.endswith(CV)) and 'target=' not in tag:
            return tag[:-1] + ' target="_blank" rel="noopener">'
        return tag
    return re.sub(r'<a\b[^>]*?\bhref="([^"]+)"[^>]*>', fix, doc)

def write(path, text):
    if path.endswith('.html'): text = new_tab(text)
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding='utf-8')
    written.append(path)

def venue_short(p):
    k = p['kind']
    if k == 'article': return f"<i>{esc(p['journal'])}</i>"
    if k == 'chapter': return f"Chapter in <i>{esc(p['booktitle'])}</i>"
    if k == 'encyclopedia': return f"<i>{esc(p['booktitle'])}</i>, forthcoming"
    if k == 'wp_series': return f"{esc(p['institution'])} {esc(p['series'])} {esc(p['number'])}"
    if k == 'working': return 'Draft available on request' if p.get('request') else 'Working paper'
    if k == 'guide': return 'Research guide'
    if k == 'policy': return f"<i>{esc(p['outlet'])}</i>, {esc(p['publisher'])}"
    return ''

def venue_line(p):
    """Line above the title on a paper page. Deliberately carries no year."""
    k = p['kind']
    if k == 'article':
        return f"<i>{esc(p['journal'])}</i> {esc(p['volume'])} ({esc(p['issue'])}): {esc(p['pages'])}"
    if k == 'chapter':
        return (f"Chapter in <i>{esc(p['booktitle'])}</i>, edited by {esc(names(p['editors']))}, "
                f"{esc(p['publisher'])}")
    if k == 'encyclopedia': return f"<i>{esc(p['booktitle'])}</i>, forthcoming"
    if k == 'wp_series': return f"{esc(p['institution'])} {esc(p['series'])} {esc(p['number'])}"
    if k == 'working': return 'Working paper, draft available on request' if p.get('request') else 'Working paper'
    if k == 'guide': return 'Research guide'
    if k == 'policy':
        num = f" {esc(p['number'])}" if p.get('number') else ''
        return f"<i>{esc(p['outlet'])}</i>{num}, {esc(p['publisher'])}"
    return ''

def entry_lines(p):
    """Coauthors on one line, outlet on the next. Working papers and guides already sit under
    their own headings, so they get no outlet line (unless the draft is available on request)."""
    out = []
    co = coauthors(p)
    if co: out.append(f'  <p class="entry-authors">With {esc(names(co))}</p>')
    if p['kind'] == 'working':
        venue = 'Draft available on request' if p.get('request') else ''
    elif p['kind'] == 'guide':
        venue = ''
    else:
        venue = venue_short(p)
    if venue: out.append(f'  <p class="entry-venue">{venue}</p>')
    return out

def citation(p):
    """Chicago author-date style."""
    a = p['authors']
    who = last_first(a[0]) if len(a) == 1 else (
        last_first(a[0]) + (', and ' if len(a) == 2 else ', ') +
        (', '.join(a[1:-1]) + ', and ' if len(a) > 2 else '') + a[-1])
    # Working papers and guides carry no year in the displayed citation (the BibTeX keeps it).
    undated = p['kind'] in ('working', 'guide')
    yr = 'Forthcoming' if p['status'] == 'forthcoming' else p['year']
    t = esc(p['title']); end = '' if t.endswith('?') else '.'
    s = f"{esc(who)}. “{t}{end}” " if undated else f"{esc(who)}. {yr}. “{t}{end}” "
    k = p['kind']
    if k == 'article':
        s += f"<i>{esc(p['journal'])}</i> {esc(p['volume'])} ({esc(p['issue'])}): {esc(p['pages'])}."
    elif k == 'chapter':
        s += f"In <i>{esc(p['booktitle'])}</i>, edited by {esc(names(p['editors']))}. {esc(p['publisher'])}."
    elif k == 'encyclopedia':
        s += f"<i>{esc(p['booktitle'])}</i>. {esc(p['publisher'])}."
    elif k == 'wp_series':
        s += f"{esc(p['series'])} {esc(p['number'])}, {esc(p['institution'])}."
    elif k == 'policy':
        s += f"<i>{esc(p['outlet'])}</i>{' ' + esc(p['number']) if p.get('number') else ''}, {esc(p['publisher'])}."
    elif k == 'guide':
        s += 'Research guide.'
    else:
        s += 'Working paper.'
    if p.get('doi'): s += f" https://doi.org/{esc(p['doi'])}."
    return s

# ---------------------------------------------------------------- BibTeX
TEX = {'’': "'", '‘': "'", '“': '``', '”': "''", '–': '--', '—': '---', 'á': "{\\'a}", 'é': "{\\'e}",
       'ï': '{\\"i}', 'ø': '{\\o}', '$': '\\$', '&': '\\&', '%': '\\%'}
PROTECT = ['YOLO', 'AI', 'REITs', 'U.S.', 'COVID-19', 'NYSE']
def tex(s):
    return ''.join(TEX.get(c, c) for c in s)
def tex_title(s):
    s = tex(s)
    for w in PROTECT: s = re.sub(r'(?<![{\w])' + re.escape(w) + r'(?![\w}])', '{' + w + '}', s)
    return s
MONTHS = {'1': 'jan', '2': 'feb', '3': 'mar', '4': 'apr', '5': 'may', '6': 'jun', '7': 'jul', '8': 'aug',
          '9': 'sep', '10': 'oct', '11': 'nov', '12': 'dec'}

def bibtex(p):
    k = p['kind']; f = []
    f.append(('author', ' and '.join(tex(last_first(a)) for a in p['authors'])))
    f.append(('title', tex_title(p['title'])))
    page_url = url(f"papers/{p['slug']}.html")
    link = p['links'][0]['url'] if p['links'] else page_url
    if k == 'article':
        typ = 'article'
        f += [('journal', p['journal']), ('volume', p['volume']), ('number', p['issue']),
              ('pages', tex(p['pages'])), ('year', p['year'])]
    elif k in ('chapter', 'encyclopedia'):
        typ = 'incollection'
        f.append(('booktitle', tex(p['booktitle'])))
        if p.get('editors'): f.append(('editor', ' and '.join(tex(last_first(e)) for e in p['editors'])))
        f += [('publisher', p['publisher']), ('year', 'Forthcoming' if p['status'] == 'forthcoming' else p['year'])]
        if p.get('month'): f.append(('month', MONTHS[str(p['month'])]))
        if p.get('isbn'): f.append(('isbn', p['isbn']))
    elif k == 'wp_series':
        typ = 'techreport'
        f += [('institution', p['institution']), ('type', p['series']), ('number', p['number']), ('year', p['year'])]
    elif k == 'policy' and p.get('number'):
        typ = 'techreport'
        f += [('institution', p['publisher']), ('type', p['outlet']), ('number', p['number']), ('year', p['year'])]
    elif k == 'policy':
        typ = 'misc'
        f += [('howpublished', f"{p['outlet']}, {p['publisher']}"), ('year', p['year'])]
        if p.get('month'): f.append(('month', MONTHS[str(p['month'])]))
    else:
        typ = 'unpublished'
        f += [('note', 'Research guide' if k == 'guide' else 'Working paper'), ('year', p['year'])]
    if p.get('doi'): f.append(('doi', p['doi']))
    f.append(('url', link))
    w = max(len(n) for n, _ in f)
    body = ',\n'.join(f"  {n.ljust(w)} = {v}" if n == 'month' else f"  {n.ljust(w)} = {{{v}}}" for n, v in f)
    return f"@{typ}{{{p['bibkey']},\n{body}\n}}"

# ---------------------------------------------------------------- page frame
def head(title, desc, path, depth, meta='', ld=None, og='website'):
    r = '../' * depth
    can = BASE + '/' + ('' if path == 'index.html' else path)
    out = [f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           f'<title>{esc(title)}</title>',
           f'<meta name="description" content="{esc(desc)}">',
           f'<meta name="author" content="{ME}">',
           f'<link rel="canonical" href="{can}">',
           f'<meta property="og:type" content="{og}">',
           f'<meta property="og:title" content="{esc(title)}">',
           f'<meta property="og:description" content="{esc(desc)}">',
           f'<meta property="og:url" content="{can}">',
           f'<meta property="og:site_name" content="{ME}">',
           '<meta name="twitter:card" content="summary">',
           f'<link rel="preload" href="{r}assets/fonts/stix-two-text.woff2" as="font" type="font/woff2" crossorigin>',
           f'<link rel="stylesheet" href="{r}assets/site.css">',
           f'<link rel="alternate" type="text/plain" title="Summary for AI tools" href="{r}llms.txt">']
    if meta: out.append(meta)
    for block in (ld or []):
        out.append('<script type="application/ld+json">\n' + json.dumps(block, ensure_ascii=False, indent=1) + '\n</script>')
    out.append('</head>')
    return '\n'.join(out)

def nav_list(depth, active):
    r = '../' * depth
    cur = ' aria-current="page"'
    return '<ul class="nav-list">' + ''.join(
        f'<li><a href="{r}{h}"{cur if n == active else ""}>{n}</a></li>' for n, h in NAV) + '</ul>'

def page(path, depth, title, desc, body, active=None, meta='', ld=None, og='website', wide=False, scripts=()):
    r = '../' * depth
    hdr = (f'<header class="site-head">\n<div class="site-head-inner">\n'
           f'<a class="site-name" href="{r}index.html">{ME}</a>\n'
           f'<nav class="nav-wide" aria-label="Site">{nav_list(depth, active)}</nav>\n'
           f'<details class="nav-narrow"><summary>Menu</summary><nav aria-label="Site">{nav_list(depth, active)}</nav></details>\n'
           f'</div>\n</header>')
    foot = (f'<footer class="site-foot"><span>{ME}, W. P. Carey School of Business, Arizona State University</span>'
            f'<span>Updated {UPDATED}</span></footer>')
    scr = ''.join(f'\n<script src="{r}{s}" defer></script>' for s in scripts)
    doc = (head(title, desc, path, depth, meta, ld, og) +
           '\n<body' + (' class="wide-page"' if wide else '') + '>\n<a class="skip" href="#main">Skip to content</a>\n'
           + hdr + '\n' + body + '\n' + foot + scr + '\n</body>\n</html>\n')
    write(path, doc)

PERSON_REF = {'@type': 'Person', '@id': BASE + '/#rawley-heimer', 'name': ME, 'url': BASE + '/'}
PERSON = {**PERSON_REF, 'givenName': 'Rawley', 'familyName': 'Heimer',
          'jobTitle': 'Associate Professor of Finance', 'email': 'mailto:' + EMAIL,
          'image': BASE + '/assets/img/rawley-heimer.jpg',
          'affiliation': {'@type': 'CollegeOrUniversity', 'name': 'W. P. Carey School of Business, Arizona State University',
                          'url': 'https://wpcarey.asu.edu'},
          'alumniOf': [{'@type': 'CollegeOrUniversity', 'name': 'Brandeis University'},
                       {'@type': 'CollegeOrUniversity', 'name': 'University of Rochester'}],
          'knowsAbout': [t['name'] for t in topics] + ['Household finance', 'Litigation economics'],
          'sameAs': list(PROFILES.values())}

def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': url(h)} for i, (n, h) in enumerate(items)]}

# ---------------------------------------------------------------- listings
def entry(p, depth, finding=True, note=False):
    r = '../' * depth
    out = [f'<li>\n  <p class="entry-title"><a href="{r}papers/{p["slug"]}.html">{esc(p["title"])}</a></p>']
    out += entry_lines(p)
    if note:
        extras = (p.get('notes') or []) + (p.get('awards') or [])
        if extras: out.append(f'  <p class="entry-note">{esc(". ".join(extras))}.</p>')
    if finding: out.append(f'  <p class="entry-finding">{esc(p["finding"])}</p>')
    return '\n'.join(out) + '\n</li>'

def grouped(plist, depth, heading_tag='h2'):
    out = []
    for g, label in GROUPS:
        sub = [p for p in plist if group(p) == g]
        if not sub: continue
        out.append(f'<{heading_tag} class="sec">{label}</{heading_tag}>\n<ol class="entries">\n' +
                   '\n'.join(entry(p, depth) for p in sub) + '\n</ol>')
    return '\n'.join(out)

def topic_papers(slug): return [p for p in papers if slug in p['topics']]

def contents(depth):
    r = '../' * depth
    items = []
    for t in topics:
        items.append(f'<li><p><a class="ct" href="{r}topics/{t["slug"]}.html">{esc(t["name"])}</a></p>'
                     f'<p class="cd">{esc(t["intro"])}</p></li>')
    return '<ul class="contents">\n' + '\n'.join(items) + '\n</ul>'

# ---------------------------------------------------------------- paper pages
def glance_table(p):
    g = p.get('glance')
    if not g: return ''
    rows = ['<tr class="panel"><th colspan="3" scope="colgroup">Panel A. Design</th></tr>']
    for k, v in g['design']:
        rows.append(f'<tr><th scope="row">{esc(k)}</th><td colspan="2">{esc(v)}</td></tr>')
    rows.append(f'<tr class="panel"><th colspan="3" scope="colgroup">Panel B. {esc(g["effects_title"])}</th></tr>')
    for k, v in g['effects']:
        k = f'Fact {k}' if str(k).isdigit() else k
        if g.get('numeric'):
            rows.append(f'<tr><th scope="row" colspan="2">{esc(k)}</th><td class="num">{esc(v)}</td></tr>')
        else:
            rows.append(f'<tr><th scope="row">{esc(k)}</th><td colspan="2">{esc(v)}</td></tr>')
    return ('<section class="body-sec">\n<table class="glance">\n<caption><b>Table 1.</b> Study at a glance</caption>\n<tbody>\n'
            + '\n'.join(rows) + '\n</tbody>\n</table>\n<p class="table-note">Summarized from the paper. '
            'See the paper for exact estimates and specifications.</p>\n</section>')

def related(p):
    pool = []
    for t in p['topics']:
        for q in topic_papers(t):
            if q['slug'] != p['slug'] and q not in pool: pool.append(q)
    return pool[:4]

def paper_meta(p, page_url):
    m = [('citation_title', p['title'])]
    m += [('citation_author', last_first(a)) for a in p['authors']]
    m.append(('citation_publication_date', p['year']))
    k = p['kind']
    if k == 'article':
        m += [('citation_journal_title', p['journal']), ('citation_volume', p['volume']), ('citation_issue', p['issue'])]
        fp, _, lp = p['pages'].partition('–')
        m += [('citation_firstpage', fp), ('citation_lastpage', lp)]
    elif k in ('chapter', 'encyclopedia'):
        m += [('citation_inbook_title', p['booktitle']), ('citation_publisher', p['publisher'])]
        if p.get('isbn'): m.append(('citation_isbn', p['isbn']))
    elif k == 'wp_series':
        m += [('citation_technical_report_institution', p['institution']), ('citation_technical_report_number', p['number'])]
    elif k == 'policy':
        m.append(('citation_publisher', p['publisher']))
    if p.get('doi'): m.append(('citation_doi', p['doi']))
    m += [('citation_abstract_html_url', page_url), ('citation_language', 'en'),
          ('citation_keywords', '; '.join(x.strip() for x in p['keywords'].split(',')))]
    return '\n'.join(f'<meta name="{n}" content="{esc(v)}">' for n, v in m)

def paper_ld(p, page_url):
    status = {'published': 'Published', 'forthcoming': 'Forthcoming', 'working': 'Working paper',
              'unposted': 'Working paper (draft available on request)'}[p['status']]
    a = {'@context': 'https://schema.org', '@type': 'ScholarlyArticle', '@id': page_url + '#paper',
         'url': page_url, 'mainEntityOfPage': page_url, 'name': p['title'], 'headline': p['title'],
         'author': [PERSON_REF if n == ME else {'@type': 'Person', 'name': n} for n in p['authors']],
         'datePublished': str(p['date']), 'dateModified': UPDATED_ISO, 'creativeWorkStatus': status,
         'abstract': p['abstract'], 'description': p['lead'] + ' ' + p['brief'],
         'keywords': p['keywords'], 'inLanguage': 'en',
         'about': [{'@type': 'Thing', 'name': T[t]['name']} for t in p['topics']]}
    k = p['kind']
    if k == 'article':
        a['isPartOf'] = {'@type': 'PublicationIssue', 'issueNumber': p['issue'], 'isPartOf': {
            '@type': 'PublicationVolume', 'volumeNumber': p['volume'],
            'isPartOf': {'@type': 'Periodical', 'name': p['journal']}}}
        a['pagination'] = p['pages'].replace('–', '-')
    elif k in ('chapter', 'encyclopedia'):
        a['isPartOf'] = {'@type': 'Book', 'name': p['booktitle'], 'publisher': {'@type': 'Organization', 'name': p['publisher']}}
        if p.get('isbn'): a['isPartOf']['isbn'] = p['isbn']
        if p.get('editors'): a['isPartOf']['editor'] = [{'@type': 'Person', 'name': e} for e in p['editors']]
    elif k in ('wp_series', 'policy'):
        a['publisher'] = {'@type': 'Organization', 'name': p.get('institution') or p.get('publisher')}
    same = []
    if p.get('doi'):
        a['identifier'] = {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': p['doi']}
        same.append('https://doi.org/' + p['doi'])
    same += [l['url'] for l in p['links']]
    if same: a['sameAs'] = same
    if p.get('awards'): a['award'] = p['awards']
    if p.get('jel'): a['keywords'] += ', JEL ' + p['jel']
    return a

def paper_page(p):
    path = f"papers/{p['slug']}.html"; page_url = url(path); prim = T[p['topics'][0]]
    notes = (p.get('notes') or []) + (p.get('awards') or [])
    if p['links']:
        links = '<ul class="links">' + ''.join(
            f'<li><a href="{esc(l["url"])}">{esc(l["label"])}</a>, {esc(l["source"])}</li>' for l in p['links'])
        if p.get('doi'): links += f'<li>DOI: <a href="https://doi.org/{esc(p["doi"])}">{esc(p["doi"])}</a></li>'
        links += '</ul>'
    else:
        subj = esc('Draft request: ' + p['title'])
        links = (f'<p class="request">The draft is not yet posted. <a href="mailto:{EMAIL}?subject={subj}">'
                 f'Email for a copy</a>.</p>')
    rel = ''.join(f'<dd><a href="{q["slug"]}.html">{esc(q["title"])}</a></dd>' for q in related(p))
    tlinks = '; '.join(f'<a href="../topics/{t}.html">{esc(T[t]["name"])}</a>' for t in p['topics'])
    body = f'''<main id="main" class="wrap">
<p class="crumbs"><a href="../research.html">Research</a> › <a href="../topics/{prim["slug"]}.html">{esc(prim["name"])}</a></p>
<article>
<header class="title-block">
<p class="journal-line">{venue_line(p)}</p>
<h1 class="paper-title">{esc(p["title"])}</h1>
<p class="paper-authors">{esc(names(p["authors"]))}</p>
{f'<p class="paper-notes">{esc(". ".join(notes))}.</p>' if notes else ''}
</header>
<p class="abstract"><b>Abstract.</b> {esc(p["abstract"])}</p>
<p class="keywords"><i>Keywords:</i> {esc(p["keywords"])}.</p>
{f'<p class="keywords"><i>JEL codes:</i> {esc(p["jel"])}.</p>' if p.get("jel") else ''}
<hr class="front-end">
<section class="body-sec">
<h2>In brief</h2>
<p class="lead">{esc(p["lead"])}</p>
<p>{esc(p["brief"])}</p>
</section>
{glance_table(p)}
<section class="body-sec">
<h2>Read and cite</h2>
{links}
<p class="citation">{citation(p)}</p>
<pre class="bib" data-bib>{esc(bibtex(p))}</pre>
</section>
<section class="body-sec">
<h2>Related</h2>
<dl class="rel"><dt>Topics</dt><dd>{tlinks}</dd>{"<dt>Related papers</dt>" + rel if rel else ""}</dl>
</section>
</article>
</main>'''
    title = f"{p['title']} | {surnames(p)}"
    desc = p['lead'] if len(p['lead']) < 300 else p['lead'][:297] + '…'
    ld = [paper_ld(p, page_url), crumbs_ld([('Research', 'research.html'), (prim['name'], f"topics/{prim['slug']}.html"),
                                           (p['title'], path)])]
    page(path, 1, title, desc, body, active='Research', meta=paper_meta(p, page_url), ld=ld, og='article',
         scripts=['assets/site.js'])

# ---------------------------------------------------------------- topic pages
def topic_page(t):
    path = f"topics/{t['slug']}.html"
    plist = topic_papers(t['slug'])
    others = ''.join(f'<li><a href="{o["slug"]}.html">{esc(o["name"])}</a></li>' for o in topics if o is not t)
    body = f'''<main id="main" class="wrap">
<p class="crumbs"><a href="../research.html">Research</a> › {esc(t["name"])}</p>
<h1 class="page-title">{esc(t["name"])}</h1>
<p class="intro">{esc(t["intro"])}</p>
<p class="terms"><i>Related terms:</i> {esc(t["terms"])}.</p>
{grouped(plist, 1)}
<h2 class="sec">Other research topics</h2>
<ul class="see-also">{others}</ul>
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', '@id': url(path), 'url': url(path),
           'name': f"{t['name']}: research by {ME}", 'description': t['intro'],
           'about': {'@type': 'DefinedTerm', 'name': t['name']}, 'author': PERSON_REF,
           'hasPart': [{'@type': 'ScholarlyArticle', 'name': p['title'], 'url': url(f"papers/{p['slug']}.html")} for p in plist]},
          crumbs_ld([('Research', 'research.html'), (t['name'], path)])]
    page(path, 1, f"{t['name']} | Research by {ME}", t['intro'], body, active='Research', ld=ld)

# ---------------------------------------------------------------- index pages
def research_page():
    body = f'''<main id="main" class="wrap">
<h1 class="page-title" style="margin-top:2.75rem">Research</h1>
<p class="intro">My research spans household finance, behavioral economics, consumer credit, and financial institutions. I use high-quality microeconomic data, such as credit bureau records, brokerage accounts, and administrative datasets, to study how individuals and institutions make financial decisions and what the consequences are for welfare and policy.</p>
<h2 class="sec">Research topics</h2>
{contents(0)}
{grouped(papers, 0)}
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'url': url('research.html'),
           'name': f'Research by {ME}', 'author': PERSON_REF,
           'hasPart': [{'@type': 'ScholarlyArticle', 'name': p['title'], 'url': url(f"papers/{p['slug']}.html")} for p in papers]}]
    page('research.html', 0, f'Research | {ME}',
         'Research by Rawley Z. Heimer on household finance, retail investing, consumer credit, mortgage lending, consumer protection, and saving and retirement, organized by topic.',
         body, active='Research', ld=ld)

def list_page(path, h1, desc, plist, extra=''):
    body = f'''<main id="main" class="wrap">
<p class="crumbs"><a href="research.html">Research</a> › {esc(h1)}</p>
<h1 class="page-title">{esc(h1)}</h1>
{extra}
{grouped(plist, 0)}
</main>'''
    page(path, 0, f'{h1} | {ME}', desc, body, active='Research')

def home_page():
    sel = [p for p in papers if p.get('selected')]
    wps = [p for p in papers if p['kind'] == 'working']
    pos = ''.join(f'<li><span><span class="ttl">{esc(a)}</span>, <span class="org">{b}</span></span><span class="yrs">{esc(c)}</span></li>'
                  for a, b, c in home['positions'])
    edu = ''.join(f'<li><span><span class="ttl">{esc(a)}</span>, <span class="org">{esc(b)}</span></span><span class="yrs">{esc(c)}</span></li>'
                  for a, b, c in home['education'])
    med = ''.join(f'<li><i>{esc(o)}</i>: <a href="{esc(u)}">{esc(h)}</a></li>' for o, h, u in home['media'])
    about = '\n'.join(f'<p>{x}</p>' for x in home['about'])
    links = (f'<a href="{PROFILES["Google Scholar"]}">Google Scholar</a><a href="{PROFILES["SSRN"]}">SSRN</a>'
             f'<a href="{CV}">CV</a><a href="mailto:{EMAIL}">{EMAIL}</a>')
    body = f'''<main id="main" class="wrap">
<header class="masthead">
<img src="assets/img/rawley-heimer.jpg" alt="Portrait of Rawley Z. Heimer" width="335" height="400">
<div>
<h1 class="page-title">{ME}</h1>
<p class="role">Associate Professor of Finance<br><i>W. P. Carey School of Business, Arizona State University</i></p>
<p class="profile-links">{links}</p>
</div>
</header>
<h2 class="sec">About</h2>
<div class="prose">
{about}
</div>
<h2 class="sec">Research by topic</h2>
{contents(0)}
<h2 class="sec">Selected publications</h2>
<ol class="entries">
{chr(10).join(entry(p, 0, finding=False, note=True) for p in sel)}
</ol>
<p class="more"><a href="publications.html">All publications</a></p>
<h2 class="sec">Working papers</h2>
<ol class="entries">
{chr(10).join(entry(p, 0, finding=False) for p in wps)}
</ol>
<p class="more"><a href="working-papers.html">Working papers with summaries</a></p>
<h2 class="sec">Positions and affiliations</h2>
<ul class="cv-list">{pos}</ul>
<h2 class="sec">Education</h2>
<ul class="cv-list">{edu}</ul>
<h2 class="sec">In the media</h2>
<ul class="press-list">{med}</ul>
<p class="more"><a href="media.html">All media coverage</a></p>
</main>'''
    site = {'@context': 'https://schema.org', '@type': 'WebSite', 'url': BASE + '/', 'name': ME, 'author': PERSON_REF}
    page('index.html', 0, f'{ME} | Associate Professor of Finance, Arizona State University',
         'Rawley Z. Heimer is an Associate Professor of Finance at Arizona State University. His research covers household finance, retail investing, consumer credit, mortgage lending, consumer protection, and saving and retirement.',
         body, active=None, ld=[{'@context': 'https://schema.org', **PERSON}, site])

# ---------------------------------------------------------------- carried-over pages
def fragment_pages():
    for f in sorted((SRC / 'pages').glob('*.html')):
        raw = f.read_text(encoding='utf-8')
        m = re.match(r'<!--FRONT\n(.*?)\nFRONT-->\n', raw, re.S)
        fm = json.loads(m.group(1)); content = raw[m.end():].replace('{{root}}', '')
        name = f.stem
        cr = ''.join(f'<a href="{h}">{esc(n)}</a> › ' for n, h in fm['crumbs'])
        crumbs = f'<p class="crumbs">{cr}{esc(fm["h1"])}</p>' if fm['crumbs'] else '<div style="height:2.75rem"></div>'
        intro = f'<p class="intro">{fm["intro"]}</p>' if fm['intro'] else ''
        body = (f'<main id="main" class="wrap{" wide" if fm.get("wide") else ""}">\n{crumbs}\n'
                f'<h1 class="page-title">{esc(fm["h1"])}</h1>\n{intro}\n{content}</main>')
        active = {'about': 'About', 'contact': 'Contact', 'media': 'Media', 'resources': 'Resources',
                  'data': 'Resources', 'experiments': 'Resources'}.get(name)
        ld = fm.get('jsonld') or []
        if name == 'about': ld = [{'@context': 'https://schema.org', **PERSON}]
        scripts = [fm['script']] if fm.get('script') else []
        page(f'{name}.html', 0, fm['title'], fm['description'], body, active=active, ld=ld,
             wide=fm.get('wide', False), scripts=scripts)

# ---------------------------------------------------------------- redirects and machine-readable files
def redirect(old, new):
    target = url(new); rel = '../' * old.count('/') + new
    write(old, f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Page moved</title>
<link rel="canonical" href="{target}"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={rel}"></head>
<body><p>This page has moved to <a href="{rel}">{target}</a>.</p></body></html>
''')

def text_files():
    bib = (f'% Citations for every paper by {ME}, generated from {BASE}/research.html\n'
           f'% Updated {UPDATED}. Citation keys are stable; author order follows the published versions.\n\n')
    write('papers.bib', bib + '\n\n'.join(bibtex(p) for p in papers) + '\n')

    def line(p):
        who = names(p['authors']); yr = 'forthcoming' if p['status'] == 'forthcoming' else p['year']
        v = re.sub(r'<[^>]+>', '', venue_short(p)).replace(', forthcoming', '')
        return f"- [{p['title']}]({url('papers/' + p['slug'] + '.html')}): {who} ({yr}). {v}. {p['finding']}"
    out = [f'# {ME}', '',
           f'> Associate Professor of Finance at the W. P. Carey School of Business, Arizona State University. '
           f'Research on household finance, retail investing and brokerage, consumer credit, mortgage lending, '
           f'consumer protection and financial regulation, and saving, retirement, and inheritance. Each paper '
           f'below links to a page with the full abstract, a plain-language summary, a study-at-a-glance table '
           f'(question, setting, data, method, main findings), and citation data.', '',
           f'Contact: {EMAIL}. Former Senior Advisor for Research and Policy at the Consumer Financial Protection '
           f'Bureau and research economist at the Federal Reserve Bank of Cleveland.', '', '## Research topics', '']
    out += [f"- [{t['name']}]({url('topics/' + t['slug'] + '.html')}): {t['intro']}" for t in topics]
    for g, label in GROUPS:
        out += ['', f'## {label}', ''] + [line(p) for p in papers if group(p) == g]
    out += ['', '## Optional', '', f'- [All abstracts and summaries in one file]({url("llms-full.txt")})',
            f'- [About {ME}]({url("about.html")})', f'- [Media coverage]({url("media.html")})']
    write('llms.txt', '\n'.join(out) + '\n')

    full = [f'# {ME}: research papers with abstracts and summaries', f'Updated {UPDATED}. Source: {BASE}/research.html', '']
    for p in papers:
        full += [f"## {p['title']}", '', f"Authors: {names(p['authors'])}",
                 f"Status: {re.sub(r'<[^>]+>', '', venue_line(p))}" + (f" ({p['year']})" if p['status'] != 'unposted' else ''),
                 f"Page: {url('papers/' + p['slug'] + '.html')}"]
        if p.get('doi'): full.append(f"DOI: https://doi.org/{p['doi']}")
        full.append(f"Topics: {', '.join(T[t]['name'] for t in p['topics'])}")
        full += ['', f"In brief: {p['lead']} {p['brief']}", '', f"Abstract: {p['abstract']}", '']
        if p.get('glance'):
            g = p['glance']
            full += [f'- {k}: {v}' for k, v in g['design']]
            full += [f"- {('Fact ' + str(k)) if str(k).isdigit() else k}: {v}" for k, v in g['effects']]
            full.append('')
        full += [f"Keywords: {p['keywords']}", '', f"BibTeX key: {p['bibkey']}", '']
    write('llms-full.txt', '\n'.join(full))

    pages_ = [x for x in written if x.endswith('.html') and x not in REDIRECTS]
    def prio(x):
        return '1.0' if x == 'index.html' else '0.9' if x.startswith(('papers/', 'topics/')) or x == 'research.html' else '0.6'
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for x in sorted(pages_, key=lambda x: (x != 'index.html', x)):
        loc = BASE + '/' + ('' if x == 'index.html' else x)
        sm.append(f'  <url><loc>{loc}</loc><lastmod>{UPDATED_ISO}</lastmod><priority>{prio(x)}</priority></url>')
    sm.append('</urlset>')
    write('sitemap.xml', '\n'.join(sm) + '\n')

    agents = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User',
              'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'CCBot', 'Bingbot', 'Googlebot']
    rb = ['# Search engines and AI research tools are welcome to read and cite everything on this site.',
          'User-agent: *', 'Allow: /', '']
    for a in agents: rb += [f'User-agent: {a}', 'Allow: /', '']
    rb.append(f'Sitemap: {BASE}/sitemap.xml')
    write('robots.txt', '\n'.join(rb) + '\n')

REDIRECTS = {}
for t in topics:
    if t.get('legacy'): REDIRECTS[t['legacy'] + '.html'] = f"topics/{t['slug']}.html"
REDIRECTS['papers/consumer-complaints-financial-restitution.html'] = 'papers/fallible-firms-consumer-redress.html'
for t in topics:
    if t.get('former_slug'): REDIRECTS[f"topics/{t['former_slug']}.html"] = f"topics/{t['slug']}.html"

# ---------------------------------------------------------------- build
if __name__ == '__main__':
    for p in papers: paper_page(p)
    for t in topics: topic_page(t)
    research_page()
    list_page('publications.html', 'Publications',
              'Published and forthcoming papers by Rawley Z. Heimer, with plain-language summaries, plus guides and policy writing.',
              [p for p in papers if group(p) in ('published', 'other')])
    list_page('working-papers.html', 'Working papers',
              'Working papers by Rawley Z. Heimer, with plain-language summaries. Drafts not yet posted are available on request.',
              [p for p in papers if group(p) == 'working'],
              extra=f'<p class="intro">Papers under review or in progress. Feedback is welcome; drafts that are not yet posted are available by <a href="mailto:{EMAIL}">email</a>.</p>')
    home_page()
    fragment_pages()
    for old, new in REDIRECTS.items(): redirect(old, new)
    text_files()
    print(f'Built {len(written)} files into {OUT}')
