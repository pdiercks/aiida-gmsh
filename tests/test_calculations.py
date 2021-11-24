# -*- coding: utf-8 -*-
""" Tests for calculations

"""
import os
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run
from aiida.orm import SinglefileData

from . import TEST_DIR


def test_process(gmsh_code):
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""

    # Prepare input parameters
    GmshParameters = DataFactory('gmsh')
    parameters = GmshParameters({"2": True})

    input_geo = SinglefileData(file=os.path.join(TEST_DIR, "input_files", "unit_square.geo"))

    # set up calculation
    # needs to match spec definition in CalcJob.define()
    inputs = {
        'code': gmsh_code,
        'parameters': parameters,
        'geofile': input_geo,
        'metadata': {
            'options': {
                'max_wallclock_seconds': 30
            },
        },
    }

    result = run(CalculationFactory('gmsh'), **inputs)
    breakpoint()
    mshfile_content = result['mshfile'].get_content()

    # funny enough, could use aiida-diff here to compare against reference msh file
    assert '$MeshFormat' in mshfile_content
    assert '4.1 0 8' in mshfile_content
    assert '$EndMeshFormat' in mshfile_content
    assert '$PhysicalNames' in mshfile_content
    assert '2 1 "surface"' in mshfile_content
    assert '$EndPhysicalNames' in mshfile_content
