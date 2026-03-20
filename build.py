
#   -*- coding: utf-8 -*-
"""
PyBuilder configuration file for the G8X project.
This module defines the plugins and properties for the build process.
"""
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")


NAME = "G8X.2026.TXX.EG2"
DEFAULT_TASK = "publish"


@init
def set_properties(project):
    """
        Sets the project properties for PyBuilder.
    """
    project.set_property("coverage_break_even", [80, 100])
