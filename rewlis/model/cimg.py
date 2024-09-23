import os.path
import base64


def encode_image(folder="../../res/img/"):
    result = "\n\nclass Img:\n\n    def __init__(self):\n        self.images = {\n"
    if os.path.exists(folder):
        files = os.listdir(folder)
        for file in files:
            if not file.endswith((".png", ".ico")):
                continue
            filepath = f"{folder}{file}"
            with open(filepath, mode="rb") as f:
                image = f.read()
            result += " " * 16 + f"'{filepath}': \n"
            image_base64 = str(base64.b64encode(image))[2:-1]
            length = len(image_base64)
            chunk_size = 60
            array = list(range(0, length, chunk_size))
            for i in array[:-1]:
                result += " " * 16 + "b'" + image_base64[i:i + chunk_size] + "' +\n"
            result += " " * 16 + "b'" + image_base64[array[-1]:array[-1] + chunk_size] + "',\n"
    result += " " * 8 + "}\n"
    with open("img.py", mode="w") as f:
        f.write(result)


def decode_image(folder="img/", img=None):
    if img is None:
        return
    if not os.path.exists(folder):
        os.mkdir(folder)
    for image in img.images:
        filepath = folder + image.split("/")[-1]
        if not os.path.exists(filepath):
            with open(filepath, mode="wb") as f:
                with open("tmp", mode="wb") as tmp:
                    tmp.write(img.images[image])
                with open("tmp", mode="rb") as tmp:
                    base64.decode(tmp, f)
                os.unlink("tmp")


if __name__ == "__main__":

    # try:
    #     from img import Img
    # except ModuleNotFoundError:
    encode_image()
    # from img import Img
    # decode_image(folder="../../res/img/", img=Img())
