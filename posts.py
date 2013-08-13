# -*- coding: utf-8 -*-
import codecs
import os
import re
import math
from post import Post, PostMeta


class Posts:
    pattern = r"^\s*\d+\.\s*\[\[([^\|]*?)\|?([^\|]*?)\]\]"  # 1. [[title|id]] or [[id]]

    def __init__(self, working_dir=None, index=None, per_page=None):
        self.working_dir = working_dir
        self.index = index
        self.per_page = per_page
        self.post_metas = []

        path = u"{0}/{1}.md".format(working_dir, index)

        if os.path.exists(path):
            f = codecs.open(path, 'r', 'utf-8')

            # read whole file to give more flexible file format
            for line in f:
                match = re.match(Posts.pattern, line, re.U)
                if match:
                    post_id = match.group(2)
                    path = u"{0}/{1}.md".format(working_dir, post_id)
                    if os.path.exists(path):
                        self.post_metas.append(PostMeta(post_id))
            f.close()

    def get_posts(self, page):
        posts = []

        for i in range((page-1)*self.per_page, page*self.per_page):
            if i >= len(self.post_metas):
                break
            posts.append(Post(self.post_metas[i].post_id, working_dir=self.working_dir))

        return posts

    def get_recent_metas(self):
        length = len(self.post_metas)
        return self.post_metas[0:10] if length >= 10 else self.post_metas[0:length]

    def get_num_of_pages(self):
        return math.ceil(len(self.post_metas) / (self.per_page*1.0))
