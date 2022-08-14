import io
from PIL import Image
from urllib.request import urlopen


class Deck:
    def __init__(self, *urls):
        self.col = 4
        self.row = 2
        self.url = urls
        self.height = 340
        self.width = 290

    async def __call__(self):
        images = [Image.open(urlopen(url)) for url in self.url]
        target = Image.new("RGBA", (self.width * self.col, self.height * self.row), (0, 0, 0, 0))

        for r in range(self.row):
            for c in range(self.col):
                target.paste(images[self.col * r + c], (self.width * c, self.height * r))

        with io.BytesIO() as output:
            target.save(output, format="png")
            content = output.getvalue()

        return content
