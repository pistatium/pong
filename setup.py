from setuptools import setup, find_packages

setup(
    name="pongpy",
    url='https://github.com/pistatium/pong',
    description='Pong game',
    version="0.1.2",
    license='MIT',
    author='pistatium',
    packages=find_packages(),
    install_requires=[
        "pyxel",
        "click"
    ],
    entry_points={
        "gui_scripts": [
            "pongpy = pongpy.cmd:main"
        ]
    }
)
