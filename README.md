# cassie
Configuration builder scripts for the Cassandra coupler

## Getting started with `cassie`
### Install from GitHub
```bash
python -m pip install git+https://github.com/crvernon/cassie.git
```

## Available functionality
### 1. Build Xanthos configuration files
**Note**:  To see all optional parameters run `help(cassie.build_xanthos_configs)` after importing `cassie`

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
pet_model_abbrev = 'trn'

# abbreviation to use in the run name for the runoff model
runoff_model_abbrev = 'abcd'

# choice to generate drought stats; 0 if no, 1 if yes
generate_drought_stats = 0

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
                             runoff_model_abbrev=runoff_model_abbrev,
                             generate_drought_stats=generate_drought_stats)
```

### 2. Build Cassandra configuration files
**Note**:  To see all optional parameters run `help(cassie.build_cassandra_configs)` after importing `cassie`

```python
import cassie

# model list to process
model_list = ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']

# scenarios to process
scenario_list = ['rcp26', 'rcp45', 'rcp60', 'rcp85']

# full path to the directory to write the files to
output_dir = '/Users/d3y010/Desktop/cas'

# number of runs to generate per configuration setup; a.k.a. runs per realization
runs_per_config = 4

# full path with file name and extension to the GCAM model interface JAR file
global_model_interface_jar = '<your path>'

# location of the DBXML libraries used by older versions of the ModelInterface
global_dbxml_lib = '<your path>'

# directory where the Xanthos configuration files are stored
xanthos_config_dir = '<your dir>'

# PET model name abbreviation that will be used in the prefix of the job name 
xanthos_pet_model_abbrev = 'trn'

# runoff model name abbreviation that will be used in the prefix of the job name
xanthos_runoff_model_abbrev = 'abcd'

# four digit start year of the simulation
fldgen_startyr = 1861

# four digit through year of the simulation
fldgen_throughyr = 2099

# directory containing R package repositories for fldgen
fldgen_pkgdir = '.'

# directory containing the emulator files in the format: "fldgen-<model>.rds"
fldgen_emulator_dir = '<your dir>'

# directory containing the TGAV fiels in the format: "fldgen-<model>_<scenario>.csv.gz"
fldgen_tgav_file_dir = '<your dir>'

# construct the cassandra configuration files
cassie.build_cassandra_configs(model_list=model_list,
                               scenario_list=scenario_list,
                               output_dir=output_dir,
                               runs_per_config=runs_per_config,
                               global_model_interface_jar=global_model_interface_jar,
                               global_dbxml_lib=global_dbxml_lib,
                               xanthos_config_dir=xanthos_config_dir,
                               xanthos_pet_model_abbrev=xanthos_pet_model_abbrev,
                               xanthos_runoff_model_abbrev=xanthos_runoff_model_abbrev,
                               fldgen_startyr=fldgen_startyr,
                               fldgen_throughyr=fldgen_throughyr,
                               fldgen_pkgdir=fldgen_pkgdir,
                               fldgen_emulator_dir=fldgen_emulator_dir,
                               fldgen_tgav_file_dir=fldgen_tgav_file_dir)
```
### 3. Build Cassandra SLURM scripts
**Note**: To see all optional parameters run `help(cassie.build_job_scripts)` after importing `cassie`

```python
import cassie

# model list to process
model_list = ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']

# scenarios to process
scenario_list = ['rcp26', 'rcp45', 'rcp60', 'rcp85']

# full path to the directory to write the files to
output_dir = '/Users/d3y010/Desktop/cas'

# full path to the directory containing the Cassandra configuration files
cassandra_config_dir = '<your dir>'

# full path to the directory to write cassandra log files to
cassandra_log_dir = '<your dir'

# full path with file name and extension to the "cassandra_main.py" file
cassandra_main_script = '<your dir>'

# construct the cassandra slurm scripts
cassie.build_job_scripts(model_list=model_list,
                         scenario_list=scenario_list,
                         output_dir=output_dir,
                         cassandra_config_dir=cassandra_config_dir,
                         cassandra_log_dir=cassandra_log_dir,
                         cassandra_main_script=cassandra_main_script,
                         sbatch_account='<your account>',
                         sbatch_partition='slurm',
                         sbatch_walltime='01:00:00',
                         sbatch_ntasks=3,
                         sbatch_nodes=3,
                         sbatch_jobname='cassie',
                         sbatch_logdir='<your log dir>')
```
#### Running the SLURM scripts after generation requires the following command:
```bash
sbatch --array=0-<your number of realizations> <your target script>
```
