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
crawl_sub_subcategory("dslr", end_page=21, referer="https://www.lazada.vn/may-anh-slr/?spm=a2o4n.searchlistcategory.cate_1_7.1.6266564fnC8BJc", url="https://www.lazada.vn/may-anh-slr/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.1.6266564fnC8BJc")
crawl_sub_subcategory("mirrorless", end_page=8, referer="https://www.lazada.vn/may-anh-khong-guong-lat/?spm=a2o4n.searchlistcategory.cate_1_7.2.2e4b564fcPCNya", url="https://www.lazada.vn/may-anh-khong-guong-lat/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.2.2e4b564fcPCNya")
crawl_sub_subcategory("point_&_shoot", end_page=60, referer="https://www.lazada.vn/may-anh-du-lich/?spm=a2o4n.searchlistcategory.cate_1_7.3.59a0564fcMUIOQ", url="https://www.lazada.vn/may-anh-du-lich/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.3.59a0564fcMUIOQ")
crawl_sub_subcategory("bridge", end_page=2, referer="https://www.lazada.vn/may-anh-sieu-zoom/?spm=a2o4n.searchlistcategory.cate_1_7.4.2a00564fbtEyww", url="https://www.lazada.vn/may-anh-sieu-zoom/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.4.2a00564fbtEyww")
crawl_sub_subcategory("drones", end_page=47, referer="https://www.lazada.vn/may-bay-co-camera/?spm=a2o4n.searchlistcategory.cate_1_7.5.2d3d564fagfDcB", url="https://www.lazada.vn/may-bay-co-camera/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.5.2d3d564fagfDcB")
crawl_sub_subcategory("instant_camera", end_page=21, referer="https://www.lazada.vn/may-anh-chup-lay-ngay/?spm=a2o4n.searchlistcategory.cate_1_7.6.6843564f9hgC18", url="https://www.lazada.vn/may-anh-chup-lay-ngay/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.6.6843564f9hgC18")
crawl_sub_subcategory("lenses", end_page=102, referer="https://www.lazada.vn/cac-loai-ong-kinh/?spm=a2o4n.searchlistcategory.cate_1_7.7.6e68564fo0ASjy", url="https://www.lazada.vn/cac-loai-ong-kinh/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.7.6e68564fo0ASjy")
crawl_sub_subcategory("optics", end_page=23, referer="https://www.lazada.vn/cac-loai-ong-nhom/?spm=a2o4n.searchlistcategory.cate_1_7.8.35d9977cyobAtN", url="https://www.lazada.vn/cac-loai-ong-nhom/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.8.35d9977cyobAtN")
crawl_sub_subcategory("gadgets_&_other_cameras", end_page=28, referer="https://www.lazada.vn/cac-loai-may-anh-khac/?spm=a2o4n.searchlistcategory.cate_1_7.9.39647b48tst5fP", url="https://www.lazada.vn/cac-loai-may-anh-khac/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_7.9.39647b48tst5fP")

