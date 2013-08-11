# -*- coding: utf-8 -*-
import codecs
import os
import re
from post import Post


class PostList:
    RECENT_ONLY = 0

    def __init__(self, page, working_dir=None, index=None, per_page=None):
        self.posts = []
        self.recent = []  # meta
        num_of_recent = 5

        self.has_next = False
        counter = 0
        path = u"{0}/{1}.md".format(working_dir, index)

        if os.path.exists(path):
            f = codecs.open(path, 'r', "utf-8")

            # read whole file to give more flexible file format
            for line in f:
                post_id = None

                for match in re.finditer(r"^\d+\.*\[\[.*\|(.*)\]\]|.*\[\[(.*)\]\]", line, re.U):
                    post_id = match.group(1) or match.group(2)
                    break

                if post_id is not None:
                    path = u"{0}/{1}.md".format(working_dir, post_id)
                    if os.path.exists(path):
                        if len(self.recent) < num_of_recent:
                            self.recent.append({'post_id': post_id, 'title': post_id.replace('-', ' ')})

                        if (page - 1) * per_page <= counter < page * per_page:
                            self.posts.append(Post(post_id, working_dir=working_dir))
                        elif counter >= page * per_page and page != PostList.RECENT_ONLY:
                            self.has_next = True
                            break
                        counter += 1
        f.close()