# -*- coding: utf-8 -*-
import codecs
import os
import re
from post import Post


class RecentPostList:
    def __init__(self, working_dir=None, index=None):
        self.posts = []
        per_page = 5
        counter = 0
        path = u"{0}/{1}.md".format(working_dir, index)

        if os.path.exists(path):
            f = codecs.open(path, 'r', "utf-8")

            # read whole file to give more flexible file format
            # TODO: fix startwith format to match all ordered list item.
            for line in f:
                if line.startswith('1. '):
                    if counter <= per_page:
                        post_id = None

                        for match in re.finditer(r".*\[\[.*\|(.*)\]\]|.*\[\[(.*)\]\]", line, re.U):
                            post_id = match.group(1) or match.group(2)
                            break

                        if post_id is not None:
                            path = u"{0}/{1}.md".format(working_dir, post_id)
                            if os.path.exists(path):
                                self.posts.append({'post_id': post_id, 'title': post_id.replace('-', ' ')})
                                counter += 1
                    else:
                        break
            f.close()