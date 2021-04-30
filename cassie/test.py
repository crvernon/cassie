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
