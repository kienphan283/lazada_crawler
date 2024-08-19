import http.client
import json
import pandas as pd
from pandas import json_normalize

def fetch_data(start_page=1):
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://www.lazada.vn/may-tinh-bang/?spm=a2o4n.searchlistcategory.cate_1.2.6bd7564frDscGu'
    }

    conn = http.client.HTTPSConnection("www.lazada.vn")

    for page_num, _ in enumerate(range(start_page, 48), start=start_page):
        url = f"https://www.lazada.vn/may-tinh-bang/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1.2.6bd7564frDscGu"

        try:
            conn.request("GET", url, headers=headers)
            res = conn.getresponse()
            data = res.read()

            if res.status != 200:
                print(f"Failed to fetch data for page {page_num}, status code: {res.status}")
                # Xử lý lỗi HTTP ở đây (ví dụ: thử lại hoặc bỏ qua)
                continue

            try:
                json_data = json.loads(data.decode('utf-8'))
                data_info = json_data['mods']

                list_data = json_normalize(data_info, record_path=['listItems'])

                # Ghi dữ liệu vào file ở chế độ append
                with open("Electronic Device_tablet.txt", 'a', encoding='utf-8') as f:
                    f.write(list_data.to_string(index=False))

                print(f"Đã lưu dữ liệu trang {page_num} vào file 'Electronic Device_tablet.txt'")

            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON for page {page_num}: {e}")
                # Xử lý lỗi JSON ở đây (ví dụ: in ra nội dung phản hồi)

        finally:
            if page_num == 48:
                conn.close()

# Gọi hàm để lấy dữ liệu
fetch_data(start_page=1)