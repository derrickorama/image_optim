# -*- coding: utf-8 -*-

import math
import os
import re
import subprocess


class ImageOptim():

    def __init__(self, config_path=None):
        if config_path is not None:
            print('load config')
            # self.config_path = '"'

    def get_bytes(self, number):
        value = float(number[:-1])

        if number.endswith('K'):
            value = value * 1024
        elif number.endswith('M'):
            value = value * 1024 * 1024

        return math.ceil(value)

    def get_percent(self, number):
        if number.endswith('%'):
            number = number[:-1]
        number = float(number)
        return round(number, 2)

    def split_output(self, line):
        # Parse ratio
        ratio_match = re.search(r'^[^\s]+\s*', line)
        ratio = ratio_match.group(0).strip()

        # Parse size
        size_match = re.search(r'^[^\s]+\s*', line[len(ratio_match.group(0)):])
        size = size_match.group(0).strip()

        # Consider the rest of the line as the file name
        # - this captures file names that contains spaces
        filename = line[(len(size_match.group(0)) + len(ratio_match.group(0))):]

        return ratio, size, filename

    def interpret(self, stdout):
        # Split output into lines/columns & images vs totals
        images = []
        output = [line.strip() for line in re.split(r'\n', stdout.decode('utf-8').strip())]
        total_output = output.pop(len(output) - 1)

        # Gather results for each image
        for line in output:

            # Zero out image results if there are no savings
            if line.find('------') > -1:
                ratio = '0%'
                size = '0B'
                filename = line[6:].strip()
            else:
                # Parse image results
                ratio, size, filename = self.split_output(line)

            # Add to list of images
            images.append({
                'ratioSavings': self.get_percent(ratio),
                'sizeSavings': self.get_bytes(size),
                'path': filename
            })

        # Zero out totals when there are no savings
        if total_output.find('------') > -1:
            total_ratio = '0%'
            total_size = '0B'
        else:
            # Parse totals
            # - Note: starting at index 6 so "Total: " doesn't go through
            total_ratio, total_size, total_filename = self.split_output(total_output[6:].strip())

        totals = {
            # Save ratio savings in totals
            'ratioSavings': round(float(total_ratio[:-1]), 4),
            # Set size savings equal to the # of bytes (based on suffix)
            'sizeSavings': self.get_bytes(total_size)
        }

        return {
            'images': images,
            'totals': totals
        }

    def run_command(self, command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, ' '.join(command), '%s returned a non-zero return code:\n\n%s' % (command[0], stderr.decode('utf-8')))

        return stdout, stderr

    def feature_detection(self):
        utils = ['pngcrush', 'jpegoptim', 'gifsicle', 'jpegtran', 'pngout', 'advpng', 'optipng', 'pngquant', 'jhead', 'svgo']
        disabled_utils = []

        # Try getting the help docs for each utility
        for util in utils:
            try:
                stdout, stderr = self.run_command([util, '-h'])
            except FileNotFoundError:
                # If a FileNotFoundError error is thrown, the utility is not available
                disabled_utils.append('--no-%s' % util)
            except subprocess.CalledProcessError:
                pass  # who cares

        return disabled_utils

    def optimize(self, path, callback=None):
        command = ['image_optim', path]

        # Recursively optimize images if a directory is given
        if os.path.isdir(path):
            command.append('--recursive')

        # Determine which optimization utilities are available
        command += self.feature_detection()

        # Run image_optim
        stdout, stderr = self.run_command(command)

        # If nothing comes through the stdout/stderr, nothing was optimized
        if stdout == b'' and stderr == b'':
            raise NoImagesOptimizedError(path)

        # Convert result to JSON
        results = self.interpret(stdout)

        if callback is not None:
            return callback(results)
        else:
            return results


class NoImagesOptimizedError(Exception):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'No images were optimized at the given path: %s' % os.path.abspath(self.path)
