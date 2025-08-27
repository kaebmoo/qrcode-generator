# QR Code Generator Web Application

Web application สำหรับสร้าง QR Code ด้วย FastAPI และ Semantic UI

## Features

- สร้าง QR Code จากข้อความหรือ URL
- UI สวยงามด้วย Semantic UI CSS
- รองรับการเพิ่มโลโก้ตรงกลาง QR Code
- ดาวน์โหลด QR Code เป็นไฟล์ PNG คุณภาพสูง
- คัดลอกรูป QR Code ไปใช้งานได้ทันที
- Responsive design รองรับทุกอุปกรณ์

## การติดตั้ง

1. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

2. เพิ่มไฟล์โลโก้ (ถ้าต้องการ):
   - วางไฟล์โลโก้ชื่อ `logo.png` ในโฟลเดอร์ `static/`
   - รองรับไฟล์ PNG ที่มี transparency

3. รันโปรแกรม:
```bash
python main.py
```

หรือใช้ uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

4. เปิดเบราว์เซอร์ไปที่: `http://localhost:8080`

## การใช้งาน

1. **หน้าแรก**: ใส่ข้อความหรือ URL ที่ต้องการสร้าง QR Code
2. **ตัวเลือก**: เลือกว่าจะเพิ่มโลโก้หรือไม่
3. **สร้าง QR Code**: คลิกปุ่มเพื่อสร้าง QR Code
4. **ดาวน์โหลด**: บันทึก QR Code เป็นไฟล์ PNG

## API Endpoints

- `GET /` - หน้าแรกของ web application
- `POST /generate` - สร้าง QR Code และแสดงผลลัพธ์
- `GET /download/{text}` - ดาวน์โหลด QR Code เป็นไฟล์ PNG

## โครงสร้างโปรเจค

```
qrcode-generator/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── templates/          # HTML templates
│   ├── index.html      # หน้าแรก
│   └── result.html     # หน้าแสดงผลลัพธ์
└── static/             # Static files
    └── logo.png        # โลโก้ (optional)
```

## ปรับแต่งเพิ่มเติม

### เปลี่ยนขนาด QR Code
แก้ไขค่า `scale` ในฟังก์ชัน `generate_qr_code()`:
```python
scale = 8  # เปลี่ยนเป็น 10 สำหรับ QR Code ขนาดใหญ่ขึ้น
```

### เปลี่ยน Error Correction Level
แก้ไข `QrCode.Ecc` ในฟังก์ชัน `generate_qr_code()`:
- `LOW` - รองรับความเสียหาย 7%
- `MEDIUM` - รองรับความเสียหาย 15%
- `QUARTILE` - รองรับความเสียหาย 25% (default)
- `HIGH` - รองรับความเสียหาย 30%

### ปรับขนาดโลโก้
แก้ไขค่า `max_logo_size`:
```python
max_logo_size = img_size // 5  # เปลี่ยนเป็น // 4 สำหรับโลโก้ใหญ่ขึ้น
```

## Technologies Used

- **FastAPI** - Modern web framework สำหรับ Python
- **Semantic UI** - CSS framework สำหรับ UI ที่สวยงาม
- **Pillow** - Python Imaging Library สำหรับจัดการรูปภาพ
- **qrcodegen** - Library สำหรับสร้าง QR Code
- **Jinja2** - Template engine สำหรับ HTML

## License

MIT License
