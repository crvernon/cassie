import os
import pkg_resources


def build_job_scripts(model_list, scenario_list, output_dir, cassandra_config_dir, cassandra_log_dir,
                      cassandra_main_script, sbatch_account, sbatch_partition='slurm', sbatch_walltime='01:00:00',
                      sbatch_ntasks=3, sbatch_nodes=3, sbatch_jobname='cassie', sbatch_logdir='.', template=None):
    """Generate SLURM job scripts to run Cassandra.

    :param model_list:                  List of GCM names to use.
                                        E.g., ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']
    :type model_list:                   list

    :param scenario_list:               List of scenario names to use.
                                        E.g., ['rcp26', 'rcp45', 'rcp60', 'rcp85']
    :type scenario_list:                list

    :param output_dir:                  Full path to the directory to write the files to
    :type output_dir:                   str

    :param cassandra_config_dir:        Full path to the directory containing the Cassandra configuration files
    :type cassandra_config_dir:         str

    :param cassandra_log_dir:           Full path to the directory to write cassandra log files to
    :type cassandra_log_dir:            str

    :param cassandra_main_script:       Full path with file name and extension to the "cassandra_main.py" file
    :type cassandra_main_script:        str

    :param sbatch_account:              SBATCH setting for --account
    :type sbatch_account:               str

    :param sbatch_partition:            SBATCH setting for --partition
    :type sbatch_partition:             str

    :param sbatch_walltime:             SBATCH setting for --time in format HH:MM:SS
    :type sbatch_walltime:              str

    :param sbatch_ntasks:               SBATCH setting for --ntasks
    :type sbatch_ntasks:                int

    :param sbatch_nodes:                SBATCH setting for --nodes
    :type sbatch_nodes:                 int

    :param sbatch_jobname:              SBATCH setting for --job-name
    :type sbatch_jobname:               str

    :param sbatch_logdir:               SBATCH setting for --output (where to write SLURM out to)
    :type sbatch_logdir:                str

    :param template:                    Full path with filename and sh extension to an alternate template file.  The
                                        template contained in this package is used by default.
    :type template:                     str

    """

    # use default configuration template file if user does not give one
    if template is None:
        template = pkg_resources.resource_filename('cassie', 'data/sbatch_template.sh')

    # existing tags to replace in the template file
    model_tag = '<model>'
    scenario_tag = '<scenario>'
    account_tag = '<account>'
    partition_tag = '<partition>'
    ntasks_tag = '<ntasks>'
    nodes_tag = '<nodes>'
    time_tag = '<walltime>'
    jobname_tag = '<jobname>'
    logdir_tag = '<logdir>'
    cassandra_configdir_tag = '<cassconfigdir>'
    cassandra_logdir_tag = '<casslogdir>'
    cassandra_script_tag = '<cassmainscript>'

    for model in model_list:
        for scenario in scenario_list:

            output_file = os.path.join(output_dir, f'run_{model.lower()}_{scenario}.sh')

            with open(output_file, 'w') as out:
                with open(template) as get:

                    f = get.read()

                    # replace tag names with dynamic content
                    fx = f.replace(model_tag, model)
                    fx = fx.replace(scenario_tag, scenario)

                    fx = fx.replace(account_tag, sbatch_account)
                    fx = fx.replace(partition_tag, sbatch_partition)
                    fx = fx.replace(ntasks_tag, str(sbatch_ntasks))
                    fx = fx.replace(nodes_tag, str(sbatch_nodes))
                    fx = fx.replace(time_tag, sbatch_walltime)
                    fx = fx.replace(jobname_tag, sbatch_jobname)
                    fx = fx.replace(logdir_tag, sbatch_logdir)

                    fx = fx.replace(cassandra_configdir_tag, cassandra_config_dir)
                    fx = fx.replace(cassandra_logdir_tag, cassandra_log_dir)
                    fx = fx.replace(cassandra_script_tag, cassandra_main_script)

                    out.write(fx)
