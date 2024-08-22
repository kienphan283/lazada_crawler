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
crawl_sub_subcategory("laser_pointers", end_page=102, referer="https://www.lazada.vn/but-laser/?spm=a2o4n.searchlistcategory.cate_2_3.1.767b2368UqH5SH", url="https://www.lazada.vn/but-laser/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_3.1.767b2368UqH5SH")
crawl_sub_subcategory("metal_detectors", end_page=32, referer="https://www.lazada.vn/may-do-kim-loai/?spm=a2o4n.searchlistcategory.cate_2_3.2.1320564fXVfNqB", url="https://www.lazada.vn/may-do-kim-loai/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_3.2.1320564fXVfNqB")
crawl_sub_subcategory("dictionaries_&_translators", end_page=4, referer="https://www.lazada.vn/kim-tu-dien-va-may-thong-dich/?spm=a2o4n.searchlistcategory.cate_2_3.3.61067f99DtdmEB", url="https://www.lazada.vn/kim-tu-dien-va-may-thong-dich/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_3.3.61067f99DtdmEB")
crawl_sub_subcategory("universal_chargers", end_page=38, referer="https://www.lazada.vn/bo-sac-da-nang-thiet-bi-so/?spm=a2o4n.searchlistcategory.cate_2_3.4.f869624bucqxXa", url="https://www.lazada.vn/bo-sac-da-nang-thiet-bi-so/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_3.4.f869624bucqxXa")
crawl_sub_subcategory("graphic_tablets", end_page=28, referer="https://www.lazada.vn/bang-ve/?spm=a2o4n.searchlistcategory.cate_2_3.5.6881564fbuhy4P", url="https://www.lazada.vn/bang-ve/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_3.5.6881564fbuhy4P")
crawl_sub_subcategory("walkie_talkies", end_page=102, referer="https://www.lazada.vn/bo-dam-thiet-bi-so/?spm=a2o4n.searchlistcategory.cate_2_3.6.66fc3d68WFWIUA", url="https://www.lazada.vn/bo-dam-thiet-bi-so/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_3.6.66fc3d68WFWIUA")
