import re
import sys
from io import StringIO
from functools import partial
from docstring_parser import parse as docstring_parser, DocstringStyle, DocstringMeta
from docstring_parser.google import DEFAULT_SECTIONS, Section, SectionType

from pelote import __toc__ as DOCS

DEFAULT_SECTIONS.append(Section("Article", "article", SectionType.SINGULAR))
DEFAULT_SECTIONS.append(Section("References", "references", SectionType.MULTIPLE))

print_err = partial(print, file=sys.stderr)

with open("./README.template.md") as f:
    TEMPLATE = f.read()


def collapse(text):
    return text.replace("\n", " ").strip()


def get_article(docstring):
    for meta in docstring.meta:
        if type(meta) is DocstringMeta and meta.args == ["article"]:
            return collapse(meta.description)

    return None


def get_references(docstring):
    references = []

    for meta in docstring.meta:
        if type(meta) is DocstringMeta and meta.args[0] == "references":
            references.append(meta.description)

    return references


def build_toc(data):
    lines = []

    for item in data:
        lines.append(
            "* [%s](#%s)" % (item["title"], item["title"].lower().replace(" ", "-"))
        )

        for fn in item["fns"]:
            name = fn.__name__

            lines.append("  * [%s](#%s)" % (name, name.lower()))

    return "\n".join(lines)


def assembling_description(docstring):
    d = docstring.short_description or ""

    if docstring.long_description:
        if docstring.blank_after_long_description:
            d += "\n" + docstring.long_description
        else:
            d += " " + docstring.long_description

    return d.strip()


DEFAULT_RE = re.compile(r".\s*Defaults? to (.+)\.", re.MULTILINE)
CLEAN_RE = re.compile(r"`")


def template_param(param):
    line = "* **%s** " % param.arg_name

    if param.type_name:
        if param.is_optional:
            line += "*%s, optional*" % param.type_name
        else:
            line += "*%s*" % param.type_name

    m = DEFAULT_RE.search(param.description)

    if m is not None:
        line += " `%s`" % CLEAN_RE.sub("", m.group(1))

    line += " - %s" % DEFAULT_RE.sub(".", param.description)

    return line


def template_return(param):
    line = "*%s*" % param.type_name
    line += " - %s" % DEFAULT_RE.sub(".", param.description)
    return line


def build_docs(data):
    f = StringIO()

    p = partial(print, file=f)

    for item in data:
        p()
        p("---")
        p()
        p("### %s" % item["title"])

        for fn in item["fns"]:
            name = fn.__name__
            docstring = docstring_parser(fn.__doc__, DocstringStyle.GOOGLE)
            description = assembling_description(docstring)

            p()
            p("#### %s" % name)
            p()
            p(description)

            article = get_article(docstring)

            if article is not None:
                p()
                p("*Article*")
                p("> " + article)

            references = get_references(docstring)

            if references:
                p()
                p("*References*")
                p()
                for ref in references:
                    p("- " + ref)

            for example in docstring.examples:
                p()
                p("```python")
                p(example.description)
                p("```")

            p()
            p("*Arguments*")
            p()
            for param in docstring.params:
                p(template_param(param))

            if docstring.returns:
                p()
                p("*Yields*" if docstring.returns.is_generator else "*Returns*")
                p()
                p(template_return(docstring.returns))

    result = f.getvalue()
    f.close()

    return result


readme = TEMPLATE.format(toc=build_toc(DOCS), docs=build_docs(DOCS)).rstrip()

print(readme)
