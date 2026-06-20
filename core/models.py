from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User


class KhachHang(models.Model):
    """Khach hang / nguoi duoc tiem chung."""
    GIOI_TINH = [('Nam', 'Nam'), ('Nu', 'Nu'), ('Khac', 'Khac')]
    QUAN_HE = [
        ('ban_than', 'Bản thân'),
        ('con', 'Con'),
        ('vo_chong', 'Vợ/Chồng'),
        ('bo_me', 'Bố/Mẹ'),
        ('khac', 'Người thân khác'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='ho_so', verbose_name='Tai khoan quan ly')
    quan_he = models.CharField('Quan he voi chu tai khoan', max_length=10,
                               choices=QUAN_HE, default='ban_than')
    ho_ten = models.CharField('Ho ten', max_length=100)
    ngay_sinh = models.DateField('Ngay sinh')
    gioi_tinh = models.CharField('Gioi tinh', max_length=10, choices=GIOI_TINH, default='Nam')
    so_dien_thoai = models.CharField('So dien thoai', max_length=15)
    cccd = models.CharField('CCCD/CMND', max_length=20, blank=True)
    dia_chi = models.CharField('Dia chi', max_length=255, blank=True)
    ngay_tao = models.DateTimeField('Ngay tao ho so', auto_now_add=True)

    class Meta:
        verbose_name = 'Khach hang'
        verbose_name_plural = 'Khach hang'

    def __str__(self):
        return f'{self.ho_ten} - {self.so_dien_thoai}'

    @property
    def tuoi_thang(self):
        """Tuoi tinh theo thang (de doi chieu phac do)."""
        from django.utils import timezone
        today = timezone.now().date()
        return (today.year - self.ngay_sinh.year) * 12 + (today.month - self.ngay_sinh.month)


class VacXin(models.Model):
    """Danh muc vac-xin."""
    ten = models.CharField('Ten vac-xin', max_length=150)
    phong_benh = models.CharField('Phong benh', max_length=255)
    nha_san_xuat = models.CharField('Nha san xuat', max_length=150, blank=True)
    nuoc_san_xuat = models.CharField('Nuoc san xuat', max_length=100, blank=True)
    do_tuoi_min_thang = models.PositiveIntegerField('Do tuoi toi thieu (thang)', default=0)
    do_tuoi_max_thang = models.PositiveIntegerField('Do tuoi toi da (thang)', default=1200)
    han_dung_thang = models.PositiveIntegerField('Tong han dung (thang)', default=24)
    gia = models.DecimalField('Gia (VND)', max_digits=12, decimal_places=0, default=0)

    class Meta:
        verbose_name = 'Vac-xin'
        verbose_name_plural = 'Vac-xin'

    def __str__(self):
        return self.ten


class PhacDo(models.Model):
    """Phac do / goi tiem (vd: 6 trong 1, goi cho nguoi lon)."""
    NHOM = [('tre_em', 'Tre em'), ('nguoi_lon', 'Nguoi lon')]

    ten = models.CharField('Ten phac do', max_length=150)
    nhom = models.CharField('Nhom doi tuong', max_length=10, choices=NHOM, default='tre_em')
    mo_ta = models.TextField('Mo ta', blank=True)
    doi_tuong = models.CharField('Doi tuong ap dung', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Phac do tiem'
        verbose_name_plural = 'Phac do tiem'

    def __str__(self):
        return self.ten


class PhacDoChiTiet(models.Model):
    """Chi tiet tung mui trong phac do + khoang cach den mui truoc."""
    phac_do = models.ForeignKey(PhacDo, on_delete=models.CASCADE,
                                related_name='chi_tiet', verbose_name='Phac do')
    vac_xin = models.ForeignKey(VacXin, on_delete=models.CASCADE, verbose_name='Vac-xin')
    mui_so = models.PositiveIntegerField('Mui so')
    khoang_cach_ngay = models.PositiveIntegerField(
        'Khoang cach den mui truoc (ngay)', default=0,
        help_text='Mui 1 = 0. Mui sau = so ngay cach mui lien truoc.')

    class Meta:
        verbose_name = 'Chi tiet phac do'
        verbose_name_plural = 'Chi tiet phac do'
        ordering = ['phac_do', 'mui_so']

    def __str__(self):
        return f'{self.phac_do} - Mui {self.mui_so} ({self.vac_xin})'


class LoVacXin(models.Model):
    """Lo / batch vac-xin trong kho."""
    vac_xin = models.ForeignKey(VacXin, on_delete=models.CASCADE,
                                related_name='lo', verbose_name='Vac-xin')
    so_lo = models.CharField('So lo', max_length=50)
    ngay_san_xuat = models.DateField('Ngay san xuat', null=True, blank=True)
    ngay_nhap = models.DateField('Ngay nhap')
    han_su_dung = models.DateField('Han su dung')
    so_luong_ton = models.IntegerField('So luong ton', default=0)
    nguoi_nhap = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='Nguoi nhap')

    class Meta:
        verbose_name = 'Lo vac-xin'
        verbose_name_plural = 'Kho - Lo vac-xin'

    def __str__(self):
        return f'{self.vac_xin} - Lo {self.so_lo} (HSD {self.han_su_dung})'


class LichHen(models.Model):
    """Lich hen tiem cua khach."""
    TRANG_THAI = [
        ('cho', 'Chờ xác nhận'),
        ('xacnhan', 'Đã xác nhận'),
        ('datiem', 'Đã tiêm'),
        ('huy', 'Đã hủy'),
    ]
    LOAI_CHI_DINH = [
        ('khach_hang', 'Mong muốn của khách hàng'),
        ('benh_vien', 'Bệnh viện chỉ định'),
    ]
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE,
                                   related_name='lich_hen', verbose_name='Khach hang')
    ngay_hen = models.DateField('Ngay hen')
    gio_hen = models.TimeField('Gio hen', null=True, blank=True)
    vac_xin = models.ForeignKey(VacXin, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Vac-xin dang ky')
    phac_do = models.ForeignKey(PhacDo, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Goi / Phac do (tuy chon)')
    trang_thai = models.CharField('Trang thai', max_length=10, choices=TRANG_THAI, default='cho')
    loai_chi_dinh = models.CharField('Hinh thuc chi dinh', max_length=12,
                                     choices=LOAI_CHI_DINH, default='khach_hang')
    benh_vien = models.CharField('Benh vien chi dinh', max_length=200, blank=True)
    bac_si_chi_dinh = models.CharField('Bac si chi dinh', max_length=120, blank=True)
    ghi_chu = models.CharField('Ghi chu', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Lich hen'
        verbose_name_plural = 'Lich hen'
        ordering = ['-ngay_hen']

    def __str__(self):
        return f'{self.khach_hang.ho_ten} - {self.ngay_hen}'

    @property
    def la_tai_kham(self):
        """Lich tai kham sau phan ung (di kham, khong phai di tiem)."""
        return 'Tái khám sau phản ứng' in (self.ghi_chu or '')


class PhieuSangLoc(models.Model):
    """Phieu kham sang loc truoc tiem."""
    KET_LUAN = [
        ('dat', 'Du dieu kien tiem'),
        ('hoan', 'Hoan tiem'),
        ('chong', 'Chong chi dinh'),
    ]
    LY_DO_CHONG = [
        ('soc_phan_ve', 'Từng bị sốc phản vệ với vắc-xin/thành phần ở lần tiêm trước'),
        ('suy_giam_md', 'Suy giảm miễn dịch nặng (với vắc-xin sống)'),
        ('di_ung_thanh_phan', 'Dị ứng nặng với thành phần của vắc-xin'),
        ('khac', 'Khác'),
    ]
    lich_hen = models.OneToOneField(LichHen, on_delete=models.CASCADE,
                                    related_name='sang_loc', verbose_name='Lich hen')
    bac_si = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               verbose_name='Bac si sang loc')
    ngay = models.DateTimeField('Ngay sang loc', auto_now_add=True)
    nhiet_do = models.DecimalField('Nhiet do (C)', max_digits=4, decimal_places=1, null=True, blank=True)
    mach = models.PositiveIntegerField('Mach (lan/phut)', null=True, blank=True)
    huyet_ap = models.CharField('Huyet ap', max_length=20, blank=True)
    tien_su_benh = models.CharField('Tien su benh', max_length=255, blank=True)
    di_ung = models.CharField('Di ung', max_length=255, blank=True)
    benh_di_truyen = models.CharField('Benh di truyen', max_length=255, blank=True)
    dang_dung_thuoc = models.BooleanField('Dang dung thuoc', default=False)
    thuoc_dang_dung = models.CharField('Thuoc dang dung', max_length=255, blank=True)
    ket_luan = models.CharField('Ket luan', max_length=10, choices=KET_LUAN, default='dat')
    ly_do_hoan = models.CharField('Ly do hoan', max_length=255, blank=True)
    ly_do_chong = models.CharField('Ly do chong chi dinh', max_length=20,
                                   choices=LY_DO_CHONG, blank=True)
    ly_do_chong_khac = models.CharField('Ly do chong (khac)', max_length=255, blank=True)
    ghi_chu = models.TextField('Ghi chu', blank=True)

    class Meta:
        verbose_name = 'Phieu sang loc'
        verbose_name_plural = 'Phieu sang loc'

    def __str__(self):
        return f'Sang loc {self.lich_hen.khach_hang.ho_ten} - {self.get_ket_luan_display()}'


class MuiTiem(models.Model):
    """Ghi nhan mot mui tiem da thuc hien (= so tiem dien tu)."""
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE,
                                   related_name='mui_tiem', verbose_name='Khach hang')
    vac_xin = models.ForeignKey(VacXin, on_delete=models.PROTECT, verbose_name='Vac-xin')
    lo = models.ForeignKey(LoVacXin, on_delete=models.SET_NULL, null=True, blank=True,
                           verbose_name='Lo vac-xin')
    phac_do = models.ForeignKey(PhacDo, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Phac do')
    mui_so = models.PositiveIntegerField('Mui so', default=1)
    ngay_tiem = models.DateField('Ngay tiem')
    nguoi_tiem = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   verbose_name='Nguoi tiem (dieu duong)')
    vi_tri_tiem = models.CharField('Vi tri tiem', max_length=100, blank=True)
    ngay_hen_mui_ke = models.DateField('Ngay hen mui ke tiep', null=True, blank=True)

    class Meta:
        verbose_name = 'Mui tiem'
        verbose_name_plural = 'Mui tiem (So tiem)'
        ordering = ['-ngay_tiem']

    def __str__(self):
        return f'{self.khach_hang.ho_ten} - {self.vac_xin} - Mui {self.mui_so} ({self.ngay_tiem})'

    def tinh_ngay_hen_mui_ke(self):
        """
        Diem nhan ky thuat: tu dong tinh ngay hen mui ke tiep.
        Tra phac do tim mui (mui_so + 1), lay khoang_cach_ngay,
        ngay_hen_mui_ke = ngay_tiem + khoang_cach_ngay.
        """
        if not self.phac_do:
            return None
        mui_ke = self.phac_do.chi_tiet.filter(mui_so=self.mui_so + 1).first()
        if mui_ke:
            return self.ngay_tiem + timedelta(days=mui_ke.khoang_cach_ngay)
        return None  # da tiem mui cuoi

    def save(self, *args, **kwargs):
        # Tu dong tinh ngay hen mui ke khi luu
        if self.ngay_tiem and self.phac_do:
            self.ngay_hen_mui_ke = self.tinh_ngay_hen_mui_ke()
        super().save(*args, **kwargs)


class ThanhToan(models.Model):
    """Thanh toan / hoa don."""
    PHUONG_THUC = [('tien_mat', 'Tien mat'), ('chuyen_khoan', 'Chuyen khoan'), ('the', 'Quet the')]

    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE, verbose_name='Khach hang')
    lich_hen = models.ForeignKey(LichHen, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Lich hen')
    tong_tien = models.DecimalField('Tong tien (VND)', max_digits=12, decimal_places=0, default=0)
    phuong_thuc = models.CharField('Phuong thuc', max_length=15, choices=PHUONG_THUC, default='tien_mat')
    nguoi_thu = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='+', verbose_name='Nguoi thu tien')
    ngay_thanh_toan = models.DateTimeField('Ngay thanh toan', auto_now_add=True)

    class Meta:
        verbose_name = 'Thanh toan'
        verbose_name_plural = 'Thanh toan'

    def __str__(self):
        return f'{self.khach_hang.ho_ten} - {self.tong_tien} VND'


