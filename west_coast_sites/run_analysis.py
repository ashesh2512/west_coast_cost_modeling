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

if 'DATA_LIBRARY' in os.environ:
    del os.environ['DATA_LIBRARY']

# set relative paths (alternatively, set absolute paths)
custom_library = "data"
custom_config  = "north_ca.yaml"
custom_weather = "data/weather/humboldt_weather_2010_2018.csv"

if __name__ == '__main__':
    # Point ORBIT to the custom data libraries in the anlaysis repo
    initialize_library(custom_library)

    # Load in the input configuration YAML
    config = load_config(custom_config)

    # Print out the required information for input config
    phases = ['ArraySystemDesign',
              'ElectricalDesign',
              'SemiSubmersibleDesign',
              'SemiTautMooringSystemDesign',
              'ArrayCableInstallation',
              'ExportCableInstallation',
              'MooringSystemInstallation',
              'FloatingSubstationInstallation',
              'MooredSubInstallation']
    expected_config = ProjectManager.compile_input_dict(phases)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(expected_config)

    # Initialize and run project
    weather = pd.read_csv(custom_weather, parse_dates=["datetime"]).set_index("datetime")
    project = ProjectManager(config, weather=weather)
    project.run()

    # Print some output results
    pp.pprint(project.capex_breakdown_per_kw)

    print(f"\nInstallation CapEx: {project.installation_capex/1e6:.0f} M")
    print(f"System CapEx: {project.system_capex/1e6:.0f} M")
    print(f"Turbine CapEx: {project.turbine_capex/1e6:.0f} M")
    print(f"Soft CapEx: {project.soft_capex/1e6:.0f} M")
    print(f"Total CapEx: {project.total_capex/1e6:.0f} M")
    print(f"Installation Time: {project.installation_time:.0f} h\n")

    # Should add a method here to report the start/end dates of each phase and maybe plot a Gantt chart or similar
    df = pd.DataFrame(project.actions)
    # df.to_excel("north_ca_action.xlsx", index=False) 