import os
from distutils.dir_util import copy_tree
from pathlib import Path
from datetime import datetime
from io import StringIO

import markdown

class Renderer:

    def __init__(self):
        with open("templates/page.html") as f:
            self.page_template = f.read()
        with open("templates/post.html") as f:
            self.post_template = f.read()
        with open("templates/permafooter.html") as f:
            self.permafooter_template = f.read()
        self.permapages = []

    def _load_assets(self):
        copy_tree("assets", "output/assets")

    def _write_files(self):
        Path("output").mkdir(parents=True, exist_ok=True)
        with open('output/index.html', 'w+') as f:
            f.write(self.page_html)
        
        for ts, permapage in self.permapages:
            Path(f"output/post/{ts}").mkdir(parents=True, exist_ok=True)
            with open(f"output/post/{ts}/index.html", 'w+') as f:
                f.write(permapage)

    def _fill_templates(self):
        html_contents = []
        for file in reversed(os.listdir("thoughts")):
            if file.endswith(".md"):
                with open("thoughts/" + file, "r", encoding="utf-8") as f:
                    text = f.read()
                content_html = markdown.markdown(text, extensions=['nl2br', 'tables'])
                content_html = content_html.replace("<code>", "<pre><code>").replace("</code>", "</code></pre>")
                raw_timestamp = file.split(".")[0]
                html_contents.append((raw_timestamp, content_html))
        html_contents.sort(reverse=True)

        main_feed_builder = StringIO()
        for i in range(len(html_contents)):
            ts, content_html = html_contents[i]
            # Main feed generation
            date = datetime.strptime(ts, "%Y%m%d%H%M")
            date_str = date.strftime("%a, %b %d, %Y %I:%M %p")
            post_block = self.post_template.format(
                content=content_html,
                timestamp=date_str,
                permalink_rel_path=f"post/{raw_timestamp}"
            )
            main_feed_builder.write(post_block)

            # Permapages generation
            post_perma_block = self.post_template.format(
                content=content_html,
                timestamp=date_str,
                permalink_rel_path=""
            )
            perma_footer = self.permafooter_template.format(
                newer="../" + html_contents[i-1][0] if i > 0 else "",
                newer_text="<< Newer" if i > 0 else "",
                older="../" + html_contents[i+1][0] if i < len(html_contents)-1 else "",
                older_text="Older >>" if i < len(html_contents)-1 else "",
                url_depth="../../"
            )
            post_permagpage = self.page_template.format(
                posts=post_perma_block,
                url_depth="../../",
                footer=perma_footer,
            )
            self.permapages.append((ts, post_permagpage))

        self.page_html = self.page_template.format(posts=main_feed_builder.getvalue(), url_depth="", footer="") 

    def render(self):
        self._load_assets()
        self._fill_templates()
        self._write_files()

if __name__ == '__main__':
    Renderer().render()