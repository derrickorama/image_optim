# -*- coding: utf-8 -*-

import math
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
            number = float(number[:-1]) * .01
        else:
            number = float(number)
        return round(number, 4)

    def interpret(self, stdout):
        # Split output into lines/columns & images vs totals
        images = []
        output = [re.split(r'\s+', line) for line in re.split(r'\n', stdout.decode('utf-8').strip())]
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
        proc = subprocess.Popen(['image_optim', path, '--no-pngout', '--no-advpng', '--no-optipng', '--no-pngquant', '--no-jhead', '--no-svgo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        # Convert result to JSON
        results = self.interpret(stdout)

        if proc.returncode != 0:
            raise Exception('image_optim returned a non-zero return code:\n\n%s' % stderr)

        if callback is not None:
            return callback(results)
        else:
            return results
