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
crawl_sub_subcategory("traditional_laptops", end_page=34, referer="https://www.lazada.vn/laptop-van-phong/?spm=a2o4n.searchlistcategory.cate_1_3.2.2e60564fzXLs3o", url="https://www.lazada.vn/laptop-co-ban/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.SearchListCategory.cate_1_3.1.6af4zbk9zbk93P")
crawl_sub_subcategory("gaming_laptops", end_page=42, referer="https://www.lazada.vn/laptop-giai-tri/?spm=a2o4n.searchlistcategory.cate_1_3.2.2e60564fzXLs3o", url="https://www.lazada.vn/laptop-giai-tri/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_3.2.2e60564fzXLs3o")
crawl_sub_subcategory("laptops_2_in_1", end_page=8, referer="https://www.lazada.vn/dong-2-in-1/?spm=a2o4n.searchlistcategory.cate_1_3.3.2f70564fh0y2GP", url="https://www.lazada.vn/dong-2-in-1/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_3.3.2f70564fh0y2GP")