import os
import pkg_resources


def build_xanthos_configs(model_list, scenario_list, output_dir, n_configs, xanthos_root_dir, xanthos_output_dir,
                          drought_thresholds_dir, xanthos_output_variables='q', pet_model_abbrev=None,
                          runoff_model_abbrev=None, router_model_abbrev=None, template=None,
                          generate_drought_stats=0):
    """Generate Xanthos configuration files for use in Cassandra.  A default template is used that is customized for
    running the Thornthwaite PET with the abcd runoff model to execute the drought module.  You can provide your own
    template file as well that has custom configurations.

    :param model_list:                  List of GCM names to use.
                                        E.g., ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']
    :type model_list:                   list

    :param scenario_list:               List of scenario names to use.
                                        E.g., ['rcp26', 'rcp45', 'rcp60', 'rcp85']
    :type scenario_list:                list

    :param output_dir:                  Full path to the directory to write the files to
    :type output_dir:                   str

    :param n_configs:                   The number of unique configuration files to generate
    :type n_configs:                    int

    :param xanthos_root_dir:            Full path to the directory containing the input and output directories in
                                        Xanthos.  In the Xanthos config file, this is the variable "RootDir"
    :type xanthos_root_dir:             str

    :param xanthos_output_dir:          Relative path directory name for the xanthos outputs to be written to
                                        In the Xanthos config file, this is the variable "OutputFolder"
                                        E.g., 'output/trn_abcd_1000'
    :type xanthos_output_dir:           str

    :param drought_thresholds_dir:      The full path to the directory containing the drought thresholds.  The
                                        expected threshold filename format for the files within is:
                                        "drought_thresholds_<model>_16610101-22991231.npy" where model matches the
                                        those in the "model_list" parameter of this function.
                                        E.g., '/path/to/my/dir'
                                        NOTE:  no trailing slash
    :type drought_thresholds_dir:       str

    :param xanthos_output_variables:    The string of variables to output; currently set to 'q' for runoff
    :type xanthos_output_variables:     str

    :param pet_model_abbrev:            PET model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'trn'
    :type pet_model_abbrev:             str

    :param runoff_model_abbrev:         Runoff model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'abcd'
    :type runoff_model_abbrev:          str

    :param router_model_abbrev:         Routing model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'mrtm'
    :type router_model_abbrev:          str

    :param template:                    Full path with filename and ini extension to an alternate template file.  The
                                        template contained in this package is used by default.
    :type template:                     str

    :param generate_drought_stats:      1 to generate drought statistics, 0 to NOT generate
    :type generate_drought_stats:       int

    """

    # use default configuration template file if user does not give one
    if template is None:
        template = pkg_resources.resource_filename('cassie', 'data/xanthos_thorn_abcd_drought_template.ini')

    # existing tags to replace in the template file
    projectname_tag = '<projectname>'
    outputnamestr_tag = '<outputnamestr>'
    rootdir_tag = '<rootdir>'
    outputvars_tag = '<outputvars>'
    model_tag = '<model>'
    scenario_tag = '<scenario>'
    task_tag = '<task>'
    outdir_tag = '<outdir>'
    thresholdsdir_tag = '<thresholdsdir>'
    droughtstats_tag = '<droughtstats>'

    # set run name prefix
    run_prefix = ''

    if pet_model_abbrev is not None:
        run_prefix += f"{pet_model_abbrev}_"

    if runoff_model_abbrev is not None:
        run_prefix += f"{runoff_model_abbrev}_"

    if router_model_abbrev is not None:
        run_prefix += f"{router_model_abbrev}_"

    for model in model_list:
        for scenario in scenario_list:
            for i in range(n_configs):

                # construct project name
                project_name = f"{run_prefix}{model}_{scenario}"

                # construct output name string
                output_name_str = f"{project_name}_{i}"

                # xanthos config file output name
                output_file = os.path.join(output_dir, f"{output_name_str}.ini")

                with open(output_file, 'w') as out:
                    with open(template) as get:
                        f = get.read()

                        # replace tag names with dynamic content
                        fx = f.replace(projectname_tag, project_name)
                        fx = fx.replace(outputnamestr_tag, output_name_str)
                        fx = fx.replace(rootdir_tag, xanthos_root_dir)
                        fx = fx.replace(outputvars_tag, xanthos_output_variables)
                        fx = fx.replace(model_tag, model)
                        fx = fx.replace(scenario_tag, scenario)
                        fx = fx.replace(task_tag, str(i))
                        fx = fx.replace(outdir_tag, xanthos_output_dir)
                        fx = fx.replace(thresholdsdir_tag, drought_thresholds_dir)
                        fx = fx.replace(droughtstats_tag, str(generate_drought_stats))

                        out.write(fx)
