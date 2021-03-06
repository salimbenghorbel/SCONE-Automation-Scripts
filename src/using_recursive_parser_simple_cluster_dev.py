import scone_recursive_parser as srp
import par_to_controller as ptc
import numpy as np

# import controller file to string
complex_controller = srp.controller_file_to_string("../models/gait_controllers/cx_gait_controller.txt")
solLV_controller = srp.controller_file_to_string("../models/gait_controllers/sp_gait_controller.txt")
geyer_controller = srp.controller_file_to_string("../models/gait_controllers/geyer_gait_controller.txt")
geyer_solLV_controller = srp.controller_file_to_string("../models/gait_controllers/geyer_solLV_gait_controller.txt")
geyer_couplings_controller = srp.controller_file_to_string("../models/gait_controllers/geyer_couplings_gait_controller.txt")

# convert controller string to recursive dictionnary
cx_dict = srp.dict_recursive_split(complex_controller)
sp_dict = srp.dict_recursive_split(solLV_controller)
ge_dict = srp.dict_recursive_split(geyer_controller)
ge_solLV_dict = srp.dict_recursive_split(geyer_solLV_controller)
ge_couplings_dict = srp.dict_recursive_split(geyer_couplings_controller)

# convert controller string to recursive pandas Series
cx_series = srp.series_recursive_split(complex_controller)
sp_series = srp.series_recursive_split(solLV_controller)
ge_series = srp.series_recursive_split(geyer_controller)
ge_solLV_series = srp.series_recursive_split(geyer_solLV_controller)
ge_couplings_series = srp.series_recursive_split(geyer_couplings_controller)

# get, set then get value again of existant key
print(srp.get_key(cx_series, "C0","Swing, Landing", "soleus"))
srp.set_key(cx_series, "C0", "99","Swing, Landing", "soleus")
print(srp.get_key(cx_series, "C0","Swing, Landing", "soleus"))

# export series to scone files
srp.series_to_scone_file(cx_series,"../exports/cx_srp_out.scone")
srp.series_to_scone_file(sp_series,"../exports/sp_srp_out.scone")
srp.series_to_scone_file(ge_series,"../exports/ge_srp_out.scone")


# get non existant key
print(srp.get_key(cx_series, "nn","Swing, Landing", "soleus"))

# try to set non existant key
try:
    srp.set_key(cx_series, "nn", "99","Swing, Landing", "soleus")
except  AssertionError as err:
    print(err)
    
# get series of reflexes verifying certain states, a target muscle and a source muscle
found_by_states_target_source = srp.find_by_states_target_source(cx_series, "Swing, Landing", "soleus")
print(found_by_states_target_source.to_json(indent = 4))

found_by_states_target_source[1]['Selim'] = 'hello'

found_by_states_target_source = srp.find_by_states_target_source(cx_series, "Swing, Landing", "soleus")
print(found_by_states_target_source.to_json(indent = 4))



# apply par file to geyer_solLV with new value ranges.
par_file_solLV = '../models/geyer_solLV_base_files/init_geyer_good_signs.par'
min_max_ratio = 0.01 # new max/min = value*(1 +/- min_max_ratio)
std_ratio = 1 # new std = value*std_ratio

ge_solLV_series_new_range = ptc.apply_par_file_to_series_with_new_range(par_file_solLV, ge_solLV_series, min_max_ratio, std_ratio)
ge_solLV_series_fixed_values = ptc.apply_par_file_to_series_with_fixed_values(par_file_solLV, ge_solLV_series)

# generate scone folders with multiple combination of controller files.
# solLV model
key_dict_0 = {'key_name': 'KV', 'states': 'LateStance EarlyStance Liftoff', 'target': 'soleus',
              'source': None, 'key_values': [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]}

key_dict_1 = {'key_name': 'KV', 'states': 'Swing Landing', 'target': 'soleus',
              'source': None, 'key_values': [0,1,2,3,4,5,6,7]}

key_dict_list = [key_dict_0, key_dict_1 ]


output_folder_path = '../exports/geyer_solLV_multiobjective_stance_KV_swing_KV'
scone_base_files_path = '../models/cluster/geyer_solLV_multiobjective_base_files_dev'
scone_main_file_name = 'scone_main.scone'

srp.generate_controllers_with_key_combinations(ge_solLV_series_new_range, key_dict_list, 
                                               output_folder_path, scone_base_files_path, 
                                               scone_main_file_name)
