from setuptools import setup

setup(
    name="pongpy",
    url='https://github.com/pistatium/pong',
    description='Pong game',
    version="0.0.1",
    license='MIT',
    author='pistatium',
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
