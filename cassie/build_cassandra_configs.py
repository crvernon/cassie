import os
from binascii import crc32

from configobj import ConfigObj


class BuildCassandraConfigs:
    """Generate Cassandra configuration files.

    :param model_list:                  List of GCM names to use.
                                        E.g., ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']
    :type model_list:                   list

    :param scenario_list:               List of scenario names to use.
                                        E.g., ['rcp26', 'rcp45', 'rcp60', 'rcp85']
    :type scenario_list:                list

    :param output_dir:                  Full path to the directory to write the files to
    :type output_dir:                   str

    :param runs_per_config:             Number of runs to generate per configuration setup; a.k.a. runs per realization
    :type runs_per_config:              int

    # required global parameters
    :param global_model_interface_jar:  Full path with file name and extension to the GCAM model interface JAR file
    :type global_model_interface_jar:   str

    :param global_dbxml_lib:            Location of the DBXML libraries used by older versions of the ModelInterface
                                        code.
    :type global_dbxml_lib:             str

    :param global_inputdir:             Directory containing general input files.
                                        (OPTIONAL - default is './input-data').  Relative paths will be interpreted
                                        relative to the working directory (even if they don't begin with './')
    :type global_inputdir:              str

    :param global_rgnconfig:            Directory containing region configuration files. Any data that changes with
                                        the region mapping should be in this directory.  The directory will be
                                        converted to an absolute path if it does not start with '/'.  If it starts
                                        with './' the path will be relative to the directory the driver code is running
                                        in; otherwise, it will be relative to inputdir. (OPTIONAL - default is 'rgn32')
    :type global_rgnconfig:             str

    :param xanthos_build:               True if adding Xanthos options to the config file
    :type xanthos_build:                bool

    :param fldgen_build:                True if adding Fldgen options to the config file
    :param fldgen_build:                bool

    # additional Xanthos parameters

    :param xanthos_config_dir:          Directory where the Xanthos configuration files are stored
    :type xanthos_config_dir:           str

    :param xanthos_mpi_weight:          Control for processing order via MPI
    :type xanthos_mpi_weight:           float

    :param xanthos_pet_model_abbrev:    PET model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'trn'
    :type xanthos_pet_model_abbrev:     str

    :param xanthos_runoff_model_abbrev: Runoff model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'abcd'
    :type xanthos_runoff_model_abbrev:  str

    :param xanthos_routing_model_abbrev:Routing model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'mrtm'
    :type xanthos_routing_model_abbrev: str

    # additional Fldgen parameters
    :param fldgen_loadpkgs:                     Flag indicating whether the fldgen and an2month packages need
    :type fldgen_loadpkgs:                      bool

    :param fldgen_ngrids:                       Number of climate fields to generate
    :type fldgen_ngrids:                        int

    :param fldgen_startyr:                      Four digit start year of the simulation
    :type fldgen_startyr:                       int

    :param fldgen_throughyr:                    Four digit through year of the simulation
    :type fldgen_throughyr:                     int

    :param fldgen_mpi_weight:                   Control for processing order via MPI
    :type fldgen_mpi_weight:                    float

    :param fldgen_pkgdir:                       Directory containing R package repositories for fldgen
    :type fldgen_pkgdir:                        str

    :param fldgen_emulator_dir:                 Directory containing the emulator files in the format:
                                                "fldgen-<model>.rds"
    :type fldgen_emulator_dir:                  str

    :param fldgen_tgav_file_dir:                Directory containing the TGAV fiels in the format:
                                                "fldgen-<model>_<scenario>.csv.gz"

    :type fldgen_tgav_file_dir:                 str


    """

    def __init__(self, model_list, scenario_list, output_dir, runs_per_config, global_model_interface_jar, 
                 global_dbxml_lib, global_inputdir='./input-data', global_rgnconfig='rgn32', xanthos_build=True, 
                 fldgen_build=True, **kwargs):

        self.model_list = model_list
        self.scenario_list = scenario_list
        self.output_dir = output_dir
        self.runs_per_config = runs_per_config
        self.global_model_interface_jar=global_model_interface_jar
        self.global_dbxml_lib = global_dbxml_lib
        self.global_inputdir = global_inputdir
        self.global_rgnconfig = global_rgnconfig
        self.xanthos_build = xanthos_build
        self.fldgen_build = fldgen_build

        # xanthos config options
        self.xanthos_config_dir = kwargs.get('xanthos_config_dir', None)
        self.xanthos_mpi_weight = kwargs.get('xanthos_mpi_weight', 2.0)
        self.xanthos_pet_model_abbrev = kwargs.get('xanthos_pet_model_abbrev', None)
        self.xanthos_runoff_model_abbrev = kwargs.get('xanthos_runoff_model_abbrev', None)
        self.xanthos_router_model_abbrev = kwargs.get('xanthos_router_model_abbrev', None)

        # fldgen config options
        self.fldgen_ngrids = kwargs.get('fldgen_ngrids', 1)
        self.fldgen_startyr = kwargs.get('fldgen_startyr', 1861)
        self.fldgen_throughyr = kwargs.get('fldgen_throughyr', 2099)
        self.fldgen_mpi_weight = kwargs.get('fldgen_mpi_weight', 10.0)
        self.fldgen_loadpkgs = kwargs.get('fldgen_loadpkgs', False)
        self.fldgen_pkgdir = kwargs.get('fldgen_pkgdir', '.')
        self.fldgen_emulator_dir = kwargs.get('fldgen_emulator_dir', None)
        self.fldgen_tgav_file_dir = kwargs.get('fldgen_tgav_file_dir', None)

    @staticmethod
    def signify32(x):
        if x > 0x7fffffff:
            return x - 4294967296  # x - 2**32
        else:
            return x

    def build_global(self, config):
        """Build the global section of the config file."""

        config['Global'] = {}
        config['Global']['ModelInterface'] = self.global_model_interface_jar
        config['Global']['DBXMLlib'] = self.global_dbxml_lib
        config['Global']['inputdir'] = self.global_inputdir
        config['Global']['rgnconfig'] = self.global_rgnconfig

        return config

    def build_xanthos(self, config, model, scenario, task):
        """Construct the xanthos section of the config file."""

        config['XanthosComponent'] = {}

        # set run name prefix
        run_prefix = ''

        if self.xanthos_pet_model_abbrev is not None:
            run_prefix += f"{self.xanthos_pet_model_abbrev}_"

        if self.xanthos_runoff_model_abbrev is not None:
            run_prefix += f"{self.xanthos_runoff_model_abbrev}_"

        if self.xanthos_router_model_abbrev is not None:
            run_prefix += f"{self.xanthos_router_model_abbrev}_"

        # construct project name
        xanthos_project_name = f"{run_prefix}{model}_{scenario}"

        # construct output name string
        xanthos_output_name_str = f"{xanthos_project_name}_{task}"

        config['XanthosComponent']['config_file'] = os.path.join(self.xanthos_config_dir, f"{xanthos_output_name_str}.ini")
        config['XanthosComponent']['OutputNameStr'] = xanthos_output_name_str
        config['XanthosComponent']['ProjectName'] = xanthos_project_name
        config['XanthosComponent']['mp.weight'] = self.xanthos_mpi_weight

        return config

    def build_fldgen(self, config, model, scenario):
        """Construct the fldgen section of the config file."""

        # TODO:  depreciate this
        # We're using the old Dirichlet coefficients for now, and the model names
        # on the old versions of the dataset aren't synced up with the new model
        # data.  This table will allow us to translate names until we come up with
        # the final version of the dataset.
        alpha_models = {'GFDL-ESM2M': 'alpha_gfdl_esm2m',
                        'IPSL-CM5A-LR': 'alpha_ipsl_cm5a_lr',
                        'MIROC5': 'alpha_miroc_esm_chem',
                        'HadGEM2-ES': 'alpha_noresm1_m'  # stand-in until we run the HadGEM data in an2month.
                        }

        config['FldgenComponent'] = {}
        
        config['FldgenComponent']['loadpkgs'] = self.fldgen_loadpkgs
        config['FldgenComponent']['pkgdir'] = self.fldgen_pkgdir
        config['FldgenComponent']['emulator'] = os.path.join(self.fldgen_emulator_dir, f"fldgen-{model}.rds")
        config['FldgenComponent']['tgav_file'] = os.path.join(self.fldgen_tgav_file_dir, f"fldgen-{model}_{scenario}.csv.gz")
        config['FldgenComponent']['ngrids'] = self.fldgen_ngrids
        config['FldgenComponent']['scenario'] = scenario
        config['FldgenComponent']['a2mfrac'] = f'{alpha_models[model]}'
        config['FldgenComponent']['startyr'] = self.fldgen_startyr
        config['FldgenComponent']['nyear'] = self.fldgen_throughyr - self.fldgen_startyr + 1
        config['FldgenComponent']['RNGseed'] = self.signify32(crc32(config.filename.encode()))
        config['FldgenComponent']['mp.weight'] = self.fldgen_mpi_weight

        return config

    def build_config(self):
        """Construct Cassandra configuration file from user options."""

        for scenario in self.scenario_list:
            for model in self.model_list:
                for i in range(self.runs_per_config):
                    
                    # instantiate config file
                    config = ConfigObj()
                    
                    # set file output path
                    config.filename = os.path.join(self.output_dir, f"{model}_{scenario}_{i}.cfg")

                    # build required global section
                    config = self.build_global(config)

                    # build xanthos section if desired
                    if self.xanthos_build:
                        config = self.build_xanthos(config, model, scenario, i)

                    # build fldgen section if desired
                    if self.fldgen_build:
                        config = self.build_fldgen(config, model, scenario)

                    # write output config file
                    config.write()
        

