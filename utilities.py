# utilities.py
# Assists the data analysis of Strava-data

import numpy as np


def speed_to_pace(x):
    # unit in dataframe: m/s
    # desired unit: min/km
    # 1. m/s^-1 --> s/m
    # 2. s/m/1000*60 --> min/km
    return 1 / x * 1000 / 60


def new_col_pace(df):
    # Add a pace column to df
    df['pace'] = df['avg_speed'].apply(speed_to_pace)
    print('New Column Added: Pace')
    return df


def drop_outlier(df):
    # Drop the outliers
    low_pace = 0.05
    low_hr = 0.10
    high = 0.95

    quant_df_pace = df.quantile([low_pace, high])
    quant_df_hr = df.quantile([low_hr, high])

    def outlier_pace(x):
        cond_low = x < quant_df_pace['pace'].loc[low_pace]
        cond_high = x > quant_df_pace['pace'].loc[high]
        output = cond_low or cond_high
        return output

    def outlier_avg_hr(x):
        cond_low = x < quant_df_hr['avg_hr'].loc[low_hr]
        cond_high = x > quant_df_hr['avg_hr'].loc[high]
        output = cond_low or cond_high
        return output

    # Mask out outliers

    df['outlier_pace'] = df['pace'].apply(outlier_pace)
    df['outlier_avg_hr'] = df['avg_hr'].apply(outlier_avg_hr)

    print('Number of pace outlier: ', len(df[df['outlier_pace'] == True]))
    print('Number of avg_hr outlier: ', len(df[df['outlier_avg_hr'] == True]))

    # Filter outliers and remove mask
    filt_df = df[
        (df['outlier_avg_hr'] == False) &
        (df['outlier_pace'] == False)]

    filt_df = filt_df.drop(['outlier_avg_hr', 'outlier_pace'], axis=1)

    prop_filt = len(filt_df) / len(df)

    print('Proportion of data filtered: {:.2f}'.format(1 - prop_filt))

    return filt_df


def new_col_duration(df):

    def time_to_mins(x):
        return x.seconds / 60

    df['duration'] = df['moving_time'].apply(time_to_mins)
    df = df.drop('moving_time', axis=1)

    return df


def new_col_hr_zone(df):
    # Defining HR Zones
    # TODO: Customize HR Zones

    z1 = np.arange(112, 144, 1)
    z2 = np.arange(145, 155, 1)
    z3 = np.arange(156, 162, 1)
    z4 = np.arange(163, 169, 1)
    z5 = np.arange(170, 173, 1)
    z6 = np.arange(174, 220, 1)

    def avg_hr_to_zone(hr):
        # Round hr to int
        try:
            hr = round(hr)
        except:
            pass

        if hr in z1:
            return 1
        elif hr in z2:
            return 2
        elif hr in z3:
            return 3
        elif hr in z4:
            return 4
        elif hr in z5:
            return 5
        elif hr in z6:
            return 6
        else:
            return None

    df['zone'] = df['avg_hr'].apply(avg_hr_to_zone)
    print('Proportion of data in HR Zone: {:.2f}'.format(
        df['zone'].value_counts().sum() / len(df)))

    return df
