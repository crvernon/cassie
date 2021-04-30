import cassie

# model list to process
model_list = ['IPSL-CM5A-LR', 'GFDL-ESM2M', 'HadGEM2-ES', 'MIROC5']

# scenarios to process
scenario_list = ['rcp26', 'rcp45', 'rcp60', 'rcp85']

#
output_dir = '/Users/d3y010/Desktop/cas'

#
runs_per_config = 4

#
global_model_interface_jar = '<your path>'

#
global_dbxml_lib = '<your path>'

#
xanthos_config_dir = '<your dir>'

#
xanthos_pet_model_abbrev = 'trn'

#
xanthos_runoff_model_abbrev = 'abcd'

#
fldgen_startyr = 1861

#
fldgen_throughyr = 2099

#
fldgen_pkgdir = '.'

#
fldgen_emulator_dir = '<your dir>'

#
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
