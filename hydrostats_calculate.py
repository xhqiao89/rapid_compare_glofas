import hydrostats.metrics as hm
import numpy as np
import csv

with open("/home/sherry/Downloads/United States/ID_ts_trans.csv", 'r') as my_file:
    reader = csv.reader(my_file)
    my_list = list(reader)
    # print(my_list[0])

low = np.array(my_list[0], dtype=np.float64)
med = np.array(my_list[1], dtype=np.float64)
high = np.array(my_list[2], dtype=np.float64)
obs = np.array(my_list[3], dtype=np.float64)

mean_aboslute_error1 = hm.mae(low, med)
mean_aboslute_error2 = hm.mae(low, high)
mean_aboslute_error3 = hm.mae(med, high)
kge1 = hm.kge_2012(low, obs)
kge2 = hm.kge_2012(med, obs)
kge3 = hm.kge_2012(high, obs)

print(mean_aboslute_error1)
print(mean_aboslute_error2)
print(mean_aboslute_error3)
print(kge1)
print(kge2)
print(kge3)
