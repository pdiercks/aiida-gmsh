#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run a test calculation on localhost.
Usage: ./example_01.py
"""
from os import path
import click
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
from aiida_gmsh import helpers

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), 'input_files')


def test_run(gmsh_code):
    """Run a calculation on the localhost computer.
    Uses test helpers to create AiiDA Code on the fly.
    """
    if not gmsh_code:
        # get code
        computer = helpers.get_computer()
        gmsh_code = helpers.get_code(entry_point='gmsh', computer=computer)

    # Prepare input parameters
    GmshParameters = DataFactory('gmsh')
    parameters = GmshParameters({'2': True})

    SinglefileData = DataFactory('singlefile')
    geofile = SinglefileData(file=path.join(INPUT_DIR, 'unit_square.geo'))

    # set up calculation
    inputs = {
        'code': gmsh_code,
        'parameters': parameters,
        'geofile': geofile,
        'metadata': {
            'description': 'Test job submission with the aiida_gmsh plugin',
        },
    }

    # Note: in order to submit your calculation to the aiida daemon, do:
    # from aiida.engine import submit
    # future = submit(CalculationFactory('gmsh'), **inputs)
    result = engine.run(CalculationFactory('gmsh'), **inputs)

    computed_gmsh = result['mshfile'].get_content()
    print('Computed gmsh msh file with content: \n{}'.format(computed_gmsh))


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.
    Example usage: $ ./example_01.py --code gmsh@localhost
    Alternative (creates gmsh@localhost-test code): $ ./example_01.py
    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
