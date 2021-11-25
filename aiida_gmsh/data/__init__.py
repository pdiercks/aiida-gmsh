# -*- coding: utf-8 -*-
"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from voluptuous import Schema, Optional
from aiida.orm import Dict

# A subset of gmsh's command line options
# TODO add more gmsh command line options ...
cmdline_options = {
    Optional('1'): bool,
    Optional('2'): bool,
    Optional('3'): bool,
    Optional('pid'): bool,
    Optional('format', default='auto'): str,
    Optional('order', default=1): int,
    Optional('o'): str,
}


class GmshParameters(Dict):  # pylint: disable=too-many-ancestors
    """
    Command line options for gmsh.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)

    # pylint: disable=redefined-builtin
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``GmshParameters(dict{'2': True})``
        (Perform 2D mesh generation then exit)

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):  # pylint: disable=no-self-use
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(GmshParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return GmshParameters.schema(parameters_dict)

    def cmdline_params(self, geofile):
        """Synthesize command line parameters.

        e.g. ['geofile', '-2']

        :param geofile: Name of geo file
        :param type geofile: str

        """
        parameters = [geofile]

        pm_dict = self.get_dict()
        for key, value in pm_dict.items():
            if isinstance(value, bool) and value:
                parameters.append("-"+str(key))
            elif isinstance(value, (int, str)):
                parameters.append("-"+str(key))
                parameters.append(value)

        return [str(p) for p in parameters]

    def __str__(self):
        """String representation of node.

        Append values of dictionary to usual representation. E.g.::

            uuid: b416cbee-24e8-47a8-8c11-6d668770158b (pk: 590)
            {'ignore-case': True}

        """
        string = super().__str__()
        string += '\n' + str(self.get_dict())
        return string