def build_cassandra_configs(model_list, scenario_list, output_dir, runs_per_config, global_model_interface_jar,
                            global_dbxml_lib, global_inputdir='./input-data', global_rgnconfig='rgn32',
                            xanthos_build=True, fldgen_build=True, **kwargs):
    """Convenience function to build Cassandra configuration files.

    :param model_list:                  List of GCM names to use.
                                        E.g., ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']
    :type model_list:                   list

    :param scenario_list:               List of scenario names to use.
                                        E.g., ['rcp26', 'rcp45', 'rcp60', 'rcp85']
    :type scenario_list:                list

    :param output_dir:                  Full path to the directory to write the files to
    :type output_dir:                   str

    :param runs_per_config:             Number of runs to generate per configuration setup; a.k.a. runs per realization
    :type runs_per_config:              int

    # required global parameters
    :param global_model_interface_jar:  Full path with file name and extension to the GCAM model interface JAR file
    :type global_model_interface_jar:   str

    :param global_dbxml_lib:            Location of the DBXML libraries used by older versions of the ModelInterface
                                        code.
    :type global_dbxml_lib:             str

    :param global_inputdir:             Directory containing general input files.
                                        (OPTIONAL - default is './input-data').  Relative paths will be interpreted
                                        relative to the working directory (even if they don't begin with './')
    :type global_inputdir:              str

    :param global_rgnconfig:            Directory containing region configuration files. Any data that changes with
                                        the region mapping should be in this directory.  The directory will be
                                        converted to an absolute path if it does not start with '/'.  If it starts
                                        with './' the path will be relative to the directory the driver code is running
                                        in; otherwise, it will be relative to inputdir. (OPTIONAL - default is 'rgn32')
    :type global_rgnconfig:             str

    :param xanthos_build:               True if adding Xanthos options to the config file
    :type xanthos_build:                bool

    :param fldgen_build:                True if adding Fldgen options to the config file
    :param fldgen_build:                bool

    # additional Xanthos parameters

    :param xanthos_config_dir:          Directory where the Xanthos configuration files are stored
    :type xanthos_config_dir:           str

    :param xanthos_mpi_weight:          Control for processing order via MPI
    :type xanthos_mpi_weight:           float

    :param xanthos_pet_model_abbrev:    PET model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'trn'
    :type xanthos_pet_model_abbrev:     str

    :param xanthos_runoff_model_abbrev: Runoff model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'abcd'
    :type xanthos_runoff_model_abbrev:  str

    :param xanthos_routing_model_abbrev:Routing model name abbreviation that will be used in the prefix of the job name
                                        and the output config file name.
                                        E.g., 'mrtm'
    :type xanthos_routing_model_abbrev: str


    # additional Fldgen parameters
    :param fldgen_loadpkgs:                     Flag indicating whether the fldgen and an2month packages need
    :type fldgen_loadpkgs:                      bool

    :param fldgen_ngrids:                       Number of climate fields to generate
    :type fldgen_ngrids:                        int

    :param fldgen_startyr:                      Four digit start year of the simulation
    :type fldgen_startyr:                       int

    :param fldgen_throughyr:                    Four digit through year of the simulation
    :type fldgen_throughyr:                     int

    :param fldgen_mpi_weight:                   Control for processing order via MPI
    :type fldgen_mpi_weight:                    float

    :param fldgen_pkgdir:                       Directory containing R package repositories for fldgen
    :type fldgen_pkgdir:                        str

    :param fldgen_emulator_dir:                 Directory containing the emulator files in the format:
                                                "fldgen-<model>.rds"
    :type fldgen_emulator_dir:                  str

    :param fldgen_tgav_file_dir:                Directory containing the TGAV fiels in the format:
                                                "fldgen-<model>_<scenario>.csv.gz"

    :type fldgen_tgav_file_dir:                 str

    """

    # initialize builder
    cas = BuildCassandraConfigs(model_list,
                                scenario_list,
                                output_dir,
                                runs_per_config,
                                global_model_interface_jar,
                                global_dbxml_lib,
                                global_inputdir=global_inputdir,
                                global_rgnconfig=global_rgnconfig,
                                xanthos_build=xanthos_build,
                                fldgen_build=fldgen_build,
                                **kwargs)

    cas.build_config()