class TheoDoiSauTiem(models.Model):
    """Ghi nhan theo doi phan ung sau khi tiem mot mui."""
    THOI_DIEM = [
        ('30p', 'Sau 30 phut (tai phong kham)'),
        ('24h', 'Sau 24 gio'),
        ('48h', 'Sau 48 gio'),
        ('khac', 'Khac'),
    ]
    MUC_DO = [
        ('binh_thuong', 'Binh thuong'),
        ('nhe', 'Phan ung nhe'),
        ('can_chu_y', 'Can chu y'),
        ('nghiem_trong', 'Nghiem trong'),
    ]
    XU_LY = [
        ('quay_lai', 'Quay lại để kiểm tra'),
        ('binh_thuong', 'Điều kiện bình thường'),
        ('theo_doi_tiep', 'Theo dõi tiếp'),
        ('khac', 'Khác'),
    ]
    mui_tiem = models.ForeignKey(MuiTiem, on_delete=models.CASCADE,
                                 related_name='theo_doi', verbose_name='Mui tiem')
    thoi_diem = models.CharField('Thoi diem theo doi', max_length=5,
                                 choices=THOI_DIEM, default='30p')
    nhiet_do = models.DecimalField('Nhiet do (C)', max_digits=4, decimal_places=1,
                                   null=True, blank=True)
    trieu_chung = models.CharField('Trieu chung', max_length=255, blank=True,
                                   help_text='Vd: sot, sung dau cho tiem, quay khoc, phat ban...')
    muc_do = models.CharField('Muc do', max_length=15, choices=MUC_DO, default='binh_thuong')
    ghi_chu = models.TextField('Ghi chu', blank=True)
    xu_ly = models.CharField('Huong xu ly', max_length=20, choices=XU_LY, blank=True)
    xu_ly_ghi_chu = models.CharField('Ghi chu/ly do xu ly', max_length=255, blank=True)
    ngay_ghi_nhan = models.DateTimeField('Ngay ghi nhan', auto_now_add=True)

    class Meta:
        verbose_name = 'Theo doi sau tiem'
        verbose_name_plural = 'Theo doi sau tiem'
        ordering = ['-ngay_ghi_nhan']

    def __str__(self):
        return f'{self.mui_tiem.khach_hang.ho_ten} - {self.get_muc_do_display()}'


