# -*- coding: utf-8 -*-

import os
import shutil
import unittest

import nose

from .context import ImageOptim


class ImageOptimTests(unittest.TestCase):
    """image_optim tests"""

    jpg_file_orig = os.path.join(os.path.dirname(__file__), 'assets', 'jpg-example.jpg')
    png_file_orig = os.path.join(os.path.dirname(__file__), 'assets', 'png-example.png')
    gif_file_orig = os.path.join(os.path.dirname(__file__), 'assets', 'gif-example.gif')

    @classmethod
    def setUpClass(self):
        # Get original file size
        self.jpg_file_orig_size = os.path.getsize(self.jpg_file_orig)
        self.png_file_orig_size = os.path.getsize(self.png_file_orig)
        self.gif_file_orig_size = os.path.getsize(self.gif_file_orig)

    def setUp(self):
        # Copy original JPG file
        self.jpg_file = os.path.join(os.path.dirname(__file__), 'assets', 'jpg-example-temp.jpg')
        self.png_file = os.path.join(os.path.dirname(__file__), 'assets', 'png-example-temp.png')
        self.gif_file = os.path.join(os.path.dirname(__file__), 'assets', 'gif-example-temp.gif')
        shutil.copyfile(self.jpg_file_orig, self.jpg_file)
        shutil.copyfile(self.png_file_orig, self.png_file)
        shutil.copyfile(self.gif_file_orig, self.gif_file)

    def tearDown(self):
        os.remove(self.jpg_file)
        os.remove(self.png_file)
        os.remove(self.gif_file)

    def test_optimizes_jpg_image(self):
        '''ImageOptim optimizes JPG files'''

        image_optim = ImageOptim()

        def done(results):
            self.assertGreater(self.jpg_file_orig_size, os.path.getsize(self.jpg_file))

        image_optim.optimize(self.jpg_file, done)

    def test_optimizes_png_image(self):
        '''ImageOptim optimizes PNG files'''

        image_optim = ImageOptim()

        def done(results):
            self.assertGreater(self.png_file_orig_size, os.path.getsize(self.png_file))

        image_optim.optimize(self.png_file, done)

    def test_optimizes_gif_image(self):
        '''ImageOptim optimizes GIF files'''

        image_optim = ImageOptim()

        def done(results):
            self.assertGreater(self.gif_file_orig_size, os.path.getsize(self.gif_file))

        image_optim.optimize(self.gif_file, done)

    def test_optimize_returns_results_json_in_callback(self):
        '''ImageOptim returns results in JSON format when callback is provided'''

        image_optim = ImageOptim()

        def done(results):
            self.assertIn('images', results)
            self.assertIn('totals', results)

        image_optim.optimize(self.jpg_file, done)

    def test_optimize_returns_results_json_without_callback(self):
        '''ImageOptim returns results in JSON format when callback is not provided'''

        image_optim = ImageOptim()
        results = image_optim.optimize(self.jpg_file)

        self.assertIn('images', results)
        self.assertIn('totals', results)


class ResultsInterpreterTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.image_optim = ImageOptim()

    # Image results

    def test_image_savings_ratio(self):
        '''Interpreter gets savings ratio for each image'''

        stdout = b''' 5.3%  32B  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['ratioSavings'], .053)

    def test_image_savings_size_bytes(self):
        '''Interpreter gets savings size for each image in bytes when stdout displays bytes'''

        stdout = b''' 5.3%  32B  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['sizeSavings'], 32)

    def test_image_savings_size_kilobytes(self):
        '''Interpreter gets savings size for each image in bytes when stdout displays kilobytes'''

        stdout = b''' 5.3%  32K ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['sizeSavings'], 32768)

    def test_image_savings_size_megabytes(self):
        '''Interpreter gets savings size for each image in bytes when stdout displays megabytes'''

        stdout = b''' 5.3%  32M  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['sizeSavings'], 33554432)

    def test_image_path(self):
        '''Interpreter gets path to each image'''

        stdout = b''' 5.3%  32M  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['path'], './path/to/image.jpg')

    def test_image_savings_size_float(self):
        '''Interpreter gets savings size for each image in bytes when stdout displays floats'''

        stdout = b''' 5.3%  32.25K  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['sizeSavings'], 33024)

    def test_image_savings_size_float_with_remainder(self):
        '''Interpreter gets savings size for each image in bytes when stdout displays floats that don\'t equal an whole # of bytes'''

        stdout = b''' 5.3%  32.55K  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['sizeSavings'], 33332)

    def test_no_savings(self):
        '''Interpreter sets ratioSavings and sizeSavings to 0 when no optimization occurs'''

        stdout = b''' ------    ./path/to/image.jpg\nTotal: ------'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['images'][0]['ratioSavings'], 0)
        self.assertEqual(results['images'][0]['sizeSavings'], 0)
        self.assertEqual(results['images'][0]['path'], './path/to/image.jpg')

    # Totals

    def test_total_savings_ratio(self):
        '''Interpreter gets total savings ratio'''

        stdout = b''' 5.3%  32B  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['totals']['ratioSavings'], .1157)

    def test_total_savings_size_bytes(self):
        '''Interpreter gets total savings size in bytes when stdout displays bytes'''

        stdout = b''' 5.3%  32B  ./path/to/image.jpg\nTotal: 11.57% 191B'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['totals']['sizeSavings'], 191)

    def test_total_savings_size_kilobytes(self):
        '''Interpreter gets total savings size in bytes when stdout displays kilobytes'''

        stdout = b''' 5.3%  32B  ./path/to/image.jpg\nTotal: 11.57% 191K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['totals']['sizeSavings'], 195584)

    def test_total_savings_size_megabytes(self):
        '''Interpreter gets total savings size in bytes when stdout displays megabytes'''

        stdout = b''' 5.3%  32B  ./path/to/image.jpg\nTotal: 11.57% 191M'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['totals']['sizeSavings'], 200278016)

    def test_total_no_savings(self):
        '''Interpreter sets ratioSavings and sizeSavings to 0 when no optimization occurs'''

        stdout = b''' ------    ./path/to/image.jpg\nTotal: ------'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['totals']['ratioSavings'], 0)
        self.assertEqual(results['totals']['sizeSavings'], 0)

    def test_total_savings_size_float(self):
        '''Interpreter gets total savings size in bytes when stdout displays floats'''

        stdout = b''' 5.3%  32K  ./path/to/image.jpg\nTotal: 11.57% 191.25K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['totals']['sizeSavings'], 195840)

    def test_total_savings_size_float_with_remainder(self):
        '''Interpreter gets total savings size in bytes when stdout displays floats that don\'t equal an whole # of bytes'''

        stdout = b''' 5.3%  32.55K  ./path/to/image.jpg\nTotal: 11.57% 191.55K'''
        results = self.image_optim.interpret(stdout)
        self.assertEqual(results['totals']['sizeSavings'], 196148)

if __name__ == '__main__':
    nose.main()
