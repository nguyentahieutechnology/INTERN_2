"""
Tao du lieu mau cho he thong quan ly tiem chung.
Chay:  python manage.py seed_demo
       python manage.py seed_demo --reset   (xoa du lieu cu truoc khi tao)

Trong tam: tao cac mui tiem mui 1 o nhieu moc thoi gian khac nhau de
minh hoa tinh nang TU DONG TINH & NHAC mui ke tiep.
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from core.models import (
    KhachHang, VacXin, PhacDo, PhacDoChiTiet, LoVacXin,
    LichHen, MuiTiem,
)


class Command(BaseCommand):
    help = 'Tao du lieu mau de test tinh nang nhac mui'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true',
                            help='Xoa du lieu nghiep vu cu truoc khi tao moi')

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.now().date()

        if options['reset']:
            self.stdout.write('Dang xoa du lieu cu...')
            MuiTiem.objects.all().delete()
            LichHen.objects.all().delete()
            LoVacXin.objects.all().delete()
            PhacDoChiTiet.objects.all().delete()
            PhacDo.objects.all().delete()
            VacXin.objects.all().delete()
            KhachHang.objects.all().delete()

        nguoi_tiem = User.objects.filter(is_superuser=True).first()

        # ----- 1. VAC-XIN -----
        hexaxim = VacXin.objects.create(
            ten='Vac-xin 6 trong 1 (Hexaxim)',
            phong_benh='Bach hau, Ho ga, Uon van, Bai liet, Hib, Viem gan B',
            nha_san_xuat='Sanofi Pasteur', nuoc_san_xuat='Phap',
            do_tuoi_min_thang=2, do_tuoi_max_thang=24, gia=1015000)
        mmr = VacXin.objects.create(
            ten='Vac-xin Soi - Quai bi - Rubella (MMR II)',
            phong_benh='Soi, Quai bi, Rubella',
            nha_san_xuat='MSD', nuoc_san_xuat='My',
            do_tuoi_min_thang=9, do_tuoi_max_thang=1200, gia=320000)
        viemganb = VacXin.objects.create(
            ten='Vac-xin Viem gan B (Engerix B)', phong_benh='Viem gan B',
            nha_san_xuat='GSK', nuoc_san_xuat='Bi',
            do_tuoi_min_thang=0, do_tuoi_max_thang=1200, gia=220000)
        cum = VacXin.objects.create(
            ten='Vac-xin Cum (Vaxigrip Tetra)', phong_benh='Cum mua',
            nha_san_xuat='Sanofi Pasteur', nuoc_san_xuat='Phap',
            do_tuoi_min_thang=6, do_tuoi_max_thang=1200, gia=350000)
        hpv = VacXin.objects.create(
            ten='Vac-xin HPV (Gardasil 9)',
            phong_benh='Ung thu co tu cung, sui mao ga',
            nha_san_xuat='MSD', nuoc_san_xuat='My',
            do_tuoi_min_thang=108, do_tuoi_max_thang=540, gia=3000000)

        # ----- 2. PHAC DO + CHI TIET MUI -----
        pd_6in1 = PhacDo.objects.create(
            ten='Phac do 6 trong 1 - co ban', nhom='tre_em', doi_tuong='Tre tu 2 thang tuoi',
            mo_ta='3 mui co ban cach nhau 1 thang, mui nhac luc 16-18 thang.')
        PhacDoChiTiet.objects.bulk_create([
            PhacDoChiTiet(phac_do=pd_6in1, vac_xin=hexaxim, mui_so=1, khoang_cach_ngay=0),
            PhacDoChiTiet(phac_do=pd_6in1, vac_xin=hexaxim, mui_so=2, khoang_cach_ngay=30),
            PhacDoChiTiet(phac_do=pd_6in1, vac_xin=hexaxim, mui_so=3, khoang_cach_ngay=30),
            PhacDoChiTiet(phac_do=pd_6in1, vac_xin=hexaxim, mui_so=4, khoang_cach_ngay=365),
        ])

        pd_mmr = PhacDo.objects.create(
            ten='Phac do Soi - Quai bi - Rubella', nhom='tre_em', doi_tuong='Tre tu 9 thang tuoi',
            mo_ta='2 mui, cach nhau toi thieu 3 thang.')
        PhacDoChiTiet.objects.bulk_create([
            PhacDoChiTiet(phac_do=pd_mmr, vac_xin=mmr, mui_so=1, khoang_cach_ngay=0),
            PhacDoChiTiet(phac_do=pd_mmr, vac_xin=mmr, mui_so=2, khoang_cach_ngay=90),
        ])

        pd_hpv = PhacDo.objects.create(
            ten='Phac do HPV - nguoi lon', nhom='nguoi_lon', doi_tuong='Nu 9-45 tuoi',
            mo_ta='3 mui theo lich 0 - 2 - 6 thang.')
        PhacDoChiTiet.objects.bulk_create([
            PhacDoChiTiet(phac_do=pd_hpv, vac_xin=hpv, mui_so=1, khoang_cach_ngay=0),
            PhacDoChiTiet(phac_do=pd_hpv, vac_xin=hpv, mui_so=2, khoang_cach_ngay=60),
            PhacDoChiTiet(phac_do=pd_hpv, vac_xin=hpv, mui_so=3, khoang_cach_ngay=180),
        ])

        # ----- 3. LO VAC-XIN (1 lo sap het han de demo canh bao) -----
        LoVacXin.objects.create(vac_xin=hexaxim, so_lo='HX2026A',
                                ngay_nhap=today - timedelta(days=60),
                                han_su_dung=today + timedelta(days=300), so_luong_ton=120)
        LoVacXin.objects.create(vac_xin=mmr, so_lo='MMR2026B',
                                ngay_nhap=today - timedelta(days=90),
                                han_su_dung=today + timedelta(days=20), so_luong_ton=15)  # SAP HET HAN
        LoVacXin.objects.create(vac_xin=hpv, so_lo='HPV2026C',
                                ngay_nhap=today - timedelta(days=30),
                                han_su_dung=today + timedelta(days=400), so_luong_ton=40)

        # ----- 4. KHACH HANG + MUI TIEM (cac kich ban nhac mui) -----
        # (ho_ten, ngay_sinh_offset_ngay, sdt, phac_do, vac_xin, ngay_tiem_mui1_cach_day)
        kich_ban = [
            ('Be Nguyen Minh An', 6 * 30, '0901000001', pd_6in1, hexaxim, 40),   # QUA HAN (hen -10)
            ('Be Tran Bao Ngoc', 5 * 30, '0901000002', pd_6in1, hexaxim, 27),    # SAP TOI (hen +3)
            ('Be Hoang Nhat Minh', 4 * 30, '0901000003', pd_6in1, hexaxim, 10),  # CHUA TOI (hen +20)
            ('Be Le Gia Han', 12 * 30, '0901000004', pd_mmr, mmr, 89),           # SAP TOI (hen +1)
            ('Chi Pham Thi Huong', 28 * 365, '0901000005', pd_hpv, hpv, 62),     # QUA HAN (hen -2)
        ]

        for ho_ten, tuoi_ngay, sdt, pd, vx, cach_day in kich_ban:
            kh = KhachHang.objects.create(
                ho_ten=ho_ten, ngay_sinh=today - timedelta(days=tuoi_ngay),
                gioi_tinh='Nu' if 'Chi' in ho_ten or 'Han' in ho_ten or 'Ngoc' in ho_ten else 'Nam',
                so_dien_thoai=sdt, dia_chi='TP. Ho Chi Minh')
            # Ghi nhan mui 1 -> save() tu dong tinh ngay_hen_mui_ke
            MuiTiem.objects.create(
                khach_hang=kh, vac_xin=vx, phac_do=pd, mui_so=1,
                ngay_tiem=today - timedelta(days=cach_day),
                nguoi_tiem=nguoi_tiem, vi_tri_tiem='Bap tay trai')

        # Mot khach da tiem du mui cuoi -> ngay_hen_mui_ke = None
        kh_xong = KhachHang.objects.create(
            ho_ten='Be Vo Khanh Vy', ngay_sinh=today - timedelta(days=20 * 30),
            gioi_tinh='Nu', so_dien_thoai='0901000006', dia_chi='TP. Ho Chi Minh')
        MuiTiem.objects.create(khach_hang=kh_xong, vac_xin=mmr, phac_do=pd_mmr,
                               mui_so=2, ngay_tiem=today - timedelta(days=5),
                               nguoi_tiem=nguoi_tiem, vi_tri_tiem='Bap tay trai')

        # ----- 5. VAI LICH HEN sap toi -----
        LichHen.objects.create(khach_hang=KhachHang.objects.get(so_dien_thoai='0901000002'),
                               ngay_hen=today + timedelta(days=3), phac_do=pd_6in1,
                               trang_thai='xacnhan', ghi_chu='Mui 2 - 6 trong 1')
        LichHen.objects.create(khach_hang=KhachHang.objects.get(so_dien_thoai='0901000004'),
                               ngay_hen=today + timedelta(days=1), phac_do=pd_mmr,
                               trang_thai='cho', ghi_chu='Mui 2 - MMR')

        # ----- TONG KET + DANH SACH NHAC MUI -----
        self.stdout.write(self.style.SUCCESS(
            f'\nDA TAO XONG: {VacXin.objects.count()} vac-xin, '
            f'{PhacDo.objects.count()} phac do, {KhachHang.objects.count()} khach hang, '
            f'{MuiTiem.objects.count()} mui tiem.\n'))

        self.stdout.write('=== KHACH DEN HAN NHAC MUI (han <= 7 ngay toi hoac da qua han) ===')
        han_chot = today + timedelta(days=7)
        ds_nhac = MuiTiem.objects.filter(
            ngay_hen_mui_ke__isnull=False,
            ngay_hen_mui_ke__lte=han_chot).order_by('ngay_hen_mui_ke')
        if not ds_nhac:
            self.stdout.write('  (khong co)')
        for mt in ds_nhac:
            so_ngay = (mt.ngay_hen_mui_ke - today).days
            trang_thai = f'QUA HAN {-so_ngay} ngay' if so_ngay < 0 else f'con {so_ngay} ngay'
            self.stdout.write(
                f'  - {mt.khach_hang.ho_ten}: tiem mui {mt.mui_so + 1} ({mt.vac_xin.ten}) '
                f'vao {mt.ngay_hen_mui_ke}  [{trang_thai}]')
