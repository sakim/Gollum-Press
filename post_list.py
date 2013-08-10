# -*- coding: utf-8 -*-
import codecs
import os
import re
from post import Post


class PostList:
    def __init__(self, page, working_dir=None, index=None, per_page=None):
        self.posts = []
        self.has_next = False
        counter = 0
        path = u"{0}/{1}.md".format(working_dir, index)

        if os.path.exists(path):
            f = codecs.open(path, 'r', "utf-8")

            # read whole file to give more flexible file format
            # TODO: fix startwith format to match all ordered list item.
            for line in f:
                post_id = None

                if line.startswith('1. '):
                    for match in re.finditer(r".*\[\[.*\|(.*)\]\]|.*\[\[(.*)\]\]", line, re.U):
                        post_id = match.group(1) or match.group(2)
                        break

                    if post_id is not None:
                        path = u"{0}/{1}.md".format(working_dir, post_id)
                        if os.path.exists(path):
                            if (page - 1) * per_page <= counter < page * per_page:
                                self.posts.append(Post(post_id, working_dir=working_dir))
                            elif counter >= page * per_page:
                                self.has_next = True
                                break
                            counter += 1
            f.close()