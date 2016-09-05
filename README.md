Bob Book to JPG
===

***Disclaimer:*** *This is unofficial software that is not affiliated, endorsed or supported by Bob Books in any way.*

This script takes a Bob Books `.mcf` file, created using [Bob
Designer](https://www.bobbooks.co.uk/create/bob-designer-software), and
produces a `.jpg` image for each page in the book.

### Usage

    pip install pillow beautifulsoup4
    python bobbook2jpg.py --size 2595x1024 input.mcf /path/to/Input_mcf-Dateien /path/to/output

### Limitations

* Cover pages are ignored.
* Only black and white backgrounds are currently supported, and the background
from the left pages is used for both left and right pages.
