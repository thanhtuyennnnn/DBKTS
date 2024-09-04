import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# URL của trang web chứa dữ liệu
url = 'https://www.sbv.gov.vn/webcenter/portal/vi/menu/trangchu/tk/hdtt/gdttndtcpttt;jsessionid=Q0yUpu1p3jg4Nk_rvWuoBqmutQIitx72h64PI-RUqLku9FH4SPKG!1998637140!-1166094413?_afrLoop=302466521862774#%40%3F_afrLoop%3D302466521862774%26centerWidth%3D80%2525%26leftWidth%3D20%2525%26rightWidth%3D0%2525%26showFooter%3Dfalse%26showHeader%3Dfalse%26_adf.ctrl-state%3Dndkatjg7l_4'

# Gửi yêu cầu GET đến trang web
response = requests.get(url)

# Kiểm tra phản hồi và xử lý dữ liệu
if response.status_code == 200:
    # Phân tích nội dung HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả các hàng (tr) có thuộc tính valign='top' và style='height:30px'
    rows = soup.find_all('tr', valign='top', style='height:30px')

    # Kết nối đến MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['DuLieuTaiChinh']
    collection = db['GiaoDichThanhToan']

    # Danh sách để lưu dữ liệu
    data_list = []

    for row in rows:
        # Tìm tất cả các cột (td) trong mỗi hàng
        columns = row.find_all('td')
        if len(columns) == 3:  # Chỉ lấy các hàng có đúng 3 cột
            # Lấy dữ liệu từ các cột
            data = {
                'Phương tiện thanh toán': columns[0].get_text(strip=True),
                'Số lượng giao dịch': columns[1].get_text(strip=True),
                'Giá trị giao dịch': columns[2].get_text(strip=True)
            }
            data_list.append(data)

    # Chèn dữ liệu vào MongoDB
    if data_list:
        collection.insert_many(data_list)
        print("Dữ liệu đã được chèn vào MongoDB thành công.")
    else:
        print("Không có dữ liệu để chèn.")
else:
    print(f"Error: {response.status_code}")
