import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import LoVacXin


def tru_thang(ngay, so_thang):
    """Tru lui so_thang thang khoi 1 date, giu ngay (clamp cuoi thang)."""
    thang = ngay.month - 1 - so_thang
    nam = ngay.year + thang // 12
    thang = thang % 12 + 1
    # clamp ngay neu thang dich khong du ngay (vd 31 -> 28/30)
    import calendar
    ngay_max = calendar.monthrange(nam, thang)[1]
    return ngay.replace(year=nam, month=thang, day=min(ngay.day, ngay_max))


lots = LoVacXin.objects.filter(ngay_san_xuat__isnull=True).select_related('vac_xin')
cap_nhat = 0
for lo in lots:
    thang = lo.vac_xin.han_dung_thang or 24
    nsx = tru_thang(lo.han_su_dung, thang)
    if nsx > lo.ngay_nhap:          # NSX khong the sau ngay nhap
        nsx = lo.ngay_nhap
    lo.ngay_san_xuat = nsx
    lo.save(update_fields=['ngay_san_xuat'])
    cap_nhat += 1
    print(f'  {lo.vac_xin.ten} - Lo {lo.so_lo}: NSX={nsx}  (nhap {lo.ngay_nhap}, HSD {lo.han_su_dung}, han {thang} thang)')

print(f'\nDa cap nhat {cap_nhat} lo. Con trong: {LoVacXin.objects.filter(ngay_san_xuat__isnull=True).count()}')
