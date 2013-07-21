# -*- coding: utf-8 -*-
import codecs
import os
import re
from post import Post


class PostList:
    def __init__(self, page, working_dir=None, index=None, per_page=None):
        self.posts = []

        path = u"{0}/{1}.md".format(working_dir, index)

        if os.path.exists(path):
            f = codecs.open(path, 'r', "utf-8")

            # read whole file to give more flexible file format
            counter = 0
            for line in f:
                if line.startswith('1. '):
                    if (page - 1) * per_page <= counter <= page * per_page:
                        post_id = None

                        for match in re.finditer(r".*\[\[.*\|(.*)\]\]|.*\[\[(.*)\]\]", line, re.U):
                            post_id = match.group(1) or match.group(2)
                            break

                        if post_id is not None:
                            path = u"{0}/{1}.md".format(working_dir, post_id)
                            if os.path.exists(path):
                                self.posts.append(Post(post_id, working_dir=working_dir))
                                counter += 1

                            if (counter + 1) > page * per_page:
                                break
            f.close()
