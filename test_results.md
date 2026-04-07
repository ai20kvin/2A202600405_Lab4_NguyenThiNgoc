# Test Results - TravelBuddy Agent

## Test 1 - Direct answer (Không cần tool)

```
(venv) D:\2A202600405_lab4>python agent.py
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
    Gõ 'quit' để thoát
============================================================

Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn muốn đi đâu (điểm đến) và đi từ đâu (điểm khởi hành) vậy?
```

---

## Test 2 – Single Tool Call

```
(venv) D:\2A202600405_lab4>python agent.py
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
    Gõ 'quit' để thoát
============================================================

Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

TravelBuddy đang suy nghĩ...
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Trả lời trực tiếp

TravelBuddy: Chuyến bay:
- Vietnam Airlines (economy): 06:00 -> 07:20 | Giá: 1.450.000đ
- Vietnam Airlines (business): 14:00 -> 15:20 | Giá: 2.800.000đ
- VietJet Air (economy): 08:30 -> 09:50 | Giá: 890.000đ
- Bamboo Airways (economy): 11:00 -> 12:20 | Giá: 1.200.000đ

Khách sạn: Chưa đủ thông tin.

Tổng chi phí ước tính: Chưa đủ thông tin.

Gợi ý thêm: Bạn có ngân sách bao nhiêu cho chuyến đi này? Tôi có thể giúp bạn tìm khách sạn phù hợp!
```

---

## Test 3 – Multi-Step Tool Chaining

```
(venv) D:\2A202600405_lab4>python agent.py
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
    Gõ 'quit' để thoát
============================================================

Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

TravelBuddy đang suy nghĩ...
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Trả lời trực tiếp

TravelBuddy: Chuyến bay:
- Vietnam Airlines (economy): 06:00 -> 07:20 | Giá: 1.450.000đ
- Vietnam Airlines (business): 14:00 -> 15:20 | Giá: 2.800.000đ
- VietJet Air (economy): 08:30 -> 09:50 | Giá: 890.000đ
- Bamboo Airways (economy): 11:00 -> 12:20 | Giá: 1.200.000đ

Khách sạn: Chưa đủ thông tin.

Tổng chi phí ước tính: Chưa đủ thông tin.

Gợi ý thêm: Bạn có ngân sách bao nhiêu cho chuyến đi này? Tôi có thể giúp bạn tìm khách sạn phù hợp!
```

---

## Test 4 – Missing Info / Clarification

```
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn muốn tìm khách sạn ở thành phố nào (ví dụ: Đà Nẵng/Phú Quốc/Hồ Chí Minh)?
```

---

## Test 5 – Guardrail / Refusal

```
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Mình chỉ hỗ trợ các yêu cầu liên quan đến du lịch/đặt vé/đặt phòng. Bạn cho mình biết bạn muốn đi đâu, đi từ đâu và ngân sách khoảng bao nhiêu nhé?
```
