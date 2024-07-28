#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Create GIF images for making animations """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation, either version 3 of the License, or any later version. 
 
wrfplot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with wrfplot. If not, 
see <http://www.gnu.org/licenses/>.
"""

from PIL import Image
import os
import traceback
from tqdm import tqdm
import utils


def check_img(filename):
    """ Check if given input files are valid image files"""
    try:
        im = Image.open(filename)
        im.verify()
        im.close()
        im = Image.open(filename) 
        im.transpose(Image.FLIP_LEFT_RIGHT)
        im.close()
        return True
    except: 
        print('Image', filename, 'is corrupted...')
        return False


def filter_images(image_paths, type='png'):
    """Filter images based on the type of image and correctness"""
    image_files_list = sorted(image_paths)
    images = []
    for image_path in image_files_list:
        if image_path.endswith(type):
            if check_img(image_path) is True:
                images.append(Image.open(image_path))
    
    if len(images) > 0:
        return images
    return None


def make_animation(image_paths, output_file_path, speed=False, file_type='png', loop=True):
    """Create GIF file from list of images"""
    if speed is False:
        duration_sec = 0.5 * 1000
    else:
        duration_sec = speed * 1000
    images = filter_images(image_paths, type=file_type)
    if images is not None:
        try:
            img = images[0]  # next(images)
            img.save(fp=output_file_path, format='GIF', append_images=images, save_all=True, duration=duration_sec,
                     loop=0, optimize=True)
            if os.path.exists(output_file_path):
                tqdm.write(f"\nAnimation (GIF) file created at : {utils.quote(output_file_path)}")
        except Exception as e:
            tqdm.write(traceback.format_exc())
            tqdm.write(f"Failed to create animation. {e}...")

