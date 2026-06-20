"""
Them cac goi vac-xin (phac do) da phan loai tre em / nguoi lon.
Chay SAU seed_vacxin:  python manage.py seed_goi   (idempotent)
"""
from django.core.management.base import BaseCommand

from core.models import PhacDo, PhacDoChiTiet, VacXin

# Moi goi: ten, nhom, doi_tuong, mo_ta, danh sach mui (ten_vacxin, mui_so, khoang_cach_ngay)
GOI = [
    # ----- Tre em -----
    {'ten': 'Gói vắc xin Thủy đậu (trẻ em)', 'nhom': 'tre_em',
     'doi_tuong': 'Trẻ từ 12 tháng', 'mo_ta': '2 mũi phòng thủy đậu.',
     'mui': [('Vắc-xin Thủy đậu (Varivax)', 1, 0), ('Vắc-xin Thủy đậu (Varivax)', 2, 90)]},
    {'ten': 'Gói vắc xin Viêm não Nhật Bản (trẻ em)', 'nhom': 'tre_em',
     'doi_tuong': 'Trẻ từ 9 tháng', 'mo_ta': 'Phòng viêm não Nhật Bản.',
     'mui': [('Vắc-xin Viêm não Nhật Bản (Imojev)', 1, 0),
             ('Vắc-xin Viêm não Nhật Bản (Imojev)', 2, 365)]},

    # ----- Nguoi lon -----
    {'ten': 'Gói vắc xin Cúm mùa (người lớn)', 'nhom': 'nguoi_lon',
     'doi_tuong': 'Người lớn', 'mo_ta': 'Tiêm nhắc hằng năm.',
     'mui': [('Vắc-xin Cúm (Vaxigrip Tetra)', 1, 0)]},
    {'ten': 'Gói vắc xin Viêm gan B (người lớn)', 'nhom': 'nguoi_lon',
     'doi_tuong': 'Người lớn', 'mo_ta': 'Phác đồ 3 mũi 0 - 1 - 6 tháng.',
     'mui': [('Vắc-xin Viêm gan B (Engerix B)', 1, 0),
             ('Vắc-xin Viêm gan B (Engerix B)', 2, 30),
             ('Vắc-xin Viêm gan B (Engerix B)', 3, 180)]},
    {'ten': 'Gói vắc xin Uốn ván (người lớn)', 'nhom': 'nguoi_lon',
     'doi_tuong': 'Người lớn', 'mo_ta': 'Phác đồ uốn ván cơ bản 3 mũi.',
     'mui': [('Vắc-xin Uốn ván hấp phụ (VAT)', 1, 0),
             ('Vắc-xin Uốn ván hấp phụ (VAT)', 2, 30),
             ('Vắc-xin Uốn ván hấp phụ (VAT)', 3, 180)]},
]


class Command(BaseCommand):
    help = 'Them cac goi vac-xin da phan loai'

    def handle(self, *args, **options):
        them = 0
        for g in GOI:
            pd, created = PhacDo.objects.get_or_create(
                ten=g['ten'],
                defaults={'nhom': g['nhom'], 'doi_tuong': g['doi_tuong'], 'mo_ta': g['mo_ta']})
            pd.nhom = g['nhom']      # luon cap nhat nhom
            pd.save()
            if created:
                them += 1
                for ten_vx, mui_so, kc in g['mui']:
                    vx = VacXin.objects.filter(ten=ten_vx).first()
                    if not vx:
                        self.stdout.write(self.style.WARNING(
                            f'  ! Khong tim thay vac-xin: {ten_vx} (chay seed_vacxin truoc)'))
                        continue
                    PhacDoChiTiet.objects.create(
                        phac_do=pd, vac_xin=vx, mui_so=mui_so, khoang_cach_ngay=kc)

        tre = PhacDo.objects.filter(nhom='tre_em').count()
        lon = PhacDo.objects.filter(nhom='nguoi_lon').count()
        self.stdout.write(self.style.SUCCESS(
            f'\nThem moi {them} goi. Tong: {PhacDo.objects.count()} '
            f'(tre em: {tre}, nguoi lon: {lon})'))
