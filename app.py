from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Danh sách các mô hình xe bạn muốn giữ lại
desired_models = [
    "Giá xe Rebel 300",
    "Giá xe Rebel 500",
    "Giá xe CB500X",
    "Giá xe CB500F",
    "Giá xe CBR500R",
    "Giá xe CB650F",
    "Giá xe CBR650R",
    "Giá xe Gold Wing",
    "Giá xe CBR150R ABS",
    "Giá xe CBR250RR",
    "Giá xe CB300R",
    "Giá xe CB350 H'ness",
    "Giá xe CB1000R",
    "Giá xe CBR1000RR-R FiREBLADE",
    "Giá xe CBR1000RR-R FiREBLADE SP",
    "Giá xe Gold Wing",
    "Giá xe Africa Twin Adventure Sport",
    "Giá xe CB150R Exmotion"
]

@app.get('/')
def get_moto_prices():
    try:
        url = 'https://giaxe.2banh.vn/bang-gia-xe/bang-gia-xe-moto-119.html'
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trích xuất dữ liệu từ trang web
        table = soup.find('table')  # Giả sử bảng đầu tiên chứa dữ liệu mong muốn
        if not table:
            raise ValueError("Không tìm thấy bảng nào trong trang web.")

        data = []
        rows = table.find_all('tr')
        for row in rows[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) >= 3:  # Kiểm tra nếu hàng có ít nhất 3 cột
                model = cols[0].get_text(strip=True)
                if model in desired_models:  # Chỉ lấy các mô hình xe trong danh sách bạn quan tâm
                    item = {
                        "model": model,
                        "recommended_price": cols[1].get_text(strip=True),
                        "discounted_price": cols[2].get_text(strip=True)
                    }
                    data.append(item)

        return { "data": data }  # Bao bọc dữ liệu trong một cặp dấu ngoặc nhọn

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Đã xảy ra lỗi khi truy cập dữ liệu: {str(e)}")
