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
crawl_sub_subcategory("sports_&_action_camera", end_page=17, referer="https://www.lazada.vn/may-quay-hanh-dong/?spm=a2o4n.searchlistcategory.cate_1_8.1.c2a1564f2lbdus", url="https://www.lazada.vn/may-quay-hanh-dong/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_8.1.c2a1564f2lbdus")
crawl_sub_subcategory("video_camera", end_page=102, referer="https://www.lazada.vn/mua-may-quay-phim/?spm=a2o4n.searchlistcategory.cate_1_8.2.38744f7f7RTZBv", url="https://www.lazada.vn/mua-may-quay-phim/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_8.2.38744f7f7RTZBv")
crawl_sub_subcategory("professional_video_camera", end_page=2, referer="https://www.lazada.vn/camera-chuyen-nghiep/?spm=a2o4n.searchlistcategory.cate_1_8.3.17e466e9mIFWb3", url="https://www.lazada.vn/camera-chuyen-nghiep/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_8.3.17e466e9mIFWb3")
crawl_sub_subcategory("360_cameras", end_page=3, referer="https://www.lazada.vn/360-camera/?spm=a2o4n.searchlistcategory.cate_1_8.4.6ee13567cH0ttx", url="https://www.lazada.vn/360-camera/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_8.4.6ee13567cH0ttx")
crawl_sub_subcategory("underwater_camcorders", end_page=1, referer="https://www.lazada.vn/may-quay-phim-duoi-nuoc/?spm=a2o4n.searchlistcategory.cate_1_8.5.164d564fDDoAOa", url="https://www.lazada.vn/may-quay-phim-duoi-nuoc/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_8.5.164d564fDDoAOa")

