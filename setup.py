import setuptools


setuptools.setup(
    author="Gregory R. Johnson",
    author_email="gregj@alleninstitute.org",
    description="Napari annotation tools",
    entry_points={
        "console_scripts": ["napari-annotator = annotation_tools.bin.napari_annotator"]
    },
    name="annotation_tools",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    url="https://github.com/AllenCellModeling/napari-annotation-tools",
    version="0.1",
    install_requires=[
        "napari==0.1.4",
        "numpy>=1.10.0",
        "scipy>=1.2.0",
        "scikit-image",
        "pandas",
        "aicsimageio==3",
        "natsort",
        "tqdm",
    ],
    extras_require={
        "dev": ["flake8", "pylint", "pytest", "pytest-cov"],
        "examples": ["t4==0.1.3"],
    },
)
