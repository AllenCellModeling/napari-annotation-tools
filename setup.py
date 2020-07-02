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
    version="0.2",
    install_requires=[
        "napari[pyqt5]>=0.3.0"
        "napari-aicsimageio>=0.1.3",
        "numpy>=1.17.2",
        "scipy>=1.2.0",
        "scikit-image>=0.16.1",
        "pandas>=0.25.1",
        "natsort>=6.2.0",
        "tqdm>=4.36.1",
    ],
    extras_require={
        "dev": ["flake8", "pylint", "pytest", "pytest-cov"],
        "examples": ["t4==0.1.3"],
    },
)
