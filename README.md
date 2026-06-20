# Hệ thống Quản lý Tiêm chủng

Đồ án tốt nghiệp — Website quản lý phòng khám tiêm chủng.
**Stack:** Python + Django 6 + PostgreSQL.

## Yêu cầu môi trường
- Python 3.12+
- PostgreSQL 17 (đang chạy, có database `vaccine_clinic_db`)

## Chạy project trên máy hiện tại

```powershell
cd D:\Code\vaccine_clinic
venv\Scripts\activate
python manage.py runserver
```

Mở trình duyệt:
- Trang chủ: http://127.0.0.1:8000/
- Trang quản trị: http://127.0.0.1:8000/admin/

## Tài khoản & phân quyền

Chạy 1 lần để tạo nhóm vai trò + tài khoản demo (sau khi `migrate`):
```powershell
python manage.py setup_roles
```

| Tài khoản | Mật khẩu | Vai trò | Quyền |
|-----------|----------|---------|-------|
| admin | admin123 | Quản trị (superuser) | Toàn quyền |
| letan | letan123 | Lễ tân | Khách hàng, Lịch hẹn, Thanh toán |
| bacsi | bacsi123 | Bác sĩ | Phiếu sàng lọc, xem khách/lịch |
| dieuduong | dieuduong123 | Điều dưỡng | Mũi tiêm, Kho lô, xem khách |

> Phân quyền 2 tầng: (1) Django Admin theo Group/Permission từng model; (2) tầng code — trang báo cáo nhắc mũi chặn bằng decorator `trong_nhom()` (bác sĩ truy cập sẽ thấy trang 403 thân thiện).

## Tạo dữ liệu mẫu (để demo nhắc mũi)
```powershell
python manage.py seed_demo --reset
```

## Cài lại khi chuyển sang MÁY KHÁC

1. Cài Python + PostgreSQL trên máy mới.
2. Tạo database: `CREATE DATABASE vaccine_clinic_db;`
3. Lấy code về (Git clone hoặc copy — **trừ thư mục `venv`**).
4. Tạo lại môi trường + cài thư viện:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
5. Copy `.env.example` thành `.env`, sửa mật khẩu PostgreSQL cho đúng máy mới.
6. Tạo lại bảng + tài khoản admin:
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```
7. `python manage.py runserver`

> Lưu ý: dữ liệu trong DB không đi theo code. Để mang dữ liệu sang máy mới dùng `pg_dump` / `pg_restore`.

## Cấu trúc

```
vaccine_clinic/
├── config/          # Cấu hình Django (settings, urls)
├── core/            # App nghiệp vụ
│   ├── models.py    # Các bảng: KhachHang, VacXin, PhacDo, MuiTiem...
│   ├── admin.py     # Khai báo giao diện quản trị
│   └── migrations/  # Lịch sử thay đổi cấu trúc DB
├── .env             # Cấu hình bí mật (KHÔNG commit)
├── .env.example     # File mẫu
├── requirements.txt # Danh sách thư viện
└── manage.py
```

## Các bảng dữ liệu (models)

| Model | Ý nghĩa |
|-------|---------|
| KhachHang | Hồ sơ khách hàng / người được tiêm |
| VacXin | Danh mục vắc-xin |
| PhacDo + PhacDoChiTiet | Phác đồ tiêm (các mũi + khoảng cách ngày) |
| LoVacXin | Kho - lô vắc-xin, hạn dùng |
| LichHen | Lịch hẹn tiêm |
| PhieuSangLoc | Khám sàng lọc trước tiêm |
| MuiTiem | Sổ tiêm điện tử (tự tính ngày hẹn mũi kế) |
| ThanhToan | Hóa đơn thanh toán |
```
