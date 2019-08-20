import numpy as np
from skimage.io import imread
import os

from vispy.color import Colormap
import aicsimageio


def get_default_range(image, mode):

    if mode == "fluor":
        lb = np.percentile(image, 50)
        hb = np.percentile(image, 99.99)
    if mode == "bf":
        lb = np.percentile(image, 0.5)
        hb = np.percentile(image, 99.5)

    return lb, hb


def assay_dev_images(viewer, im_path, im_labels_path):
    img = aicsimageio.AICSImage(im_path)

    import pdb

    pdb.set_trace()

    cells = img.data[0]

    print("image shape: {}".format(cells.shape))

    layer_names = [layer.name for layer in viewer.layers]

    ch_nums = [0, 3, 5, 2, 1]
    ch_names = ["probe638", "probe561", "structure", "brightfield", "dapi"]
    ch_types = ["fluor", "fluor", "fluor", "bf", "fluor"]
    ch_colors = [
        [1.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 0.0, 0.0],
    ]

    for ch_num, ch_name, ch_type, ch_color in zip(
        ch_nums, ch_names, ch_types, ch_colors
    ):
        if ch_num < cells.shape[1]:
            channel = cells[:, ch_num, :, :]
        else:
            channel = np.zeros([1, 1, 1])

        if ch_name not in layer_names:
            ch = viewer.add_image(channel, name=ch_name)
        else:
            ch = viewer.layers[ch_name]
            ch.data = channel

        ch.colormap = Colormap([(0, 0, 0, 1), ch_color])
        ch.clim = get_default_range(channel, ch_type)
        ch.blending = "additive"

    # for this case, annotations are only 2D
    if os.path.exists(im_labels_path):
        labels = imread(im_labels_path)
    else:
        labels = np.zeros(cells[0, 0, :, :].shape, dtype=np.int)

    return (viewer, layer_names, labels)


def assay_dev_images_downsampled(viewer, im_path, im_labels_path):
    base_image_name = im_path[0:-6]
    print(base_image_name)

    layer_names = [layer.name for layer in viewer.layers]

    ch_names = [
        "probe638",
        "dapi",
        "brightfield",
        "probe561",
        "brightfield",
        "structure",
    ]
    ch_types = ["fluor", "fluor", "bf", "fluor", "bf", "fluor"]
    ch_colors = [
        [1.0, 0.0, 0.0, 1.0],
        [1.0, 1.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [0.0, 0.0, 1.0, 1.0],
    ]

    for i in [
        0,
        1,
        2,
        3,
        5,
    ]:  # skipping 4th channel which is a duplicate  brightfield channel
        print(i)
        img = aicsimageio.AICSImage(base_image_name + "C" + str(i) + ".tif")
        cells = img.data[0][0]

        print("image shape: {}".format(cells.shape))

        ch_num = i
        ch_name = ch_names[i]
        ch_type = ch_types[i]
        ch_color = ch_colors[i]

        if ch_num < 6:
            channel = cells
        else:
            channel = np.zeros([1, 1, 1])

        if ch_name not in layer_names:
            ch = viewer.add_image(channel, name=ch_name)
        else:
            ch = viewer.layers[ch_name]
            ch.data = channel

        ch.colormap = Colormap([(0, 0, 0, 1), ch_color])
        ch.clim = get_default_range(channel, ch_type)
        ch.blending = "additive"

        # for this case, annotations are only 2D
        if os.path.exists(im_labels_path):
            labels = imread(im_labels_path)
        else:
            labels = np.zeros(cells[0, 0, :, :].shape, dtype=np.int)
    return (viewer, layer_names, labels)


def microscopy_czi(viewer, im_path, im_labels_path):
    img = aicsimageio.AICSImage(im_path)
    cells = img.data[0][0]

    print("image shape: {}".format(cells.shape))

    layer_names = [layer.name for layer in viewer.layers]

    ch_nums = [1, 2, 3, 4, 0]
    ch_names = ["probe488", "probe561", "probe638", "dapi", "brightfield"]
    ch_types = ["fluor", "fluor", "fluor", "fluor", "bf"]
    ch_colors = [
        [1.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
    ]

    for ch_num, ch_name, ch_type, ch_color in zip(
        ch_nums, ch_names, ch_types, ch_colors
    ):
        if ch_num < cells.shape[0]:
            channel = cells[ch_num, :, :, :]
        else:
            channel = np.zeros([1, 1, 1])

        if ch_name not in layer_names:
            ch = viewer.add_image(channel, name=ch_name)
        else:
            ch = viewer.layers[ch_name]
            ch.data = channel

        ch.colormap = Colormap([(0, 0, 0, 1), ch_color])
        ch.clim = get_default_range(channel, ch_type)
        ch.blending = "additive"

    if os.path.exists(im_labels_path):
        labels = imread(im_labels_path)
    else:
        labels = np.zeros(cells[0, 0, :, :].shape, dtype=np.int)

    return (viewer, layer_names, labels)
