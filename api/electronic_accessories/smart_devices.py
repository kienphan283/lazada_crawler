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
crawl_sub_subcategory("smartwatch_&_accessories", end_page=102, referer="https://www.lazada.vn/dong-ho-thong-minh-phu-kien/?spm=a2o4n.searchlistcategory.cate_2_2.1.21b1564fQpFzbG", url="https://www.lazada.vn/dong-ho-thong-minh-phu-kien/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.1.21b1564fQpFzbG")
crawl_sub_subcategory("fitness_trackers_accessories", end_page=102, referer="https://www.lazada.vn/phu-kien-thiet-bi-theo-doi-van-dong/?spm=a2o4n.searchlistcategory.cate_2_2.2.2315997dkxoed1", url="https://www.lazada.vn/phu-kien-thiet-bi-theo-doi-van-dong/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.2.2315997dkxoed1")
crawl_sub_subcategory("smart_speakers", end_page=86, referer="https://www.lazada.vn/loa-thong-minh/?spm=a2o4n.searchlistcategory.cate_2_2.3.69a2564f0yg5mv", url="https://www.lazada.vn/loa-thong-minh/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.3.69a2564f0yg5mv")
crawl_sub_subcategory("smart_switches", end_page=63, referer="https://www.lazada.vn/cong-tat-thong-minh/?spm=a2o4n.searchlistcategory.cate_2_2.4.171a564fw7T7Rl", url="https://www.lazada.vn/cong-tat-thong-minh/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.4.171a564fw7T7Rl")
crawl_sub_subcategory("smart_glasses", end_page=92, referer="https://www.lazada.vn/mat-kinh-thong-minh/?spm=a2o4n.searchlistcategory.cate_2_2.5.7e6f16bd7F3Ueo", url="https://www.lazada.vn/mat-kinh-thong-minh/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.5.7e6f16bd7F3Ueo")
crawl_sub_subcategory("smart_rings", end_page=4, referer="https://www.lazada.vn/nhan-thong-minh/?spm=a2o4n.searchlistcategory.cate_2_2.6.28fc564fsPdKlK", url="https://www.lazada.vn/nhan-thong-minh/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.6.28fc564fsPdKlK")
crawl_sub_subcategory("pc_vr_accessories", end_page=51, referer="https://www.lazada.vn/phu-kien-thiet-bi-thuc-te-ao/?spm=a2o4n.searchlistcategory.cate_2_2.7.6f4f56dcCy8c89", url="https://www.lazada.vn/phu-kien-thiet-bi-thuc-te-ao/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.7.6f4f56dcCy8c89")
crawl_sub_subcategory("virtual_reality", end_page=102, referer="https://www.lazada.vn/thiet-bi-thuc-te-ao-cong-nghe/?spm=a2o4n.searchlistcategory.cate_2_2.8.2e97564faotPaL", url="https://www.lazada.vn/thiet-bi-thuc-te-ao-cong-nghe/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.8.2e97564faotPaL")
crawl_sub_subcategory("gesture_control", end_page=5, referer="https://www.lazada.vn/thiet-bi-dieu-khien-bang-cu-chi/?spm=a2o4n.searchlistcategory.cate_2_2.9.1cf5564fLIrVPL", url="https://www.lazada.vn/thiet-bi-dieu-khien-bang-cu-chi/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.9.1cf5564fLIrVPL")
crawl_sub_subcategory("smart_trackers", end_page=102, referer="https://www.lazada.vn/thiet-bi-giam-sat-thong-minh/?spm=a2o4n.searchlistcategory.cate_2_2.10.7f2b564f6brwh9", url="https://www.lazada.vn/thiet-bi-giam-sat-thong-minh/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.10.7f2b564f6brwh9")
crawl_sub_subcategory("streaming_media_players", end_page=102, referer="https://www.lazada.vn/cac-loai-media-player/?spm=a2o4n.searchlistcategory.cate_2_2.11.3f52564fyDKxP4", url="https://www.lazada.vn/cac-loai-media-player/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_2.11.3f52564fyDKxP4")

