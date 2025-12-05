import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Cấu hình tham số thực tế của Bắc Kinh (Dựa trên báo cáo UN Environment)
# 2013: PM2.5 ~ 90, SO2 ~ 25 (Ô nhiễm nặng do than)
# 2023: PM2.5 ~ 30, SO2 ~ 3 (Cải thiện rõ rệt)

start_date = datetime(2013, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='H')

n_rows = len(date_range)

# Hàm tạo xu hướng giảm dần (Linear Decay) + Biến động theo mùa (Mùa đông cao hơn)
def generate_trend(start_val, end_val, noise_level, seasonal_amp):
    # Xu hướng tuyến tính giảm dần theo thời gian
    trend = np.linspace(start_val, end_val, n_rows)
    
    # Biến động theo mùa (Mùa đông index thấp/cao tùy bán cầu, ở đây giả lập chu kỳ sin)
    # Bắc Kinh ô nhiễm nhất vào mùa đông (tháng 12, 1)
    seasonal = seasonal_amp * np.cos(2 * np.pi * (date_range.dayofyear) / 365)
    
    # Nhiễu ngẫu nhiên
    noise = np.random.normal(0, noise_level, n_rows)
    
    data = trend + seasonal + noise
    return np.maximum(data, 0) # Không âm

# Tạo dữ liệu
df = pd.DataFrame({
    'Local Time': date_range,
    'City': 'Beijing',
    'Country Code': 'CN',
    'Timezone': 'Asia/Shanghai'
})

# 1. PM2.5: Giảm mạnh từ 90 xuống 30 (Chính sách kiểm soát xe & bụi)
df['PM25'] = generate_trend(90, 30, 15, 20)
df['AQI'] = df['PM25'] * 1.5 + np.random.normal(0, 10, n_rows) # AQI thường tương quan PM2.5

# 2. SO2: Giảm cực mạnh từ 40 xuống 3 (Chính sách bỏ than đá - Coal Ban)
df['SO2'] = generate_trend(40, 3, 5, 10)

# 3. NO2: Giảm vừa phải từ 50 xuống 30 (Kiểm soát xe cộ nhưng xe tăng lên)
df['NO2'] = generate_trend(50, 30, 10, 10)

# 4. CO: Giảm nhẹ
df['CO'] = generate_trend(1500, 800, 200, 100)

# 5. Các chỉ số khác (Giả định ổn định hoặc biến động tự nhiên)
df['O3'] = np.random.normal(40, 15, n_rows) # Ozone đôi khi tăng do phản ứng hóa học
df['PM10'] = df['PM25'] * 1.8 # Tương quan bụi lớn
df['Temperature'] = 15 + 15 * np.sin(2 * np.pi * (date_range.dayofyear - 100) / 365) + np.random.normal(0, 3, n_rows)
df['Humidity'] = np.random.uniform(20, 90, n_rows)
df['WindSpeed'] = np.random.uniform(0, 15, n_rows)
df['Pressure'] = np.random.normal(1013, 10, n_rows)
df['Precipitation'] = np.where(np.random.rand(n_rows) > 0.9, np.random.uniform(0, 20, n_rows), 0)
df['Clouds'] = np.random.randint(0, 100, n_rows)
df['UV Index'] = np.maximum(0, 5 * np.sin(2 * np.pi * (date_range.dayofyear - 80) / 365))

# Làm tròn số
cols_to_round = ['AQI', 'PM25', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'Temperature', 'Humidity']
df[cols_to_round] = df[cols_to_round].round(1)

# Lưu file
output_path = 'd:/VKU_learning/HK5/KhoDuLieu/BigProject/repo/AirQuality_Repo/Data/beijing_air_quality_2013_2023.csv'
df.to_csv(output_path, index=False)

print(f"Đã tạo dữ liệu Bắc Kinh tại: {output_path}")
print(f"Tổng số dòng: {n_rows}")
