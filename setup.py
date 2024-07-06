from distutils.core import setup

setup(
    name='potato_sauce',
    version='1.0',
    description='Dependency-light python libraries for general use in Prize Potato projects',
    author='Oliver Kisielius',
    packages=['potato_sauce', 'potato_sauce.proto'],
    install_requires=[
        'protobuf',
    ],
    extras_require={
        # Install with `pip install -e .[dev]`
        # See https://stackoverflow.com/questions/28509965
        'dev': [
            # For absl-test. Move to install_requires if we start using
            # absl.app or absl.flags in scripts.
            'absl-py',
            'pytype',  # For type-checking
        ],
    },
)
