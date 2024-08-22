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
crawl_sub_subcategory("headphones_&_headsets", end_page=102, referer="https://www.lazada.vn/cac-loai-tai-nghe/?spm=a2o4n.searchlistcategory.cate_1_5.1.5a874c39phBqrj", url="https://www.lazada.vn/cac-loai-tai-nghe/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.1.5a874c39phBqrj")
crawl_sub_subcategory("home_audio", end_page=102, referer="https://www.lazada.vn/he-thong-giai-tri-cho-tai-gia/?spm=a2o4n.officialstores.cate_1_5.3.24246780iCKdAV", url="https://www.lazada.vn/he-thong-giai-tri-cho-tai-gia/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.officialstores.cate_1_5.3.24246780iCKdAV")
crawl_sub_subcategory("professional_audio_equipment", end_page=102, referer="https://www.lazada.vn/am-thanh-song-san-khau/?spm=a2o4n.searchlistcategory.cate_1_5.4.2654564fuNaAYB", url="https://www.lazada.vn/am-thanh-song-san-khau/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.4.2654564fuNaAYB")
crawl_sub_subcategory("dj_equipment", end_page=1, referer="https://www.lazada.vn/thiet-bi-dj-2/?spm=a2o4n.searchlistcategory.cate_1_5.5.345d3b8f2oxCgX", url="https://www.lazada.vn/thiet-bi-dj-2/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.5.345d3b8f2oxCgX")
crawl_sub_subcategory("turntables", end_page=102, referer="https://www.lazada.vn/may-doc-dia-than/?spm=a2o4n.searchlistcategory.cate_1_5.6.e2e04efdODBOPL", url="https://www.lazada.vn/may-doc-dia-than/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.6.e2e04efdODBOPL")
crawl_sub_subcategory("headphones_accessories", end_page=102, referer="https://www.lazada.vn/phu-kien-tai-nghe/?spm=a2o4n.searchlistcategory.cate_1_5.7.52c2564f4eVzy8", url="https://www.lazada.vn/phu-kien-loa-de-ban/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.8.1ed5564ftpSN6K")
crawl_sub_subcategory("portable_speakers_accessories", end_page=9, referer="https://www.lazada.vn/phu-kien-loa-de-ban/?spm=a2o4n.searchlistcategory.cate_1_5.8.1ed5564ftpSN6K", url="https://www.lazada.vn/phu-kien-loa-de-ban/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.8.792b564fMAA6ik")
crawl_sub_subcategory("home_audio_accessories", end_page=102, referer="https://www.lazada.vn/phu-kien-am-thanh-tai-gia/?spm=a2o4n.searchlistcategory.cate_1_5.9.6d2e1379JFWVIx", url="https://www.lazada.vn/phu-kien-am-thanh-tai-gia/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.9.6d2e1379JFWVIx")
crawl_sub_subcategory("professional_audio_accessories", end_page=24, referer="https://www.lazada.vn/phu-kien-am-thanh-chuyen-nghiep/?spm=a2o4n.searchlistcategory.cate_1_5.10.792b564fMAA6ik", url="https://www.lazada.vn/phu-kien-am-thanh-chuyen-nghiep/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.10.792b564fMAA6ik")
crawl_sub_subcategory("portable_players", end_page=102, referer="https://www.lazada.vn/thiet-bi-phat-am-thanh-di-dong/?spm=a2o4n.searchlistcategory.cate_1_5.11.438e4cdbZXn0ph", url="https://www.lazada.vn/thiet-bi-phat-am-thanh-di-dong/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_1_5.11.438e4cdbZXn0ph")

