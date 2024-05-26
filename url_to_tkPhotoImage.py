from io import BytesIO
import urllib.request
from PIL import Image, ImageTk


def url2PhotoImage(url):
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    img = Image.open(BytesIO(raw_data))
    return ImageTk.PhotoImage(img)
