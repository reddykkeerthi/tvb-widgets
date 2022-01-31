# -*- coding: utf-8 -*-
#
# "TheVirtualBrain - Widgets" package
#
# (c) 2022-2023, TVB Widgets Team
#

import os
import setuptools

VERSION = "0.1"
TEAM = "Juelich SDL Neuroscience, INS -Marseille, Codemart"
REQUIRED_PACKAGES = ["ebrains_drive", "ipywidgets", "ipygany", "pyvista", "tvb-library"]

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fd:
    DESCRIPTION = fd.read()

setuptools.setup(name='tvb-widgets',
                 version=VERSION,
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 install_requires=REQUIRED_PACKAGES,
                 description='GUI widgets for EBRAINS showcases',
                 long_description=DESCRIPTION,
                 license="GPL-3.0-or-later",
                 author=TEAM,
                 author_email='tvb.admin@thevirtualbrain.org',
                 url='https://github.com/the-virtual-brain/tvb-widgets',
                 keywords='tvb widgets jupyterlab ebrains showcases')
