import numpy as np
import pandas as pd
from nptdms import TdmsFile

tdms_file = TdmsFile('UNH-01_R131_07_05_2017_03_01_40_Decimate_All.tdms')

for key, value in tdms_file.objects().items():
    print(key)