"""
Them lo (ton kho) cho cac vac-xin chua co lo.
Chay:  python manage.py seed_lo   (idempotent - chi them cho vac-xin chua co lo con ton)
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import LoVacXin, VacXin


class Command(BaseCommand):
    help = 'Them lo cho cac vac-xin con thieu'

    def add_arguments(self, parser):
        parser.add_argument('--so-luong', type=int, default=100,
                            help='So luong ton moi lo (mac dinh 100)')

    def handle(self, *args, **options):
        today = timezone.now().date()
        so_luong = options['so_luong']
        them = 0

        for vx in VacXin.objects.all().order_by('ten'):
            # Bo qua neu da co lo con ton
            if vx.lo.filter(so_luong_ton__gt=0).exists():
                continue
            so_lo = f'LO{vx.id:03d}-2026'
            _, created = LoVacXin.objects.get_or_create(
                vac_xin=vx, so_lo=so_lo,
                defaults=dict(
                    ngay_nhap=today - timedelta(days=15),
                    han_su_dung=today + timedelta(days=540),
                    so_luong_ton=so_luong))
            if created:
                them += 1
                self.stdout.write(f'  + {vx.ten}: lo {so_lo}, ton {so_luong}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDa them {them} lo. Tong so lo: {LoVacXin.objects.count()}. '
            f'Vac-xin co ton kho: '
            f'{VacXin.objects.filter(lo__so_luong_ton__gt=0).distinct().count()}/'
            f'{VacXin.objects.count()}'))
