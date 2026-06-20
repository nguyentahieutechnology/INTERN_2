from django.contrib import admin

from .models import (
    KhachHang, VacXin, PhacDo, PhacDoChiTiet, LoVacXin,
    LichHen, PhieuSangLoc, MuiTiem, ThanhToan, TheoDoiSauTiem, ThongBao,
    QuyTrinhTiem, PhieuXuatKho, PhieuHuyKho, LichSuQuanTri,
)


@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'quan_he', 'user', 'gioi_tinh', 'ngay_sinh', 'so_dien_thoai')
    search_fields = ('ho_ten', 'so_dien_thoai', 'cccd', 'user__username')
    list_filter = ('gioi_tinh', 'quan_he')


@admin.register(VacXin)
class VacXinAdmin(admin.ModelAdmin):
    list_display = ('ten', 'phong_benh', 'nha_san_xuat', 'han_dung_thang',
                    'do_tuoi_min_thang', 'do_tuoi_max_thang', 'gia')
    search_fields = ('ten', 'phong_benh')


class PhacDoChiTietInline(admin.TabularInline):
    """Nhap cac mui cua phac do ngay trong trang phac do."""
    model = PhacDoChiTiet
    extra = 1


@admin.register(PhacDo)
class PhacDoAdmin(admin.ModelAdmin):
    list_display = ('ten', 'nhom', 'doi_tuong')
    list_filter = ('nhom',)
    inlines = [PhacDoChiTietInline]


@admin.register(LoVacXin)
class LoVacXinAdmin(admin.ModelAdmin):
    list_display = ('vac_xin', 'so_lo', 'ngay_nhap', 'han_su_dung', 'so_luong_ton')
    list_filter = ('vac_xin',)
    search_fields = ('so_lo',)


@admin.register(LichHen)
class LichHenAdmin(admin.ModelAdmin):
    list_display = ('khach_hang', 'ngay_hen', 'gio_hen', 'phac_do',
                    'loai_chi_dinh', 'benh_vien', 'trang_thai')
    list_filter = ('trang_thai', 'loai_chi_dinh', 'ngay_hen')
    search_fields = ('khach_hang__ho_ten', 'benh_vien', 'bac_si_chi_dinh')


@admin.register(PhieuSangLoc)
class PhieuSangLocAdmin(admin.ModelAdmin):
    list_display = ('lich_hen', 'bac_si', 'ket_luan', 'nhiet_do', 'mach', 'ngay')
    list_filter = ('ket_luan',)


@admin.register(MuiTiem)
class MuiTiemAdmin(admin.ModelAdmin):
    list_display = ('khach_hang', 'vac_xin', 'mui_so', 'ngay_tiem', 'ngay_hen_mui_ke', 'nguoi_tiem')
    list_filter = ('vac_xin', 'ngay_tiem')
    search_fields = ('khach_hang__ho_ten',)
    date_hierarchy = 'ngay_tiem'


@admin.register(ThanhToan)
class ThanhToanAdmin(admin.ModelAdmin):
    list_display = ('khach_hang', 'tong_tien', 'phuong_thuc', 'ngay_thanh_toan')
    list_filter = ('phuong_thuc',)


@admin.register(TheoDoiSauTiem)
class TheoDoiSauTiemAdmin(admin.ModelAdmin):
    list_display = ('mui_tiem', 'thoi_diem', 'nhiet_do', 'muc_do', 'ngay_ghi_nhan')
    list_filter = ('muc_do', 'thoi_diem')
    search_fields = ('mui_tiem__khach_hang__ho_ten', 'trieu_chung')


@admin.register(ThongBao)
class ThongBaoAdmin(admin.ModelAdmin):
    list_display = ('nguoi_nhan', 'noi_dung', 'da_doc', 'ngay_tao')
    list_filter = ('da_doc',)
    search_fields = ('nguoi_nhan__username', 'noi_dung')


@admin.register(QuyTrinhTiem)
class QuyTrinhTiemAdmin(admin.ModelAdmin):
    list_display = ('lich_hen', 'giai_doan', 'vac_xin', 'lo', 'ngay_cap_nhat')
    list_filter = ('giai_doan',)


@admin.register(PhieuXuatKho)
class PhieuXuatKhoAdmin(admin.ModelAdmin):
    list_display = ('lo', 'so_luong', 'nguoi_xuat', 'quy_trinh', 'ngay_xuat')
    search_fields = ('lo__so_lo', 'lo__vac_xin__ten')


@admin.register(PhieuHuyKho)
class PhieuHuyKhoAdmin(admin.ModelAdmin):
    list_display = ('lo', 'so_luong', 'ly_do', 'nguoi_huy', 'ngay_huy')
    list_filter = ('ly_do',)
    search_fields = ('lo__so_lo', 'lo__vac_xin__ten')


@admin.register(LichSuQuanTri)
class LichSuQuanTriAdmin(admin.ModelAdmin):
    list_display = ('thoi_gian', 'nguoi', 'hanh_dong')
    search_fields = ('hanh_dong', 'nguoi__username')


admin.site.site_header = 'He thong Quan ly Tiem chung'
admin.site.site_title = 'Quan ly Tiem chung'
admin.site.index_title = 'Trang quan tri'
