import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='label-studio-tools',
    version='0.0.1',
    author='Heartex',
    author_email="hello@heartex.ai",
    description='Label studio common tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/heartexlabs/label-studio-tools',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)