# Napari Annotation Tools


#### **_this repo is under development and not stable!_**


## Installation


(optional) Make a conda envrionment first:
```sh
$ conda create -n annotation_tools python=3.7
$ conda activate annotation_tools
```

Install the software:
```sh
$ git clone https://github.com/AllenCellModeling/napari-annotation-tools.git
$ cd napari-annotation-tools
$ pip install -e .
```


## HOW TO RUN

### Default Usage:

The code is set up with useful defaults and is configured to to copy the files over to your computer first. __Please make sure you have 27.9 gb of space free for images before you start__. 

First start finder and press ⌘ + k to bring up the "Connect to Server" menu. Enter `smb://allen` and mount the `aics` drive. This allows us to automagically copy files over from the file system.

Then start the app. It should start copying over files for you. Once this is done, you should be able to disconnect from the network an annotate stuff remotely. Those results will be saved to your harddrive in the `./data/annotations folder`.

After the `napari` environment is activated in conda, run the following command in the Teriminal app:
```sh
$ napari-annotator
```

### Advanced Usage:

By default the code uses a .json file that lives in `./data/experiment.json`. That file looks like this:
```
{
	"annotator": "user",
	"data_csv": "./data/20190520_napari_annotation_files.csv",
	"data_dir_local": "./data/images",
	"save_dir": "./data/annotations",
	"start_from_last_annotation": 1,
	"save_if_empty": 0
}
```
These parameters should be self explanatory. Please change this configuration to suit your needs. 

To run the annotator with a different .json file do:

```sh
$ napari-annotator --prefs_path "/path/to/your/file.json"
```


Features
--------

* TODO - Documentation

Support
-------
We are not currently supporting this code, but simply releasing it to the community AS IS but are not able to provide any guarantees of support. The community is welcome to submit issues, but you should not expect an active response.

## Documentation: 
   https://annotation-tools.readthedocs.io.

