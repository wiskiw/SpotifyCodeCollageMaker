from PIL import Image
from collage_builder import AccurateCollageBuilder
from core import ImageSize


def main():
    # Open image using Image module
    spcode1 = Image.open("raw/spcode-1-256px.jpeg")
    spcode2 = Image.open("raw/spcode-2-256px.jpeg")
    spcode3 = Image.open("raw/spcode-3-256px.jpeg")

    canvas_size = ImageSize(spcode1.size[0], spcode1.size[1] * 3)
    images = [spcode1, spcode2, spcode3]
    collage = AccurateCollageBuilder().build(canvas_size, images)

    collage.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
