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
crawl_sub_subcategory("power_banks", end_page=102, referer="https://www.lazada.vn/pin-sac-du-phong/?spm=a2o4n.searchlistcategory.cate_2_1.1.7623564fP141Ko", url="https://www.lazada.vn/pin-sac-du-phong/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.1.7623564fP141Ko")
crawl_sub_subcategory("cables_&_converters", end_page=102, referer="https://www.lazada.vn/cap-dien-thoai/?spm=a2o4n.searchlistcategory.cate_2_1.2.2b6b8f62537ida", url="https://www.lazada.vn/cap-dien-thoai/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.2.2b6b8f62537ida")
crawl_sub_subcategory("wall_chargers", end_page=102, referer="https://www.lazada.vn/bo-sac-co-day-cho-dien-thoai/?spm=a2o4n.searchlistcategory.cate_2_1.3.4dd0564fPzv7Xl", url="https://www.lazada.vn/bo-sac-co-day-cho-dien-thoai/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.3.4dd0564fPzv7Xl")
crawl_sub_subcategory("wireless_chargers", end_page=46, referer="https://www.lazada.vn/bo-sac-khong-day-cho-dien-thoai/?spm=a2o4n.searchlistcategory.cate_2_1.4.5860564fVoHP0y", url="https://www.lazada.vn/bo-sac-khong-day-cho-dien-thoai/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.4.5860564fVoHP0y")
crawl_sub_subcategory("phone_cases_&_covers", end_page=102, referer="https://www.lazada.vn/op-lung-bao-da-dien-thoai/?spm=a2o4n.searchlistcategory.cate_2_1.5.13e4564fKMhi1Z", url="https://www.lazada.vn/op-lung-bao-da-dien-thoai/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.5.13e4564fKMhi1Z")
crawl_sub_subcategory("tablet_cases_&_covers", end_page=102, referer="https://www.lazada.vn/op-lung-bao-da-may-tinh-bang/?spm=a2o4n.searchlistcategory.cate_2_1.6.7c5b564fCdMBnd", url="https://www.lazada.vn/op-lung-bao-da-may-tinh-bang/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.6.7c5b564fCdMBnd")
crawl_sub_subcategory("screen_protectors", end_page=102, referer="https://www.lazada.vn/mieng-dan-man-hinh-dien-thoai/?spm=a2o4n.searchlistcategory.cate_2_1.7.529b564fRUvfRY", url="https://www.lazada.vn/mieng-dan-man-hinh-dien-thoai/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.7.529b564fRUvfRY")
crawl_sub_subcategory("selfie_sticks", end_page=30, referer="https://www.lazada.vn/gay-chup-anh/?spm=a2o4n.searchlistcategory.cate_2_1.8.371d564fVxmnBB", url="https://www.lazada.vn/gay-chup-anh/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.8.371d564fVxmnBB")
crawl_sub_subcategory("car_chargers", end_page=44, referer="https://www.lazada.vn/sac-tren-xe-hoi/?spm=a2o4n.searchlistcategory.cate_2_1.9.2485564fyruwXw", url="https://www.lazada.vn/sac-tren-xe-hoi/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.9.2485564fyruwXw")
crawl_sub_subcategory("prepaid_cards", end_page=37, referer="https://www.lazada.vn/sim-the-cao/?spm=a2o4n.searchlistcategory.cate_2_1.10.7769564fCSrs5X", url="https://www.lazada.vn/sim-the-cao/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.10.7769564fCSrs5X")
crawl_sub_subcategory("docks_&_stands", end_page=102, referer="https://www.lazada.vn/dock-sac-dien-thoai/?spm=a2o4n.searchlistcategory.cate_2_1.11.4f9e564feQgZIQ", url="https://www.lazada.vn/dock-sac-dien-thoai/?ajax=true&isFirstRequest=true&page={page_num}&spm=a2o4n.searchlistcategory.cate_2_1.11.4f9e564feQgZIQ")

