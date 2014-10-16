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

    def interpret(self, stdout):
        # Split output into lines/columns & images vs totals
        images = []
        output = [re.split(r'\s+', line.strip()) for line in re.split(r'\n', stdout.decode('utf-8').strip())]
        total_output = output.pop(len(output) - 1)

        # Gather results for each image
        for line in output:
            if line[0] == '------':
                line[0] = '0'
                line.append(line[1])
                line[1] = '0B'

            images.append({
                'ratioSavings': self.get_percent(line[0]),
                'sizeSavings': self.get_bytes(line[1]),
                'path': line[2]
            })

        # If there were no savings, set "savings" and "sizeSavings" to 0
        if total_output[1] == '------':
            total_output[1] = '0B'
            total_output.append('0B')

        totals = {
            # Save ratio savings in totals
            'ratioSavings': round(float(total_output[1][:-1]) * .01, 4),
            # Set size savings equal to the # of bytes (based on suffix)
            'sizeSavings': self.get_bytes(total_output[2])
        }

        return {
            'images': images,
            'totals': totals
        }

    def optimize(self, path, callback=None):
        command = ['image_optim', path]

        if os.path.isdir(path):
            command.append('--recursive')

        command = command + ['--no-pngout', '--no-advpng', '--no-optipng', '--no-pngquant', '--no-jhead', '--no-svgo', '--jpeg-tran']

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            raise Exception('image_optim returned a non-zero return code:\n\n%s' % stderr.decode('utf-8'))

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
