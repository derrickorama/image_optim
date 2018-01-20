# ImageOptim

Python bindings for [image_optim](https://github.com/toy/image_optim).

*Note: this will also autodetect the optimization tools available and apply the --no-UTILITY_NAME options when executing image_optim.*

# Requirements

* [Python 3.x](https://www.python.org)
* [image_optim](https://github.com/toy/image_optim)
* An image optimization tool for any image you plan to optimize (e.g. [jpegoptim](https://github.com/tjko/jpegoptim) for JPGs, [pngcrush](http://pmt.sourceforge.net/pngcrush/) for PNGs, [gifsicle](http://www.lcdf.org/gifsicle/) for GIFs, etc.)

# Installation

Pip install:

    pip install -e git+https://github.com/derrickorama/image_optim.git#egg=imageoptim

If you use a pip requirements.txt file, add this line:

    -e git+git@github.com:derrickorama/imageoptim.git#egg=imageoptim

# Usage

Optimize a single image

    image_optim = ImageOptim()
    results = image_optim.optimize('/path/to/image.jpg')
    print(results)

Optimize an entire directory

    image_optim = ImageOptim()
    results = image_optim.optimize('/path/to/directory')
    print(results)

Exclude paths

    image_optim = ImageOptim()
    results = image_optim.optimize('/path/to/directory', exclude='filename.*')
    print(results)

You can also use a callback (for async sort of stuff)

    image_optim = ImageOptim()

    def done(results):
        print(results)

    image_optim.optimize('/path/to/image.jpg', done)

# Development

1. Install or build image_optim (Ruby Gem) from source

       gem install image_optim

2. Install gifsicle, jpegoptim, and pngcrush (see https://github.com/toy/image_optim for details)

3. Create and "source" into a Python 3 virtual environment, for example

       pyvenv-3.4 ENV
       source ENV/bin/activate

4. Install dependencies with "make"

       make

## Testing

Run "make test"

       make test
