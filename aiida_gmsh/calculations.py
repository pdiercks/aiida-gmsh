# -*- coding: utf-8 -*-
"""
Calculations provided by aiida_gmsh.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData
from aiida.plugins import DataFactory

GmshParameters = DataFactory('gmsh')


class GmshCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the gmsh executable.

    Simple AiiDA plugin wrapper for generating a .msh file from a .geo file.
    """

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super().define(spec)
        spec.input('geofile', valid_type=SinglefileData, help='The .geo file to process.')
        spec.input('parameters', valid_type=GmshParameters, help='Command line parameters for gmsh')
        spec.output('mshfile', valid_type=SinglefileData, help='The output file containing the generated mesh.')

        # set default values for AiiDA options
        spec.inputs['metadata']['options']['output_filename'].valid_type = str
        # TODO set default output_filename to geofile.with_suffix('.msh') if option "-o fname.msh" not given
        # TODO set default output_filename to fname.msh if option "-o fname.msh" is included in GmshParameters
        spec.inputs['metadata']['options']['output_filename'].default = 'mesh.msh'
        spec.inputs['metadata']['options']['resources'].default = {
            'num_machines': 1,
            'num_mpiprocs_per_machine': 1,
        }
        spec.inputs['metadata']['options']['parser_name'].default = 'gmsh'

        spec.exit_code(300, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')


    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
            needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()
        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(
            geofile=self.inputs.geofile.filename
        )
        codeinfo.code_uuid = self.inputs.code.uuid
        # TODO have to use other than stdout ouptut???

        # FIXME gmsh does not write contents of .msh to stdout
        # however, if commented out 'mesh.msh' is not retrieved by the Parser
        # codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = [
            (self.inputs.geofile.uuid, self.inputs.geofile.filename, self.inputs.geofile.filename),
        ]

        # Add the output file to the retrieved temporary list. The reason for using `retrieve_temporary_list` instead of
        # `retrieve_list` is that the parser will be reporting the output file as a `SinglefileData` output node. If we
        # use the `retrieve_list`, the output file will be stored twice; once in the `retrieved` output node and once in
        # the `mshfile` output node. By using the `retrieve_temporary_list`, the output file will not be permanently
        # stored in the `retrieved` output node and preventing duplication.
        if "-o" in codeinfo.cmdline_params:
            output_filename_index = codeinfo.cmdline_params.index("-o") + 1
            calcinfo.retrieve_temporary_list = [codeinfo.cmdline_params[output_filename_index]]
        else:
            calcinfo.retrieve_temporary_list = [self.metadata.options.output_filename]

        breakpoint()
        return calcinfo
