import requests
from pymongo import MongoClient

# URL API
url = ('http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/FAS/A.VN.FCSODUG_GDP_PT?'
       'startPeriod=2004&endPeriod=2022')

# Gửi yêu cầu GET tới API
response = requests.get(url)

# Kiểm tra phản hồi và xử lý dữ liệu
if response.status_code == 200:
    data = response.json()

    # Trích xuất các giá trị dữ liệu
    observations = data['CompactData']['DataSet']['Series']['Obs']

    # Kết nối đến MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['imf_data']  # Tạo cơ sở dữ liệu 'imf_data'
    collection = db['financial_services']  # Tạo collection 'financial_services'

    # Chuẩn bị dữ liệu để chèn vào MongoDB
    documents = []
    for obs in observations:
        document = {
            'year': obs['@TIME_PERIOD'],
            'value': float(obs['@OBS_VALUE'])
        }
        documents.append(document)

    # Chèn dữ liệu vào collection
    collection.insert_many(documents)

    print("Dữ liệu đã được thêm vào MongoDB thành công.")
else:
    print(f"Error: {response.status_code}")
