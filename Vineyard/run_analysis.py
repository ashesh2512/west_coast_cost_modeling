"""Primary analysis script."""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import pandas as pd
import datetime as dt
import pprint

from ORBIT import load_config
from ORBIT import ProjectManager
from ORBIT.core.library import initialize_library

import os
if 'DATA_LIBRARY' in os.environ:
    del os.environ['DATA_LIBRARY']

if __name__ == '__main__':
    # Point ORBIT to the custom data libraries in the anlaysis repo
    initialize_library("/Users/asharma/codes/P_Code/currTests/cost_modeing/Vineyard/data")

    # Load in the input configuration YAML
    config = load_config('/Users/asharma/codes/P_Code/currTests/cost_modeing/Vineyard/vineyard.yaml')

    # Print out the required information for input config
    phases = ['ArraySystemDesign', 'ExportSystemDesign', 'MonopileDesign', 'OffshoreSubstationDesign', 'ScourProtectionDesign', 'ArrayCableInstallation', 'ExportCableInstallation', 'OffshoreSubstationInstallation', 'MonopileInstallation', 'ScourProtectionInstallation', 'TurbineInstallation']
    expected_config = ProjectManager.compile_input_dict(phases)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(expected_config)

    # Initialize and run project
    weather = pd.read_csv('/Users/asharma/codes/P_Code/currTests/cost_modeing/Vineyard/data/weather/vineyard_wind_weather_1983_2017_orbit.csv').set_index("datetime")  # Project installation begins at start of weather file unless other wise specified in install_phase in input config
    project = ProjectManager(config, weather=weather)
    project.run()

    # Print some output results
    pp.pprint(project.capex_breakdown_per_kw)
