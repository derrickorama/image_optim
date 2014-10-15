# ImageOptim

Python bindings for [image_optim](https://github.com/toy/image_optim)

# Known issues

Does not take advantage of the following optimization tools (the ones that image_optim supports)

* [pngout](http://www.advsys.net/ken/util/pngout.htm)
* [advpng](http://advancemame.sourceforge.net/doc-advpng.html)
* [optipng](http://optipng.sourceforge.net)
* [pngquant](http://pngquant.org/)
* [jhead](http://www.sentex.net/~mwandel/jhead/)
* [svgo](https://github.com/svg/svgo)

# Requirements

* [Python 3.x](https://www.python.org)
* [image_optim](https://github.com/toy/image_optim)
* [jpegoptim](https://github.com/tjko/jpegoptim)
* [pngcrush](http://pmt.sourceforge.net/pngcrush/)
* [gifsicle](http://www.lcdf.org/gifsicle/)

# Installation

Pip install:

    pip install -e git+git@github.com:derrickorama/imageoptim.git#egg=imageoptim

If you use a pip requirements.txt file, add this line:

    -e git+git@github.com:derrickorama/imageoptim.git#egg=imageoptim

# Usage

(need to add this)

## Testing

Use nosetests

    nosetests tests
