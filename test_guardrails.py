from guardrails import (
    parse_money,
    parse_nights,
    parse_total_budget,
    parse_hotel_budget_per_night,
    needs_clarification,
    build_trip_plan_response,
)


def test_parse_money():
    assert parse_money("ngân sách 5 triệu") == 5_000_000
    assert parse_money("tối đa 500k/đêm") == 500_000
    assert parse_money("5.000.000đ") == 5_000_000


def test_parse_nights():
    assert parse_nights("ở 3 đêm") == 3
    assert parse_nights("2dem") == 2


def test_clarify_hotel_needs_budget_per_night():
    q = needs_clarification("Tìm khách sạn ở Đà Nẵng")
    assert q and "mỗi đêm" in q


def test_clarify_trip_needs_total_budget():
    q = needs_clarification("Tư vấn đi Hà Nội Đà Nẵng 3 đêm")
    assert q and "cả chuyến" in q


def test_build_trip_plan_response_when_enough_info():
    out = build_trip_plan_response("Tư vấn chuyến đi Hà Nội Đà Nẵng 3 đêm, ngân sách 5 triệu, khách sạn 500k/đêm")
    assert out is not None
    assert out.startswith("Chuyến bay:")
    assert "Khách sạn:" in out and "Tổng chi phí ước tính:" in out and "Gợi ý thêm:" in out


if __name__ == "__main__":
    test_parse_money()
    test_parse_nights()
    test_clarify_hotel_needs_budget_per_night()
    test_clarify_trip_needs_total_budget()
    test_build_trip_plan_response_when_enough_info()
    print("OK: test_guardrails.py")