class ThongBao(models.Model):
    """Thong bao gui den nguoi dung (vd khach hang khi lich hen doi trang thai)."""
    nguoi_nhan = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='thong_bao', verbose_name='Nguoi nhan')
    noi_dung = models.CharField('Noi dung', max_length=255)
    duong_dan = models.CharField('Duong dan', max_length=200, blank=True)
    da_doc = models.BooleanField('Da doc', default=False)
    ngay_tao = models.DateTimeField('Ngay tao', auto_now_add=True)

    class Meta:
        verbose_name = 'Thong bao'
        verbose_name_plural = 'Thong bao'
        ordering = ['-ngay_tao']

    def __str__(self):
        return f'{self.nguoi_nhan} - {self.noi_dung[:40]}'


class QuyTrinhTiem(models.Model):
    """Theo doi quy trinh tiem cua mot lich hen qua 9 buoc."""
    B_DA_TOI = 1        # le tan: khach da toi
    B_DANG_CHO = 2      # le tan: dang cho
    B_VAO_PHONG = 3     # le tan: da vao phong kham
    B_SANG_LOC = 4      # bac si: sang loc + duyet cho tiem
    B_THANH_TOAN = 5    # le tan: thanh toan
    B_XUAT_KHO = 6      # thu kho: xuat kho
    B_TIEM = 7          # dieu duong: tiem
    B_THEO_DOI = 8      # dieu duong: theo doi
    HOAN_TAT = 9
    GIAI_DOAN = [
        (B_DA_TOI, 'Khách đã tới'),
        (B_DANG_CHO, 'Khách đang chờ'),
        (B_VAO_PHONG, 'Đã vào phòng khám'),
        (B_SANG_LOC, 'Bác sĩ sàng lọc'),
        (B_THANH_TOAN, 'Thanh toán'),
        (B_XUAT_KHO, 'Xuất kho'),
        (B_TIEM, 'Tiêm'),
        (B_THEO_DOI, 'Theo dõi sau tiêm'),
        (HOAN_TAT, 'Hoàn tất'),
    ]
    lich_hen = models.OneToOneField(LichHen, on_delete=models.CASCADE,
                                    related_name='quy_trinh', verbose_name='Lich hen')
    giai_doan = models.PositiveSmallIntegerField('Giai doan', default=B_DA_TOI, choices=GIAI_DOAN)
    vac_xin = models.ForeignKey(VacXin, null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name='Vac-xin (don)')
    lo = models.ForeignKey(LoVacXin, null=True, blank=True, on_delete=models.SET_NULL,
                           verbose_name='Lo xuat kho')
    mui_tiem = models.ForeignKey(MuiTiem, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='Mui tiem')
    thanh_toan = models.ForeignKey('ThanhToan', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='Thanh toan')
    ghi_chu_sang_loc = models.CharField('Ghi chu sang loc', max_length=255, blank=True)
    ngay_cap_nhat = models.DateTimeField('Cap nhat', auto_now=True)

    class Meta:
        verbose_name = 'Quy trinh tiem'
        verbose_name_plural = 'Quy trinh tiem'

    def __str__(self):
        return f'{self.lich_hen.khach_hang.ho_ten} - {self.get_giai_doan_display()}'

    @property
    def la_tai_kham(self):
        return self.lich_hen.la_tai_kham

    def ten_giai_doan(self):
        """Ten giai doan hien tai (tai kham: buoc 4 la 'Bac si kham')."""
        if self.la_tai_kham and self.giai_doan == self.B_SANG_LOC:
            return 'Bác sĩ khám'
        return self.get_giai_doan_display()


