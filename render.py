import os
from datetime import datetime
import markdown

class Renderer:

    def __init__(self):
        with open("templates/page.html") as f:
            self.page_template = f.read()
        with open("templates/post.html") as f:
            self.post_template = f.read()
        self.render()

    def render(self):
        posts = []
        for file in reversed(os.listdir("thoughts")):
            if file.endswith(".md"):
                with open("thoughts/" + file, "r", encoding="utf-8") as f:
                    text = f.read()
                text_html = markdown.markdown(text, extensions=['nl2br', 'tables'])
                raw_timestamp = file.split(".")[0]
                date = datetime.strptime(raw_timestamp, "%Y%m%d")
                date_str = date.strftime("%a, %b %d, %Y")
                post_html = self.post_template.format(content=text_html, timestamp=date_str)
                posts.append(post_html)
        page_html = self.page_template.format(posts="".join(posts))
        with open('output/index.html', 'w+') as f:
            f.write(page_html)

if __name__ == '__main__':
    Renderer()