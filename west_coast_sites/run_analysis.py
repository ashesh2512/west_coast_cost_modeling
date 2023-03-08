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
os.chdir('/Users/asharma/codes/P_Code/currTests/west_coast_cost_modeling/west_coast_sites')
write_mode = False

# set problem parameters
site = 'central_CA'
mean_windspeed = 9.31
port = 'San Luis'
distance = 111.351
depth = 1013
distance_to_landfall = 97.381
start_date = '01/01/2002'

if 'DATA_LIBRARY' in os.environ:
    del os.environ['DATA_LIBRARY']

# set relative paths (alternatively, set absolute paths)
custom_library = 'data'
custom_config  = 'base_setup.yaml'
custom_weather = 'data/weather/' + site + '_swh_150m.csv'

if __name__ == '__main__':
    # Point ORBIT to the custom data libraries in the anlaysis repo
    initialize_library(custom_library)

    # Load in the input configuration YAML
    base_config = load_config(custom_config)

    # dependency of install phases
    mod_config = {
        'site': {
        'mean_windspeed': mean_windspeed,
        'distance': distance,
        'depth': depth,
        'distance_to_landfall': distance_to_landfall
        },

        'install_phases': {
        'MooringSystemInstallation': start_date,
        'MooredSubInstallation': ('MooringSystemInstallation', 0.5),
        'ArrayCableInstallation': ('MooredSubInstallation', 0.5),
        'ExportCableInstallation': start_date,
        'FloatingSubstationInstallation': ('ExportCableInstallation', 0.25)
        }
    }

    # create run config
    run_config = ProjectManager.merge_dicts(base_config, mod_config)

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
    # pp.pprint(expected_config)

    # Initialize and run project
    weather = pd.read_csv(custom_weather, parse_dates=["datetime"]).set_index("datetime")
    project = ProjectManager(run_config, weather=weather)
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
    if write_mode:
        df.to_excel(site + '_action_' + port + start_date + '.xlsx', index=False) 