class PhieuXuatKho(models.Model):
    """Lich su xuat kho: moi lan xuat 1 phieu."""
    lo = models.ForeignKey(LoVacXin, on_delete=models.CASCADE,
                           related_name='phieu_xuat', verbose_name='Lo')
    so_luong = models.PositiveIntegerField('So luong', default=1)
    nguoi_xuat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   verbose_name='Nguoi xuat')
    nguoi_nhan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='+', verbose_name='Dieu duong nhan')
    ngay_nhan = models.DateTimeField('Ngay nhan', null=True, blank=True)
    quy_trinh = models.ForeignKey(QuyTrinhTiem, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='phieu_xuat', verbose_name='Quy trinh')
    ngay_xuat = models.DateTimeField('Ngay xuat', auto_now_add=True)

    class Meta:
        verbose_name = 'Phieu xuat kho'
        verbose_name_plural = 'Phieu xuat kho'
        ordering = ['-ngay_xuat']

    def __str__(self):
        return f'{self.lo} x{self.so_luong}'


class PhieuHuyKho(models.Model):
    """Lich su huy vac-xin (het han / loi chat luong...)."""
    LY_DO = [
        ('het_han', 'Hết hạn sử dụng'),
        ('loi_chat_luong', 'Lỗi chất lượng'),
        ('vo_hong', 'Vỡ/hỏng/bảo quản sai'),
        ('khac', 'Khác'),
    ]
    lo = models.ForeignKey(LoVacXin, on_delete=models.CASCADE,
                           related_name='phieu_huy', verbose_name='Lo')
    so_luong = models.PositiveIntegerField('So luong huy', default=1)
    ly_do = models.CharField('Ly do', max_length=20, choices=LY_DO, default='het_han')
    ghi_chu = models.CharField('Ghi chu', max_length=255, blank=True)
    nguoi_huy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  verbose_name='Nguoi huy')
    ngay_huy = models.DateTimeField('Ngay huy', auto_now_add=True)

    class Meta:
        verbose_name = 'Phieu huy kho'
        verbose_name_plural = 'Phieu huy kho'
        ordering = ['-ngay_huy']

    def __str__(self):
        return f'{self.lo} x{self.so_luong} ({self.get_ly_do_display()})'


