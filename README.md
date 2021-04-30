# cassie
Configuration builders scripts for the Cassandra coupler

## Getting started with `cassie`
### Install from GitHub
```bash
python -m pip install git+https://github.com/crvernon/cassie.git
```

## Available functionality
### 1. Build Xanthos configuration files
```python 
import cassie

# model list to process
model_list = ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']

# scenarios to process
scenario_list = ['rcp26', 'rcp45', 'rcp60', 'rcp85']

# directory to write the output config files to
output_dir = "<your output dir>"

# the number of config files to generate per combination
n_configs = 1000

# the root directory where xanthos input and output directories are stored
xanthos_root_dir = "<your dir>"

# the directory to save your xanthos run output to
xanthos_output_dir = "output/<my additional dir>"

# directory where the drought threshold files are stored
drought_thresholds_dir = "<your dir>"

# xanthos variables to write files for
xanthos_output_variables = 'q'

# abbreviation to use in the run name for the PET model
pet_model_abbrev = 'thorn'

# abbreviation to use in the run name for the runoff model
runoff_model_abbrev = 'abcd'

# generate the configuration files
cassie.build_xanthos_configs(model_list=model_list,
                             scenario_list=scenario_list,
                             output_dir=output_dir,
                             n_configs=n_configs,
                             xanthos_root_dir=xanthos_root_dir,
                             xanthos_output_dir=xanthos_output_dir,
                             drought_thresholds_dir=drought_thresholds_dir,
                             xanthos_output_variables=xanthos_output_variables,
                             pet_model_abbrev=pet_model_abbrev,
                             runoff_model_abbrev=runoff_model_abbrev)
```
