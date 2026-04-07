import re
from typing import Optional

from tools import FLIGHTS_DB, HOTELS_DB, calculate_budget_impl, search_flights, search_hotels


CITY_NAMES = sorted(
    {c for pair in FLIGHTS_DB.keys() for c in pair} | set(HOTELS_DB.keys()),
    key=len,
    reverse=True,
)


def normalize_text(s: str) -> str:
    return (s or "").strip().lower()


def fmt_money(v: int) -> str:
    return "{:,.0f}đ".format(v).replace(",", ".")




def looks_like_travel_request(text: str) -> bool:
    t = normalize_text(text)
    travel_keywords = [
        "du lịch",
        "tour",
        "vé máy bay",
        "chuyến bay",
        "bay",
        "khách sạn",
        "hotel",
        "đặt phòng",
        "phòng",
        "resort",
        "homestay",
        "hostel",
        "lịch trình",
        "đi ",
        "đến ",
    ]
    return any(k in t for k in travel_keywords)


def extract_cities(text: str) -> list[str]:
    nt = normalize_text(text)
    matches: list[tuple[int, str]] = []
    for city in CITY_NAMES:
        idx = nt.find(city.lower())
        if idx != -1:
            matches.append((idx, city))

    matches.sort(key=lambda item: item[0])

    seen = set()
    uniq: list[str] = []
    for _, city in matches:
        if city not in seen:
            uniq.append(city)
            seen.add(city)
    return uniq


def parse_nights(text: str) -> Optional[int]:
    t = normalize_text(text)
    m = re.search(r"(\d{1,2})\s*(đêm|dem)\b", t)
    if not m:
        return None
    try:
        v = int(m.group(1))
    except ValueError:
        return None
    return v if v > 0 else None


def parse_money(text: str) -> Optional[int]:
    t = normalize_text(text)
    candidates: list[int] = []

    for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*(tr|triệu|trieu)\b", t):
        num = m.group(1).replace(",", ".")
        try:
            candidates.append(int(float(num) * 1_000_000))
        except ValueError:
            pass

    for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*k\b", t):
        num = m.group(1).replace(",", ".")
        try:
            candidates.append(int(float(num) * 1_000))
        except ValueError:
            pass

    for m in re.finditer(r"(\d[\d\.\,]{2,})\s*(vnđ|vnd|đ)\b", t):
        digits = re.sub(r"[^\d]", "", m.group(1))
        if digits:
            try:
                candidates.append(int(digits))
            except ValueError:
                pass

    for m in re.finditer(r"\b(\d{6,})\b", t):
        try:
            candidates.append(int(m.group(1)))
        except ValueError:
            pass

    if not candidates:
        return None
    return max(candidates)


def parse_hotel_budget_per_night(text: str) -> Optional[int]:
    t = normalize_text(text)
    if any(k in t for k in ["/đêm", "mỗi đêm", "đêm", "dem"]):
        return parse_money(t)
    return None


def parse_total_budget(text: str) -> Optional[int]:
    t = normalize_text(text)
    if any(k in t for k in ["ngân sách", "budget", "tổng", "tổng chi", "tổng cộng"]):
        return parse_money(t)
    return None


