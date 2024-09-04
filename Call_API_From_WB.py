import wbdata
import pandas as pd
from pymongo import MongoClient

# Thiết lập quốc gia và các mã chỉ số
country_code = 'VNM'  # Mã quốc gia cho Việt Nam
indicators = {
    'GFDD.OI.06': '5-bank asset concentration',
    'GFDD.EI.07': 'Bank cost to income ratio (%)',
    'GFDD.EI.02': 'Bank lending-deposit spread'
}

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['world_bank_data']  # Tạo/Chọn cơ sở dữ liệu
collection = db['financial_indicators']  # Tạo/Chọn bảng

# Lấy dữ liệu riêng lẻ cho từng chỉ số và chèn vào MongoDB
for code, name in indicators.items():
    df_single = wbdata.get_dataframe({code: name}, country=country_code)
    data = df_single.reset_index().to_dict('records')  # Chuyển DataFrame thành danh sách dictionary
    if data:  # Kiểm tra xem dữ liệu có rỗng không
        collection.insert_many(data)  # Chèn dữ liệu vào MongoDB

# Sau đó hợp nhất lại các dữ liệu này nếu cần
df_combined = wbdata.get_dataframe(indicators, country=country_code)
df_filtered = df_combined.loc['2000':'2021']
combined_data = df_filtered.reset_index().to_dict('records')  # Chuyển DataFrame thành danh sách dictionary

if combined_data:  # Kiểm tra xem dữ liệu có rỗng không
    collection.insert_many(combined_data)  # Chèn dữ liệu hợp nhất vào MongoDB

print("Dữ liệu đã được chèn vào MongoDB thành công!")
