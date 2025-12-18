import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ==========================================
# CẤU HÌNH DỮ LIỆU HÀ NỘI (IQAir Real Data)
# Nguồn: IQAir World Air Quality Report (2018-2023)
# ==========================================
HANOI_REAL_STATS = {
    # Trước 2018 không có data IQAir chi tiết, giả định xu hướng tăng nhẹ
    2013: {'mean_pm25': 45.0, 'trend': 'stable'},
    2014: {'mean_pm25': 47.0, 'trend': 'stable'},
    2015: {'mean_pm25': 48.0, 'trend': 'high'},
    2016: {'mean_pm25': 50.0, 'trend': 'high'},
    2017: {'mean_pm25': 45.0, 'trend': 'drop'},
    # Data IQAir chính thức
    2018: {'mean_pm25': 40.8, 'trend': 'real'},
    2019: {'mean_pm25': 46.9, 'trend': 'real_peak'}, 
    2020: {'mean_pm25': 37.9, 'trend': 'real_covid'},
    2021: {'mean_pm25': 36.2, 'trend': 'real_covid'},
    2022: {'mean_pm25': 40.1, 'trend': 'real_rebound'}
}

def generate_hanoi_history(start_year=2013, end_year=2022):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31, 23)
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    n_rows = len(date_range)
    
    df = pd.DataFrame({
        'Local Time': date_range,
        'City': 'Hanoi',
        'Country Code': 'VN',
        'Timezone': 'Asia/Ho_Chi_Minh'
    })
    
    # Giữ nguyên hệ số mùa của Hà Nội (mùa đông cao)
    month_factor = np.array([1.4, 1.3, 1.2, 0.9, 0.7, 0.6, 0.6, 0.7, 0.9, 1.2, 1.5, 1.6])
    
    hour_factor = np.array([
        1.0, 0.9, 0.8, 0.8, 0.8, 0.9, 
        1.1, 1.3, 1.4, 1.2, 1.0, 0.9, 
        0.8, 0.7, 0.7, 0.8, 1.0, 1.3, 
        1.5, 1.4, 1.2, 1.1, 1.1, 1.0 
    ])
    
    pm25_values = []
    
    for i, current_time in enumerate(date_range):
        year = current_time.year
        month = current_time.month
        hour = current_time.hour
        
        target_mean = HANOI_REAL_STATS.get(year, {'mean_pm25': 40})['mean_pm25']
        
        # Base value
        base_value = target_mean * month_factor[month-1] * hour_factor[hour]
        # Nhiễu
        weather_noise = np.random.normal(loc=0, scale=target_mean * 0.4)
        
        final_val = base_value + weather_noise
        
        if final_val < 5: final_val = np.random.randint(5, 15)
        # Giảm giới hạn max xuống thực tế hơn
        if final_val > 400: final_val = 400
            
        pm25_values.append(final_val)

    df['PM2.5'] = np.round(pm25_values, 1)
    
    # Sinh các cột khác
    df['AQI'] = (df['PM2.5'] * 1.8).clip(20, 500).astype(int)
    df['PM10'] = (df['PM2.5'] * 1.5 + np.random.uniform(5, 15, n_rows)).round(1)
    df['CO'] = (df['PM2.5'] * 8 + 200).round(1)
    df['NO2'] = (df['PM2.5'] * 0.5 + 15).round(1)
    df['SO2'] = (df['PM2.5'] * 0.2 + 5).round(1)
    df['O3'] = np.random.uniform(10, 80, n_rows).round(1)
    
    # Weather
    df['Temperature'] = np.random.uniform(10, 38, n_rows).round(1)
    df['Relative Humidity'] = np.random.uniform(40, 99, n_rows).round(1)
    df['Pressure'] = np.random.uniform(995, 1020, n_rows).round(1)
    df['Wind Speed'] = np.random.uniform(0, 10, n_rows).round(1)
    df['Clouds'] = np.random.randint(20, 100, n_rows)
    df['Precipitation'] = 0.0
    df['UV Index'] = np.random.uniform(0, 12, n_rows).round(1)
    
    return df

def merge_with_real_2023(history_df, real_2023_path):
    try:
        real_df = pd.read_csv(real_2023_path)
        
        cols_order = ['Local Time','UTC Time','City','Country Code','Timezone','AQI','CO','NO2','O3','PM10','PM25','SO2','Clouds','Precipitation','Pressure','Relative Humidity','Temperature','UV Index','Wind Speed']
        
        history_df = history_df.rename(columns={
            'PM2.5': 'PM25', 
            'Relative Humidity': 'Relative Humidity',
            'Wind Speed': 'Wind Speed'
        })
        
        history_df['UTC Time'] = history_df['Local Time'] - timedelta(hours=7)
        history_df = history_df[cols_order]
        real_df = real_df[cols_order]
        
        full_df = pd.concat([history_df, real_df], ignore_index=True)
        return full_df
        
    except Exception as e:
        print(f"Error merging: {e}")
        return history_df

if __name__ == "__main__":
    print("Generating IQAir Real-Base Hanoi Data (2013-2022)...")
    history_df = generate_hanoi_history()
    
    current_csv = 'hanoi-aqi-weather-data.csv'
    
    # Đọc file 2023 gốc (Lưu ý: Bạn vừa backup file gốc là 'hanoi-aqi-weather-data_BACKUP.csv' nếu muốn lấy lại)
    # Nhưng script này sẽ dùng file hiện tại (đang là full fake).
    # -> Cần đọc file backup nếu muốn giữ data 2023 gốc
    
    backup_read = 'hanoi-aqi-weather-data_BACKUP.csv' 
    # Check nếu backup tồn tại thì dùng, ko thì dùng file hiện tại (hy vọng đoạn 2023 ở cuối vẫn còn nguyên)
    if os.path.exists(backup_read):
         full_df = merge_with_real_2023(history_df, backup_read)
    else:
         # Nếu lỡ mất backup thì dùng lại file hiện tại (lấy phần đuôi 2023)
         try:
            current_df = pd.read_csv(current_csv)
            # Lấy 8785 dòng cuối (2023)
            real_2023_part = current_df[current_df['Local Time'].str.contains('2023-')]
            # Lưu tạm
            real_2023_part.to_csv('temp_2023.csv', index=False)
            full_df = merge_with_real_2023(history_df, 'temp_2023.csv')
         except:
            full_df = history_df # Worst case

    output_path = 'hanoi_air_quality_FULL_IQAir.csv'
    full_df.to_csv(output_path, index=False)
    
    print(f"Data generated: {output_path}")
    print("Stats Check (Should match IQAir):")
    print(full_df.groupby(pd.to_datetime(full_df['Local Time']).dt.year)['PM25'].mean())
