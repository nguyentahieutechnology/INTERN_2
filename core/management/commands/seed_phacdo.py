"""
Tao phac do cho cac vac-xin chua co phac do nao (de dat lich co goi phu hop).
Chay:  python manage.py seed_phacdo   (idempotent)
"""
from django.core.management.base import BaseCommand

from core.models import PhacDo, PhacDoChiTiet, VacXin

# So mui mac dinh + khoang cach (ngay) cho phac do don gian theo ten vac-xin
# Neu khong khai bao -> 1 mui
PHAC_DO_MUI = {
    'Vắc-xin Lao (BCG)': [(1, 0)],
    'Vắc-xin Rotavirus (Rotarix)': [(1, 0), (2, 30)],
    'Vắc-xin Phế cầu (Synflorix)': [(1, 0), (2, 30), (3, 30)],
    'Vắc-xin Viêm gan A (Avaxim)': [(1, 0), (2, 180)],
    'Vắc-xin Não mô cầu BC (VA-Mengoc-BC)': [(1, 0), (2, 45)],
    'Vắc-xin Não mô cầu ACYW (Menactra)': [(1, 0), (2, 90)],
    'Vắc-xin Dại (Verorab)': [(1, 0), (2, 3), (3, 7)],
    'Vắc-xin Thương hàn (Typhim Vi)': [(1, 0)],
}


class Command(BaseCommand):
    help = 'Tao phac do cho cac vac-xin con thieu'

    def handle(self, *args, **options):
        them = 0
        for vx in VacXin.objects.all().order_by('ten'):
            # Bo qua neu vac-xin nay da nam trong mot phac do nao do
            if PhacDoChiTiet.objects.filter(vac_xin=vx).exists():
                continue
            nhom = 'tre_em' if vx.do_tuoi_min_thang < 108 else 'nguoi_lon'
            pd = PhacDo.objects.create(
                ten=f'Phác đồ {vx.ten}', nhom=nhom,
                doi_tuong=('Trẻ em' if nhom == 'tre_em' else 'Người lớn'),
                mo_ta=f'Phác đồ tiêm {vx.ten}.')
            mui = PHAC_DO_MUI.get(vx.ten, [(1, 0)])
            for mui_so, kc in mui:
                PhacDoChiTiet.objects.create(
                    phac_do=pd, vac_xin=vx, mui_so=mui_so, khoang_cach_ngay=kc)
            them += 1
            self.stdout.write(f'  + {pd.ten} ({len(mui)} mũi)')

        self.stdout.write(self.style.SUCCESS(
            f'\nĐã tạo {them} phác đồ. Tổng phác đồ: {PhacDo.objects.count()}. '
            f'Vắc-xin có phác đồ: '
            f'{VacXin.objects.filter(phacdochitiet__isnull=False).distinct().count()}/'
            f'{VacXin.objects.count()}'))
