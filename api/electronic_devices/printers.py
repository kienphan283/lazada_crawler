import http.client
import json
import pandas as pd
from pandas import json_normalize

def process_and_save_data(data, sub_subcategory_name, page_num):
    try:
        json_data = json.loads(data.decode('utf-8'))
        data_info = json_data.get('mods', {})  # Lấy từ điển 'mods' nếu tồn tại, nếu không trả về từ điển rỗng

        # Duyệt qua các mục trong 'listItems' (nếu tồn tại)
        for item in data_info.get('listItems', []):
            # Xử lý và lưu từng trường dữ liệu
            save_field_to_csv(item, 'name', sub_subcategory_name)
            save_field_to_csv(item, 'location', sub_subcategory_name)
            save_field_to_csv(item, 'brandName', sub_subcategory_name)
            save_field_to_csv(item, 'originalPrice', sub_subcategory_name)
            save_field_to_csv(item, 'sellerName', sub_subcategory_name)
            save_field_to_csv(item, 'discount', sub_subcategory_name)
            save_field_to_csv(item, 'image', sub_subcategory_name)
            save_field_to_csv(item, 'priceShow', sub_subcategory_name)
            save_field_to_csv(item, 'review', sub_subcategory_name)
            save_field_to_csv(item, 'ratingScore', sub_subcategory_name)
        
        print(f"Đã xử lý dữ liệu trang {page_num} cho {sub_subcategory_name}")

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON for page {page_num}: {e}")
            # Xử lý lỗi JSON ở đây (ví dụ: in ra nội dung phản hồi)

def save_field_to_csv(item, field_name, sub_subcategory_name):
    if field_name in item:
        extracted_value = item[field_name]
        print(f"Đã tìm thấy {field_name}: {extracted_value}")
        with open(f"{field_name}_{sub_subcategory_name}.csv", 'a', encoding='utf-8') as f:
            f.write(extracted_value + "\n")

def crawl_sub_subcategory(sub_subcategory_name, start_page=1, end_page=34, referer="", url=""):
    headers = {
        'Accept': 'application/json',
        'Referer': referer
    }
    conn = http.client.HTTPSConnection("www.lazada.vn")

    for page_num, _ in enumerate(range(start_page, end_page+1), start=start_page):
        url = url.format(page_num=page_num)

        try:
            conn.request("GET", url, headers=headers)
            res = conn.getresponse()
            data = res.read()

            if res.status != 200:
                print(f"Failed to fetch data for page {page_num}, status code: {res.status}")
                # Xử lý lỗi HTTP ở đây (ví dụ: thử lại hoặc bỏ qua)
                continue

            process_and_save_data(data, sub_subcategory_name, page_num)

        finally:
            if page_num == end_page+1:
                conn.close()

# Gọi hàm để lấy dữ liệu
crawl_sub_subcategory("printers", end_page=56, referer="https://www.lazada.vn/may-in/?spm=a2o4n.searchlistcategory.cate_1_10.1.834f564fvSg8Us", url="https://www.lazada.vn/may-in/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_10.1.834f564fvSg8Us")
crawl_sub_subcategory("scanners", end_page=102, referer="https://www.lazada.vn/may-scan/?spm=a2o4n.searchlistcategory.cate_1_10.2.7af5564f14wHUU", url="https://www.lazada.vn/may-scan/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_10.2.7af5564f14wHUU")
crawl_sub_subcategory("3d_printing", end_page=24, referer="https://www.lazada.vn/may-in-3d/?spm=a2o4n.10441748.cate_1_10.4.796847e7sFKbvL", url="https://www.lazada.vn/may-in-3d/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.10441748.cate_1_10.4.796847e7sFKbvL")
crawl_sub_subcategory("printer_cutter", end_page=4, referer="https://www.lazada.vn/may-in-cat/?spm=a2o4n.searchlistcategory.cate_1_10.5.567c564fOBeXgl", url="https://www.lazada.vn/may-in-cat/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_10.5.567c564fOBeXgl")
crawl_sub_subcategory("ink", end_page=49, referer="https://www.lazada.vn/muc-in/?spm=a2o4n.searchlistcategory.cate_1_10.6.28ca564fu85J85", url="https://www.lazada.vn/muc-in/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_10.6.28ca564fu85J85")
crawl_sub_subcategory("printer_memory_modules", end_page=7, referer="https://www.lazada.vn/bo-nho-may-in/?spm=a2o4n.searchlistcategory.cate_1_10.7.4ad1564fnFCVM5", url="https://www.lazada.vn/bo-nho-may-in/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_10.7.4ad1564fnFCVM5")
