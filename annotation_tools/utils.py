import argparse
import os
import warnings
import json
import numpy as np


def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def save_load_dict(args, save_path):
    # saves a dictionary, 'args', as a json file. Or loads if it exists.

    if os.path.exists(save_path):
        warnings.warn(
            "Preference file exists at {}. Using existing args file.".format(save_path)
        )

        # load file
        with open(save_path, "rb") as f:
            args = json.load(f)
    else:

        with open(save_path, "w") as f:
            json.dump(args, f, indent=4, sort_keys=True)

    return args


def check_keys(args, required_keys, error_message):
    missing_keys = [key not in args for key in required_keys]

    if np.any(missing_keys):
        raise KeyError(error_message.format(required_keys[missing_keys]))

    return missing_keys
