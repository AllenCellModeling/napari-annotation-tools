#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modified from
https://github.com/sofroniewn/image-demos/blob/master/examples/kaggle_nuclei_editor.py
and
https://github.com/sofroniewn/image-demos/blob/master/examples/allen_cell.py
"""

import numpy as np
from skimage.io import imread, imsave
import os
from os.path import isfile
import warnings
import argparse
import pandas as pd
import json
from sys import platform
import napari
# import napari.layers.labels._constants as layer_constants
import tqdm
import shutil

from annotation_tools import image_loaders
from annotation_tools import utils

skimage_save_warning = "'%s is a low contrast image' % fname"
with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", category=UserWarning, message=skimage_save_warning
    )

parser = argparse.ArgumentParser(description="Annotator for GE/SCE")
parser.add_argument(
    "--prefs_path", type=str, default="./data/experiment.json", help="Experiment file"
)
args = parser.parse_args()
print(args)

with open(args.prefs_path, "rb") as f:
    args = json.load(f)

# Check the keys in the json file
missing_keys = utils.check_keys(
    args,
    required_keys=np.array(
        [
            "annotator",
            "data_csv",
            "data_dir_local",
            "save_dir",
            "start_from_last_annotation",
            "save_if_empty",
            "im_loader",
        ]
    ),
    error_message="The following fields are missing from the preferences_file: {}",
)

start_from_last_annotation = args["start_from_last_annotation"]
save_if_empty = args["save_if_empty"]

# Make a save directory if one does not exist
save_dir = args["save_dir"]
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Get the image loader function
im_loader = getattr(image_loaders, args["im_loader"])

# Get the experiment file if one already exists
args = utils.save_load_dict(args, "{}/experiment.json".format(args["save_dir"]))

# Read the list of data
df = pd.read_csv(args["data_csv"])

# Verify data
missing_keys = utils.check_keys(
    df,
    required_keys=np.array(["file_path", "set"]),
    error_message="The following fields are missing from the data_csv: {}",
)

if platform == "darwin":
    operating_system = "mac"
elif platform == "linux" or platform == "linux2":
    operating_system = "linux"
else:
    raise TypeError("mac and linux are only allowed operating systems")


data_dir_local = args["data_dir_local"]

# if we have a local data dir, then update the image paths to reflect that
if data_dir_local is not None:
    if not os.path.exists(data_dir_local):
        os.makedirs(data_dir_local)

    image_paths = np.array(
        [
            "{}/{}".format(data_dir_local, os.path.basename(file_path))
            for file_path in df.file_path
        ]
    )

    # verify all image paths are local
    for i in tqdm.tqdm(range(len(df.file_path))):
        if not os.path.exists(image_paths[i]):
            if operating_system == "mac":
                shutil.copyfile(
                    df.file_path[i].replace("/allen/", "/Volumes/"), image_paths[i]
                )
            elif operating_system == "linux":
                shutil.copyfile(df.file_path[i], image_paths[i])


else:
    # Check the os and modify the paths accordingly
    if platform == "darwin":  # macos
        image_paths = np.array(
            [file_path.replace("/allen/", "/Volumes/") for file_path in df.file_path]
        )
    elif platform == "linux" or platform == "linux2":
        image_paths = np.array([file_path for file_path in df.file_path])


ref_files = image_paths[df.set == "reference"]
annotate_files = image_paths[df.set == "annotate"]
# np.random.shuffle(annotate_files)

image_paths = np.concatenate([ref_files, annotate_files])

annotation_paths = [
    "{}/annotation_{}.tiff".format(save_dir, os.path.basename(image_path))
    for image_path in image_paths
]

# Set the image index of where we last let off
if not start_from_last_annotation:
    curr_index = 0
else:
    missing_files = ~np.array(
        [os.path.exists(annotation_path) for annotation_path in annotation_paths]
    )
    if not np.any(missing_files):
        curr_index = len(annotation_paths) - 1
    else:
        curr_index = np.where(missing_files)[0][0]

# Some useful functions for tracking the index of the current image
def get_max_index():
    return len(image_paths)


def get_index():
    return curr_index


def set_index(index):
    global curr_index

    if index < 0:
        index = 0
    if index >= get_max_index():
        index = get_max_index() - 1

    curr_index = index


with napari.gui_qt():
    # create an empty viewer
    viewer = napari.Viewer()

    @viewer.bind_key("s")
    def save(viewer, layer_name="annotations"):
        """Save the current annotations
        """
        labels = viewer.layers[layer_name].data.astype(np.uint16)

        if (not save_if_empty) and np.all(labels == 0):
            msg = "{} layer is empty. save_if_empty set to False.".format(
                viewer.layers[layer_name].name
            )
            print(msg)
            viewer.status = msg
            return

        save_path = annotation_paths[curr_index]
        imsave(save_path, labels, plugin="tifffile", photometric="minisblack")
        msg = "Saving " + viewer.layers[layer_name].name + ": " + save_path
        print(msg)
        viewer.status = msg

    @viewer.bind_key("n")
    def next(viewer):
        """Save the current annotation and load the next image and annotation
        """
        save(viewer)

        set_index(get_index() + 1)
        load_image(viewer, image_paths[get_index()], annotation_paths[get_index()])

        msg = "Loading " + image_paths[curr_index]
        print(msg)
        viewer.status = msg

    @viewer.bind_key("b")
    def previous(viewer):
        """Save the current annotation and load the previous image and annotation
        """
        save(viewer)

        set_index(get_index() - 1)
        load_image(viewer, image_paths[get_index()], annotation_paths[get_index()])

        msg = "Loading " + image_paths[curr_index]
        print(msg)
        viewer.status = msg

    @viewer.bind_key("t")
    def background_label(viewer, layer_name="annotations"):
        """Set current label to background
        """
        viewer.layers[layer_name].selected_label = 0

    @viewer.bind_key("m")
    def max_label(viewer, layer_name="annotations"):
        """Sets label to max label in visible slice
        """
        label = viewer.layers[layer_name]._data_view.max()
        viewer.layers[layer_name].selected_label = label + 1

    def load_image(viewer, im_path, im_labels_path):
        message = "Reading image {}".format(im_path)
        viewer.status = message
        print(message)

        viewer, layer_names, labels = im_loader(viewer, im_path, im_labels_path)

        if "annotations" not in layer_names:
            annotations_layer = viewer.add_labels(
                labels, name="annotations", opacity=0.75
            )
        else:
            annotations_layer = viewer.layers["annotations"]
            annotations_layer.data = labels

        annotations_layer.n_dimensional = False

        if annotations_layer.mode == "fill":
            annotations_layer.mode = "paint"
            viewer.status = "Switched to paint mode for your safety."

        max_label(viewer)

        display_string = "{}/{}: {}".format(get_index() + 1, get_max_index(), im_path)

        viewer.title = display_string

        viewer._on_layers_change(None)

    # add the first image
    load_image(viewer, image_paths[curr_index], annotation_paths[curr_index])