def needs_clarification(text: str) -> Optional[str]:
    t = normalize_text(text)

    if not looks_like_travel_request(t):
        return (
            "Mình chỉ hỗ trợ các yêu cầu liên quan đến du lịch/đặt vé/đặt phòng. "
            "Bạn cho mình biết bạn muốn đi đâu, đi từ đâu và ngân sách khoảng bao nhiêu nhé?"
        )

    if any(k in t for k in ["khách sạn", "hotel", "đặt phòng", "resort", "homestay", "hostel"]):
        cities = extract_cities(t)
        if not cities:
            return "Bạn muốn tìm khách sạn ở thành phố nào (ví dụ: Đà Nẵng/Phú Quốc/Hồ Chí Minh)?"
        if parse_hotel_budget_per_night(t) is None:
            return "Ngân sách tối đa của bạn cho khách sạn là bao nhiêu **mỗi đêm** (VNĐ)?"

    if any(k in t for k in ["chuyến bay", "vé máy bay", "bay"]):
        cities = extract_cities(t)
        if len(cities) < 2:
            return "Bạn cho mình biết điểm khởi hành và điểm đến (ví dụ: Hà Nội → Đà Nẵng) nhé?"

    if any(k in t for k in ["tư vấn", "gợi ý", "lịch trình", "kế hoạch", "đi du lịch"]):
        cities = extract_cities(t)
        if not cities:
            return "Bạn muốn đi đâu (điểm đến) và đi từ đâu (điểm khởi hành) vậy?"
        if parse_total_budget(t) is None:
            return "Ngân sách dự kiến cho **cả chuyến đi** của bạn là khoảng bao nhiêu (VNĐ)?"

    return None


def is_full_trip_advice(text: str) -> bool:
    t = normalize_text(text)
    return any(k in t for k in ["tư vấn", "gợi ý", "lịch trình", "kế hoạch", "combo", "chuyến đi"])


def build_trip_plan_response(user_text: str) -> Optional[str]:
    t = normalize_text(user_text)
    if not is_full_trip_advice(t):
        return None

    cities = extract_cities(t)
    if len(cities) < 2:
        return None

    origin, destination = cities[0], cities[1]
    total_budget = parse_total_budget(t)
    nights = parse_nights(t)
    hotel_budget_per_night = parse_hotel_budget_per_night(t)
    if total_budget is None or nights is None or hotel_budget_per_night is None:
        return None

    flight_search_text = search_flights(origin, destination)
    flights = FLIGHTS_DB.get((origin, destination)) or FLIGHTS_DB.get((destination, origin)) or []
    if not flights:
        flight_line = f"Không tìm thấy chuyến bay phù hợp cho tuyến {origin} ↔ {destination}."
        flight_cost = 0
    else:
        best_flight = min(flights, key=lambda x: x["price"])
        flight_cost = int(best_flight["price"])
        flight_line = (
            f"{best_flight['airline']} ({best_flight['class']}): "
            f"{best_flight['departure']} → {best_flight['arrival']} | Giá {fmt_money(flight_cost)}"
        )

    hotel_search_text = search_hotels(destination, hotel_budget_per_night)
    hotels = HOTELS_DB.get(destination) or []
    hotels_ok = [h for h in hotels if int(h["price_per_night"]) <= hotel_budget_per_night]
    if not hotels_ok:
        hotel_line = hotel_search_text
        hotel_cost = 0
    else:
        best_hotel = sorted(hotels_ok, key=lambda h: (h["rating"], h["stars"]), reverse=True)[0]
        hotel_cost = int(best_hotel["price_per_night"]) * nights
        hotel_line = (
            f"{best_hotel['name']} ({best_hotel['stars']}⭐) | "
            f"{best_hotel['area']} | {best_hotel['rating']}/5 | "
            f"{fmt_money(int(best_hotel['price_per_night']))}/đêm × {nights} đêm = {fmt_money(hotel_cost)}"
        )

    expenses_str = f"vé_máy_bay:{flight_cost},khách_sạn:{hotel_cost}"
    budget_table = calculate_budget_impl(total_budget=total_budget, expenses=expenses_str)

    total_est = flight_cost + hotel_cost
    total_line = f"{fmt_money(total_est)} (chi tiết:\n{budget_table})"

    return (
        f"Chuyến bay: {flight_line}\n"
        f"Khách sạn: {hotel_line}\n"
        f"Tổng chi phí ước tính: {total_line}\n"
        f"Gợi ý thêm: Nếu muốn tiết kiệm hơn: giảm ngân sách khách sạn/đêm hoặc chọn chuyến bay giờ linh hoạt. "
        f"Nếu bạn cho mình biết ngày đi cụ thể và số người, mình tối ưu combo chính xác hơn."
    )

