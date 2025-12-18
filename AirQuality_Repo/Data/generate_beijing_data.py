import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# CẤU HÌNH DỮ LIỆU THỰC TẾ (REAL STATISTICS)
# Nguồn: Beijing Municipal Ecology and Environment Bureau
# ==========================================
BEIJING_REAL_STATS = {
    2013: {'mean_pm25': 89.5, 'trend': 'very_high'},
    2014: {'mean_pm25': 85.9, 'trend': 'high'},
    2015: {'mean_pm25': 80.6, 'trend': 'high'},
    2016: {'mean_pm25': 73.0, 'trend': 'variable'},
    2017: {'mean_pm25': 58.0, 'trend': 'drop'}, # Coal-to-Gas impact
    2018: {'mean_pm25': 51.0, 'trend': 'stable'},
    2019: {'mean_pm25': 42.0, 'trend': 'stable'},
    2020: {'mean_pm25': 38.0, 'trend': 'low'}, # Covid impact
    2021: {'mean_pm25': 33.0, 'trend': 'low'},
    2022: {'mean_pm25': 30.0, 'trend': 'lowest'},
    2023: {'mean_pm25': 32.0, 'trend': 'stable'} # Rebound slightly
}

def generate_hourly_data(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    n_rows = len(date_range)
    
    # 1. Cơ bản: Tạo Index thời gian
    df = pd.DataFrame({
        'Local Time': date_range,
        'City': 'Beijing',
        'Country Code': 'CN',
        'Timezone': 'Asia/Shanghai'
    })
    
    # 2. Tạo đặc trưng Mùa và Giờ (Seasonality)
    # Mùa đông (Tháng 11, 12, 1) thường cao hơn Mùa hè (6, 7, 8)
    month_factor = np.array([1.3, 1.2, 1.0, 0.9, 0.8, 0.7, 0.7, 0.8, 0.9, 1.1, 1.4, 1.5])
    # Giờ cao điểm: Sáng (8-10h) và Tối (18-22h)
    hour_factor = np.array([
        1.0, 0.9, 0.8, 0.8, 0.8, 0.9, # 0-5h
        1.1, 1.3, 1.4, 1.2, 1.0, 0.9, # 6-11h
        0.8, 0.7, 0.7, 0.8, 0.9, 1.1, # 12-17h
        1.3, 1.4, 1.5, 1.4, 1.2, 1.1  # 18-23h
    ])
    
    pm25_values = []
    
    # 3. Tạo dữ liệu dựa trên Target Mean từng năm
    current_year = start_date.year
    
    for i, current_time in enumerate(date_range):
        year = current_time.year
        month = current_time.month
        hour = current_time.hour
        
        # Lấy target mean của năm đó
        target_mean = BEIJING_REAL_STATS.get(year, {'mean_pm25': 30})['mean_pm25']
        
        # Tính toán giá trị cơ sở (Base) dựa trên Mean
        # Base value này sẽ dao động xung quanh Target Mean
        base_value = target_mean 
        
        # Áp dụng yếu tố Mùa và Giờ
        seasonal_val = base_value * month_factor[month-1] * hour_factor[hour]
        
        # Thêm nhiễu ngẫu nhiên (Random Noise) để giống thật
        # Weather impact: Gió, Mưa (Random biến động mạnh)
        weather_noise = np.random.normal(loc=0, scale=target_mean * 0.4) 
        
        final_val = seasonal_val + weather_noise
        
        # Đảm bảo không âm và các giá trị cực đoan (Outliers)
        if final_val < 5: final_val = np.random.randint(5, 15)
        # Năm ô nhiễm thì cho phép max cao hơn
        max_limit = 800 if year <= 2016 else 300
        if final_val > max_limit: final_val = max_limit
            
        pm25_values.append(final_val)

    df['PM25'] = np.round(pm25_values, 1)
    
    # 4. Sinh các chỉ số khác dựa trên PM2.5 (Correlation)
    # AQI (Simplified calculation for simulation)
    df['AQI'] = (df['PM25'] * 1.5 + np.random.randint(-10, 20, n_rows)).clip(20, 500).astype(int)
    
    # Các khí khác (Có tương quan thuận với PM2.5)
    df['PM10'] = (df['PM25'] * 1.6 + np.random.normal(0, 10, n_rows)).clip(10, None).round(1)
    df['CO'] = (df['PM25'] * 10 + 300 + np.random.normal(0, 50, n_rows)).round(1)
    df['NO2'] = (df['PM25'] * 0.6 + 20 + np.random.normal(0, 5, n_rows)).round(1)
    df['SO2'] = (df['PM25'] * 0.4 + 5 + np.random.normal(0, 2, n_rows)).round(1)
    
    # Ozone (O3) thường nghịch biến với NO2 (cao vào mùa hè, giữa trưa)
    df['O3'] = np.random.uniform(20, 100, n_rows).round(1)
    
    # Thời tiết (Giả lập để không bị NULL)
    df['Temperature'] = np.random.uniform(-5, 35, n_rows).round(1)
    df['RelativeHumidity'] = np.random.uniform(20, 90, n_rows).round(1)
    df['Pressure'] = np.random.uniform(990, 1030, n_rows).round(1)
    df['WindSpeed'] = np.random.uniform(0, 15, n_rows).round(1)
    df['Clouds'] = np.random.randint(0, 100, n_rows)
    df['Precipitation'] = 0.0 # Giả định đơn giản
    df['UVIndex'] = np.random.randint(0, 11, n_rows).astype(float) # Đảm bảo float

    # Đổi tên cột cho khớp với file Hà Nội (Nếu cần Mapping trong SSIS)
    # Ở đây giữ nguyên format cũ của script để tránh lỗi SSIS mapping cũ
    # (Local Time,City,Country Code,Timezone,PM25,AQI,SO2,NO2,CO,O3,PM10,Temperature,Humidity,WindSpeed,Pressure,Precipitation,Clouds,UV Index)
    
    df = df.rename(columns={'RelativeHumidity': 'Humidity', 'UVIndex': 'UV Index'})
    
    # Reorder columns to match destination expectations if needed, 
    # but based on previous CSV, the order was:
    cols = ['Local Time','City','Country Code','Timezone','PM25','AQI','SO2','NO2','CO','O3','PM10','Temperature','Humidity','WindSpeed','Pressure','Precipitation','Clouds','UV Index']
    df = df[cols]
    
    return df

if __name__ == "__main__":
    print("Generating Authentic Simulated Beijing Data (2013-2023)...")
    # Generate data
    df = generate_hourly_data(datetime(2013, 1, 1), datetime(2023, 12, 31, 23))
    
    # Save
    output_path = 'beijing_air_quality_2013_2023.csv' # Overwrite cũ
    df.to_csv(output_path, index=False)
    print(f"Data generated successfully: {output_path}")
    print(f"Total rows: {len(df)}")
    print("Annual Averages Check:")
    print(df.groupby(df['Local Time'].dt.year)['PM25'].mean())
