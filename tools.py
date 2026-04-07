try:
    # Khi chạy cùng LangChain/LangGraph
    from langchain_core.tools import tool
except ModuleNotFoundError:
    # Cho phép chạy/test offline khi môi trường chưa cài langchain_core
    def tool(fn):  # type: ignore
        return fn

# ==========================================================
# MOCK DATA – Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ==========================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu FLIGHTS_DB với key (origin, destination)
    # - Nếu tìm thấy -> format danh sách chuyến bay dễ đọc, bao gồm giá tiền
    # - Nếu không tìm thấy -> thử tra ngược (destination, origin) xem có không,
    #   nếu cũng không có -> "Không tìm thấy chuyến bay từ X đến Y."
    # Gợi ý: format giá tiền có dấu chấm phân cách (1.450.000đ)
    # 1. Thử tìm kiếm theo chiều xuôi (Origin -> Destination)
    flights = FLIGHTS_DB.get((origin, destination))
    
    # 2. Nếu không thấy, thử tìm kiếm theo chiều ngược lại (Destination -> Origin)
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        # Nếu tìm thấy chiều ngược, ta cập nhật lại tên để thông báo chính xác
        if flights:
            temp = origin
            origin = destination
            destination = temp

    # 3. Nếu vẫn không tìm thấy chuyến nào
    if not flights:
        return f"Hiện tại không tìm thấy chuyến bay nào giữa {origin} và {destination}."

    # 4. Nếu tìm thấy, tiến hành định dạng danh sách trả về
    result = f"Danh sách chuyến bay từ {origin} đi {destination}:\n"
    for f in flights:
        # Định dạng giá tiền có dấu chấm phân cách (VD: 1.450.000đ)
        formatted_price = "{:,.0f}đ".format(f['price']).replace(",", ".")
        
        result += f"- {f['airline']} ({f['class']}): {f['departure']} -> {f['arrival']} | Giá: {formatted_price}\n"
    
    return result

search_flights_tool = tool(search_flights)


def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu HOTELS_DB[city]
    # - Lọc theo max_price_per_night
    # - Sắp xếp theo rating giảm dần
    # - Format đẹp. Nếu không có kết quả -> "Không tìm thấy khách sạn tại X với giá dưới Y/đêm. Hãy thử tăng ngân sách."
    # 1. Kiểm tra xem thành phố có trong dữ liệu không
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Rất tiếc, chúng tôi chưa có dữ liệu khách sạn tại {city}."

    # 2. Lọc khách sạn theo giá tối đa (max_price_per_night)
    filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]

    # 3. Nếu sau khi lọc không còn khách sạn nào
    if not filtered_hotels:
        formatted_max_price = "{:,.0f}đ".format(max_price_per_night).replace(",", ".")
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {formatted_max_price}/đêm. Bạn thử tăng ngân sách hoặc chọn khu vực khác xem sao nhé!"

    # 4. Sắp xếp khách sạn theo điểm đánh giá (rating) giảm dần (từ cao đến thấp)
    sorted_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)

    # 5. Định dạng kết quả trả về cho đẹp
    result = f"Danh sách khách sạn tốt nhất tại {city} phù hợp với ngân sách của bạn:\n"
    for h in sorted_hotels:
        price = "{:,.0f}đ".format(h['price_per_night']).replace(",", ".")
        result += f"- {h['name']} ({h['stars']}⭐) | Khu vực: {h['area']} | Đánh giá: {h['rating']}/5 | Giá: {price}/đêm\n"
    
    return result

search_hotels_tool = tool(search_hotels)

def calculate_budget_impl(total_budget: int, expenses: str) -> str:
    """
    Nội bộ: tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    """
    def _fmt_money(v: int) -> str:
        return "{:,.0f}đ".format(v).replace(",", ".")

    try:
        if expenses is None:
            return "Lỗi định dạng chi phí: thiếu dữ liệu expenses."

        raw = expenses.strip()
        if not raw:
            return (
                "Lỗi định dạng chi phí: expenses rỗng. "
                "Vui lòng nhập theo định dạng 'tên_khoản:số_tiền,tên_khoản:số_tiền' "
                "(VD: 'vé_máy_bay:890000,khách_sạn:650000')."
            )

        expense_items = [item.strip() for item in raw.split(",") if item.strip()]
        total_expense = 0
        detail_lines: list[str] = []

        for item in expense_items:
            if ":" not in item:
                return (
                    f"Lỗi định dạng chi phí: '{item}'. "
                    "Vui lòng nhập theo định dạng 'tên_khoản:số_tiền' (các khoản cách nhau bởi dấu phẩy)."
                )

            name, amount_str = item.split(":", 1)
            name = name.strip()
            amount_str = amount_str.strip()
            if not name or not amount_str:
                return (
                    f"Lỗi định dạng chi phí: '{item}'. "
                    "Vui lòng nhập theo định dạng 'tên_khoản:số_tiền'."
                )

            try:
                amount = int(amount_str)
            except ValueError:
                return (
                    f"Lỗi định dạng chi phí: số tiền không hợp lệ trong '{item}'. "
                    "Số tiền phải là số nguyên (VD: 890000)."
                )

            total_expense += amount
            pretty_name = name.replace("_", " ").strip()
            if pretty_name:
                pretty_name = pretty_name[:1].upper() + pretty_name[1:]
            else:
                pretty_name = name
            detail_lines.append(f"- {pretty_name}: {_fmt_money(amount)}")

        remaining = total_budget - total_expense

        result = "Bảng chi phí:\n"
        result += "\n".join(detail_lines)
        result += "\n---\n"
        result += f"Tổng chi: {_fmt_money(total_expense)}\n"
        result += f"Ngân sách: {_fmt_money(total_budget)}\n"

        if remaining >= 0:
            result += f"Còn lại: {_fmt_money(remaining)}"
        else:
            result += f"Vượt ngân sách {_fmt_money(-remaining)}! Cần điều chỉnh."

        return result

    except Exception:
        return (
            f"Lỗi định dạng chi phí: '{expenses}'. "
            "Vui lòng nhập theo định dạng 'tên_khoản:số_tiền,tên_khoản:số_tiền'."
        )


def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    return calculate_budget_impl(total_budget, expenses)

calculate_budget_tool = tool(calculate_budget)