class LichSuQuanTri(models.Model):
    """Lich su cac thao tac chinh sua cua admin (audit log)."""
    nguoi = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              related_name='lich_su_quan_tri', verbose_name='Nguoi thuc hien')
    hanh_dong = models.CharField('Hanh dong', max_length=300)
    thoi_gian = models.DateTimeField('Thoi gian', auto_now_add=True)

    class Meta:
        verbose_name = 'Lich su quan tri'
        verbose_name_plural = 'Lich su quan tri'
        ordering = ['-thoi_gian']

    def __str__(self):
        return f'{self.nguoi} - {self.hanh_dong[:40]}'


class TinNhanHoTro(models.Model):
    """Tin nhan ho tro truc tuyen giua khach hang va nhan vien (le tan)."""
    khach = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='tin_ho_tro', verbose_name='Khach (chu hoi thoai)')
    nguoi_gui = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  related_name='+', verbose_name='Nguoi gui')
    la_nhan_vien = models.BooleanField('Nhan vien gui', default=False)
    noi_dung = models.TextField('Noi dung')
    ngay = models.DateTimeField('Ngay', auto_now_add=True)
    da_doc = models.BooleanField('Da doc', default=False)

    class Meta:
        verbose_name = 'Tin nhan ho tro'
        verbose_name_plural = 'Tin nhan ho tro'
        ordering = ['ngay']

    def __str__(self):
        return f'{self.khach.username} - {"NV" if self.la_nhan_vien else "KH"}: {self.noi_dung[:30]}'


