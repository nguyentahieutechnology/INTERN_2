"""Context processors: thong bao (chuong) + co vai tro cho navbar."""
from core.models import ThongBao, TinNhanHoTro, YeuCauDatLaiMatKhau


def thong_bao(request):
    if not request.user.is_authenticated:
        return {}
    qs = ThongBao.objects.filter(nguoi_nhan=request.user)
    return {
        'tb_chua_doc': qs.filter(da_doc=False).count(),
        'tb_list': qs[:8],
    }


def vai_tro(request):
    """Co tien loi de an/hien menu theo vai tro."""
    u = request.user
    if not u.is_authenticated:
        return {}
    nhom = set(u.groups.values_list('name', flat=True))
    return {
        'la_le_tan': 'Le tan' in nhom,
        'la_bac_si': 'Bac si' in nhom,
        'la_dieu_duong': 'Dieu duong' in nhom,
        'la_thu_kho': 'Thu kho' in nhom,
    }


def yeu_cau_mat_khau(request):
    """So yeu cau dat lai mat khau dang cho (hien badge cho admin)."""
    u = request.user
    if not u.is_authenticated or not u.is_superuser:
        return {}
    return {'so_yc_mat_khau': YeuCauDatLaiMatKhau.objects.filter(da_xu_ly=False).count()}


def ho_tro_chua_doc(request):
    """So hoi thoai ho tro co tin khach chua doc (badge cho le tan/admin)."""
    u = request.user
    if not u.is_authenticated:
        return {}
    if u.is_superuser or u.groups.filter(name='Le tan').exists():
        n = (TinNhanHoTro.objects.filter(la_nhan_vien=False, da_doc=False)
             .values('khach').distinct().count())
        return {'so_ho_tro_chua_doc': n}
    return {}
