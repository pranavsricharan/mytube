from PIL.Image import Image


def crop_to_aspect(image: Image, aspect_ratio: float) -> Image:
    """
    Crops an image to a given aspect ratio.
    """
    if image.width / image.height > aspect_ratio:
        newwidth = int(image.height * aspect_ratio)
        newheight = image.height
    else:
        newwidth = image.width
        newheight = int(image.width / aspect_ratio)

    x_start = (image.width - newwidth) / 2
    y_start = (image.height - newheight) / 2

    img = image.crop((x_start, y_start, x_start +
                      newwidth, y_start + newheight))

    return img
