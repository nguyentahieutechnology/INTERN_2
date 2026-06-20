"""
Them danh muc vac-xin day du (tre em + nguoi lon).
Chay:  python manage.py seed_vacxin   (chay lai nhieu lan khong trung - dung get_or_create)

Phan loai theo do tuoi (giong views.py):
  - Tre em   : do_tuoi_min_thang < 108  (duoi 9 tuoi)
  - Nguoi lon: do_tuoi_max_thang >= 216 (tu 18 tuoi)
Nhieu vac-xin thuoc CA HAI nhom (vd Cum, Thuy dau) - dung thuc te.
"""
from django.core.management.base import BaseCommand

from core.models import VacXin

# Chuan hoa ten 5 vac-xin cu (khong dau) -> co dau tieng Viet
DOI_TEN = {
    'Vac-xin 6 trong 1 (Hexaxim)': 'Vắc-xin 6 trong 1 (Hexaxim)',
    'Vac-xin Soi - Quai bi - Rubella (MMR II)': 'Vắc-xin Sởi - Quai bị - Rubella (MMR II)',
    'Vac-xin Viem gan B (Engerix B)': 'Vắc-xin Viêm gan B (Engerix B)',
    'Vac-xin Cum (Vaxigrip Tetra)': 'Vắc-xin Cúm (Vaxigrip Tetra)',
    'Vac-xin HPV (Gardasil 9)': 'Vắc-xin HPV (Gardasil 9)',
}

# (ten, phong_benh, nha_san_xuat, nuoc_san_xuat, tuoi_min_thang, tuoi_max_thang, gia)
DANH_MUC = [
    # ----- Nhom co san (chuan hoa) -----
    ('Vắc-xin 6 trong 1 (Hexaxim)', 'Bạch hầu, Ho gà, Uốn ván, Bại liệt, Hib, Viêm gan B',
     'Sanofi Pasteur', 'Pháp', 2, 24, 1015000),
    ('Vắc-xin Sởi - Quai bị - Rubella (MMR II)', 'Sởi, Quai bị, Rubella',
     'MSD', 'Mỹ', 9, 1200, 320000),
    ('Vắc-xin Viêm gan B (Engerix B)', 'Viêm gan B', 'GSK', 'Bỉ', 0, 1200, 220000),
    ('Vắc-xin Cúm (Vaxigrip Tetra)', 'Cúm mùa', 'Sanofi Pasteur', 'Pháp', 6, 1200, 350000),
    ('Vắc-xin HPV (Gardasil 9)', 'Ung thư cổ tử cung, sùi mào gà', 'MSD', 'Mỹ', 108, 540, 3000000),

    # ----- Vac-xin thien ve TRE EM (tuoi_min < 108) -----
    ('Vắc-xin Lao (BCG)', 'Bệnh lao', 'Viện Vắc-xin IVAC', 'Việt Nam', 0, 12, 150000),
    ('Vắc-xin Rotavirus (Rotarix)', 'Tiêu chảy cấp do Rotavirus', 'GSK', 'Bỉ', 2, 6, 820000),
    ('Vắc-xin Phế cầu (Synflorix)', 'Viêm phổi, viêm tai giữa do phế cầu', 'GSK', 'Bỉ', 2, 60, 1045000),
    ('Vắc-xin Thủy đậu (Varivax)', 'Thủy đậu', 'MSD', 'Mỹ', 12, 1200, 970000),
    ('Vắc-xin Viêm não Nhật Bản (Imojev)', 'Viêm não Nhật Bản', 'Sanofi Pasteur', 'Thái Lan', 9, 1200, 720000),
    ('Vắc-xin Viêm gan A (Avaxim)', 'Viêm gan A', 'Sanofi Pasteur', 'Pháp', 12, 1200, 660000),
    ('Vắc-xin Não mô cầu BC (VA-Mengoc-BC)', 'Viêm màng não do não mô cầu B, C', 'Finlay', 'Cuba', 6, 540, 290000),

    # ----- Vac-xin thien ve NGUOI LON (tuoi_max >= 216) -----
    ('Vắc-xin Uốn ván hấp phụ (VAT)', 'Uốn ván', 'IVAC', 'Việt Nam', 108, 1200, 130000),
    ('Vắc-xin Zona thần kinh (Shingrix)', 'Zona thần kinh (giời leo)', 'GSK', 'Bỉ', 600, 1200, 3800000),
    ('Vắc-xin Não mô cầu ACYW (Menactra)', 'Viêm màng não do não mô cầu A, C, Y, W-135',
     'Sanofi Pasteur', 'Mỹ', 9, 660, 1280000),
    ('Vắc-xin Dại (Verorab)', 'Bệnh dại', 'Sanofi Pasteur', 'Pháp', 0, 1200, 350000),
    ('Vắc-xin Thương hàn (Typhim Vi)', 'Thương hàn', 'Sanofi Pasteur', 'Pháp', 24, 1200, 380000),
]


class Command(BaseCommand):
    help = 'Them danh muc vac-xin tre em + nguoi lon'

    def handle(self, *args, **options):
        # 1. Chuan hoa ten cu
        for cu, moi in DOI_TEN.items():
            if VacXin.objects.filter(ten=cu).update(ten=moi):
                self.stdout.write(f'  Đổi tên: {cu} -> {moi}')

        # 2. Them moi (khong trung)
        them = da_co = 0
        for ten, pb, nsx, nuoc, mn, mx, gia in DANH_MUC:
            _, created = VacXin.objects.get_or_create(
                ten=ten,
                defaults=dict(phong_benh=pb, nha_san_xuat=nsx, nuoc_san_xuat=nuoc,
                              do_tuoi_min_thang=mn, do_tuoi_max_thang=mx, gia=gia))
            if created:
                them += 1
            else:
                da_co += 1

        # 3. Tong ket theo nhom
        tre_em = VacXin.objects.filter(do_tuoi_min_thang__lt=108).order_by('ten')
        nguoi_lon = VacXin.objects.filter(do_tuoi_max_thang__gte=216).order_by('ten')

        self.stdout.write(self.style.SUCCESS(
            f'\nThêm mới {them}, đã có sẵn {da_co}. Tổng vắc-xin: {VacXin.objects.count()}'))
        self.stdout.write(f'\n=== VẮC XIN TRẺ EM ({tre_em.count()}) ===')
        for v in tre_em:
            self.stdout.write(f'  - {v.ten}')
        self.stdout.write(f'\n=== VẮC XIN NGƯỜI LỚN ({nguoi_lon.count()}) ===')
        for v in nguoi_lon:
            self.stdout.write(f'  - {v.ten}')
