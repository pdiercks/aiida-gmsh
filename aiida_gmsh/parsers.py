# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_gmsh.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
import pathlib

from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida.common import exceptions
from aiida.orm import SinglefileData

GmshCalculation = CalculationFactory('gmsh')


class GmshParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a GmshCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, GmshCalculation):
            raise exceptions.ParsingError('Can only parse GmshCalculation')

    def parse(self, retrieved_temporary_folder, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        retrieved_temporary_folder = pathlib.Path(kwargs['retrieved_temporary_folder'])
        output_filename = self.node.get_option('output_filename')
        output_filepath = retrieved_temporary_folder / output_filename

        if not output_filepath.exists():
            self.logger.error(
                f'required output file `{output_filename}` was not present in the temporary retrieved folder.'
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        with output_filepath.open('rb') as handle:
            mshfile = SinglefileData(file=handle)

        self.out('mshfile', mshfile)
