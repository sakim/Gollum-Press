# -*- coding: utf-8 -*-
import codecs
import re
import subprocess
import markdown
from jinja2 import Markup


class PostMeta:
    def __init__(self, post_id):
        self.post_id = post_id
        self.title = post_id.replace('-', ' ')


class Post:
    _pattern = r"\[\[(.*)\|(.*)\]\]|\[\[(.*)\]\]"

    def __init__(self, post_id, working_dir=None):
        self.post_id = post_id
        self.title = post_id.replace('-', ' ')

        filename = u"{0}.md".format(post_id)
        path = u"{0}/{1}.md".format(working_dir, post_id)

        f = codecs.open(path, 'r', "utf-8")
        self.content = f.read()
        f.close()

        self.read_categories()
        self.replace_links()
        self.author, self.date = self.read_author_date(filename, working_dir)

        # markdown to html
        self.content_markup = Markup(markdown.markdown(self.content))

    def read_author_date(self, filename, working_dir):
        cmd = u"git log --diff-filter=A --date=iso -1 {0}".format(filename)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=working_dir,  shell=True)
        p.wait()

        if p.returncode == 0:
            for match in re.finditer(r"\nAuthor:[\s]*(.*?)[\s]*<[^/]*>\nDate:[\s]*(.*?)\n", p.stdout.read(), re.U):
                return match.group(1), match.group(2)
        return "", ""

    # TODO fix regex workaround.
    def read_categories(self):
        def sub(match):
            if match.group(1):
                return match.group(1)
            else:
                return match.group(3)

        lines = self.content.splitlines()
        if len(lines) >= 2:
            candidate = lines.pop()
            hr = lines.pop()
            hr = "".join(hr.split())
            # markdown horizontal rules (gollum log convention: category separator)
            if hr.startswith(u'---') or hr.startswith(u'***') or hr.startswith(u'___'):
                tags = re.sub(Post._pattern, sub, candidate, 0, re.U)
                self.tags = tags.split(',')
                self.content = "\n".join(lines)
            else:
                self.tags = []

    def replace_links(self):
        def sub(match):
            if match.group(1):
                return u"[{1}]({0}/{2})".format(u"/posts", match.group(1), match.group(2))
            else:
                return u"[{1}]({0}/{2})".format(u"/posts", match.group(3), match.group(3))

        self.content = re.sub(Post._pattern, sub, self.content, 0, re.U)
