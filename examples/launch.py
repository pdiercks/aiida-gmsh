import os
from aiida.engine import run, submit
from aiida.orm import Dict
from aiida.plugins import DataFactory
from workchain import SubprocessWorkChain
SinglefileData = DataFactory("singlefile")

param = {"-2": True, "-o": "mysupermesh.msh"}
inputs = {
        "cmdline_parameters": Dict(dict=param),
        "geofile": SinglefileData(os.path.abspath("./unit_square.geo")),
        }
result = submit(SubprocessWorkChain, **inputs)