class YeuCauDatLaiMatKhau(models.Model):
    """Yeu cau quen mat khau -> admin dat lai trong khu quan tri."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='yeu_cau_mat_khau', verbose_name='Tai khoan')
    ngay_tao = models.DateTimeField('Ngay yeu cau', auto_now_add=True)
    da_xu_ly = models.BooleanField('Da xu ly', default=False)
    tu_choi = models.BooleanField('Tu choi', default=False)
    ngay_xu_ly = models.DateTimeField('Ngay xu ly', null=True, blank=True)

    class Meta:
        verbose_name = 'Yeu cau dat lai mat khau'
        verbose_name_plural = 'Yeu cau dat lai mat khau'
        ordering = ['da_xu_ly', '-ngay_tao']

    def __str__(self):
        return f'{self.user.username} - {"da xu ly" if self.da_xu_ly else "cho xu ly"}'


# ===== Signals: tu dong tao ThongBao cho khach hang =====
from django.db.models.signals import post_save, pre_save  # noqa: E402
from django.dispatch import receiver  # noqa: E402
from django.urls import reverse  # noqa: E402


@receiver(pre_save, sender=LichHen)
def _lichhen_nho_trangthai_cu(sender, instance, **kwargs):
    """Ghi nho trang thai cu de so sanh sau khi luu."""
    if instance.pk:
        instance._trang_thai_cu = LichHen.objects.filter(
            pk=instance.pk).values_list('trang_thai', flat=True).first()
    else:
        instance._trang_thai_cu = None


@receiver(post_save, sender=LichHen)
def _lichhen_thong_bao_doi_trangthai(sender, instance, created, **kwargs):
    try:
        ngay = instance.ngay_hen.strftime('%d/%m/%Y')
    except AttributeError:
        ngay = str(instance.ngay_hen)

    if created:
        # Lich hen moi -> bao cho tat ca le tan
        from django.contrib.auth.models import Group
        nhom = Group.objects.filter(name='Le tan').first()
        if nhom:
            for le_tan in nhom.user_set.all():
                ThongBao.objects.create(
                    nguoi_nhan=le_tan,
                    noi_dung=f'Lịch hẹn mới: {instance.khach_hang.ho_ten} '
                             f'đặt ngày {ngay} (chờ xác nhận).',
                    duong_dan=reverse('le_tan_lich_hen'))
        return

    cu = getattr(instance, '_trang_thai_cu', None)
    user = instance.khach_hang.user
    if user and cu and cu != instance.trang_thai:
        # Tai kham: trang thai 'datiem' hien thi la "Da kham"
        ten_tt = instance.get_trang_thai_display()
        if instance.trang_thai == 'datiem' and instance.la_tai_kham:
            ten_tt = 'Đã khám'
        ThongBao.objects.create(
            nguoi_nhan=user,
            noi_dung=f'Lịch hẹn ngày {ngay} đã chuyển sang "{ten_tt}".',
            duong_dan=reverse('ca_nhan'))


@receiver(post_save, sender=MuiTiem)
def _muitiem_thong_bao(sender, instance, created, **kwargs):
    user = instance.khach_hang.user
    if user and created:
        ThongBao.objects.create(
            nguoi_nhan=user,
            noi_dung=f'Bạn vừa được ghi nhận tiêm "{instance.vac_xin.ten}" '
                     f'(mũi {instance.mui_so}).',
            duong_dan=reverse('ca_nhan'))
