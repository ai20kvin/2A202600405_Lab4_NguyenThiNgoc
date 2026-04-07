from tools import search_flights, search_hotels, calculate_budget


def test_search_flights_found():
    out = search_flights("Hà Nội", "Đà Nẵng")
    assert "Danh sách chuyến bay" in out
    assert "Hà Nội" in out and "Đà Nẵng" in out


def test_search_flights_not_found():
    out = search_flights("Đà Nẵng", "Cần Thơ")
    assert "không tìm thấy" in out.lower()


def test_search_hotels_budget_filter():
    out = search_hotels("Đà Nẵng", max_price_per_night=300_000)
    assert "Đà Nẵng" in out
    assert "250.000đ" in out or "300.000đ" in out


def test_search_hotels_no_city():
    out = search_hotels("Huế", max_price_per_night=1_000_000)
    assert "chưa có dữ liệu" in out.lower()


def test_calculate_budget_ok():
    out = calculate_budget(5_000_000, "vé_máy_bay:890000,khách_sạn:650000")
    assert "Bảng chi phí:" in out
    assert "Tổng chi:" in out and "Ngân sách:" in out and "Còn lại:" in out


def test_calculate_budget_over():
    out = calculate_budget(100_000, "vé:150000")
    assert "Vượt ngân sách" in out


def test_calculate_budget_bad_format():
    out = calculate_budget(1_000_000, "vé-100000")
    assert "Lỗi định dạng" in out


if __name__ == "__main__":
    # Chạy nhanh không cần pytest
    test_search_flights_found()
    test_search_flights_not_found()
    test_search_hotels_budget_filter()
    test_search_hotels_no_city()
    test_calculate_budget_ok()
    test_calculate_budget_over()
    test_calculate_budget_bad_format()
    print("OK: test_tools.py")

