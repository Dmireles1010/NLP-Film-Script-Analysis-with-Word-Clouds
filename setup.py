import setuptools



setuptools.setup(
    name="CECS-450-Group-3", # Replace with your own username
    version="0.0.1",
    author="David Mireles, Tri Nguyen, Katherine Seng",

    description="A Tag Cloud Visualization",
    long_description="A Tag Cloud Visualization of Film Transcript Dialogue",
    long_description_content_type="text/markdown",
    url="https://github.com/KatherineSeng/CECS450-Group3-Project1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
       'nltk'
    ]

)