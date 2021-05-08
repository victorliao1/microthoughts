import os
from datetime import datetime
from distutils.dir_util import copy_tree
import markdown

class Renderer:

    def __init__(self):
        with open("templates/page.html") as f:
            self.page_template = f.read()
        with open("templates/post.html") as f:
            self.post_template = f.read()

    def _load_assets(self):
        copy_tree("assets", "output/assets")

    def _fill_templates(self):
        posts = []
        for file in reversed(os.listdir("thoughts")):
            if file.endswith(".md"):
                with open("thoughts/" + file, "r", encoding="utf-8") as f:
                    text = f.read()
                text_html = markdown.markdown(text, extensions=['nl2br', 'tables'])

                text_html = text_html.replace("<code>", "<pre><code>").replace("</code>", "</code></pre>")

                raw_timestamp = file.split(".")[0]
                date = datetime.strptime(raw_timestamp, "%Y%m%d%H%M")
                date_str = date.strftime("%a, %b %d, %Y %I:%M %p")
                post_html = self.post_template.format(content=text_html, timestamp=date_str)
                posts.append(post_html)
        page_html = self.page_template.format(posts="".join(posts))
        with open('output/index.html', 'w+') as f:
            f.write(page_html)
    
    def render(self):
        self._load_assets()
        self._fill_templates()

if __name__ == '__main__':
    Renderer().render()