import scone_recursive_parser as srp
import par_to_controller as ptc
import numpy as np

# import controller file to string
controller = srp.controller_file_to_string("../models/gait_controllers/new_controller_TAV_GAS.txt")

# convert controller string to recursive dictionnary
dict = srp.dict_recursive_split(controller)

# convert controller string to recursive pandas Series
series = srp.series_recursive_split(controller)

""""# get, set then get value again of existant key
print(srp.get_key(series, "KV","Swing Landing", "soleus"))
srp.set_key(series, "KV", "99","Swing Landing", "soleus")
print(srp.get_key(series, "KV","Swing Landing", "soleus"))"""

# export series to scone files
#srp.series_to_scone_file(series,"../exports/new_TAV_GAS_srp_out.scone")

""""# get series of reflexes verifying certain states, a target muscle and a source muscle
found_by_states_target_source = srp.find_by_states_target_source(cx_series, "Swing, Landing", "soleus")
print(found_by_states_target_source.to_json(indent = 4))

found_by_states_target_source[1]['Selim'] = 'hello'

found_by_states_target_source = srp.find_by_states_target_source(cx_series, "Swing, Landing", "soleus")
print(found_by_states_target_source.to_json(indent = 4))"""

# apply par file to controller with new value ranges.
par_file = '../models/new_TAV_GAS_base_files/new_TAV_GAS_init.par'
min_max_ratio = 0.01  # new max/min = value*(1 +/- min_max_ratio)
std_ratio = 1  # new std = value*std_ratio

series_new_range = ptc.apply_par_file_to_series_with_new_range_2(par_file, series, min_max_ratio)  # same std
#series_new_range = ptc.apply_par_file_to_series_with_new_range(par_file, series, min_max_ratio, std_ratio)
#series_fixed_values = ptc.apply_par_file_to_series_with_fixed_values(par_file, series)

# generate scone folders with multiple combination of controller files.
key_dict_0 = {'key_name': 'KV', 'states': 'LateStance EarlyStance Liftoff', 'target': ['soleus', 'gastroc'],
              'source': None, 'key_values': range(10,100,10)}

key_dict_1 = {'key_name': 'KV', 'states': 'Swing Landing', 'target': ['soleus', 'gastroc'], 'source': None,
              'key_values': range(10,100,10)}

key_dict_list = [key_dict_0, key_dict_1]

output_folder_path = '../exports/new_TAV_GAS_soleus_gastroc_KV_2D_stance_swing'
scone_base_files_path = '../models/new_TAV_GAS_base_files'
scone_main_file_name = 'scone_main.scone'

srp.generate_controllers_with_key_combinations_2(series_new_range, key_dict_list,
                                               output_folder_path, scone_base_files_path, 
                                               scone_main_file_name)
