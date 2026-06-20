"""
Tao 4 nhom vai tro + gan quyen + tao tai khoan demo cho moi vai tro.
Chay SAU khi da migrate:  python manage.py setup_roles

4 vai tro:
  - Quan tri      : toan quyen tren nghiep vu
  - Le tan        : khach hang, lich hen, thanh toan
  - Bac si        : phieu sang loc + xem khach/lich
  - Dieu duong    : mui tiem + kho lo + xem khach
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.db import transaction


def crud(model, *actions):
    """Sinh ma quyen kieu 'add_khachhang', 'view_lichhen'..."""
    return [f'{a}_{model}' for a in actions]


# Ma quyen cho tung vai tro (cac model thuoc app 'core')
QUYEN_VAI_TRO = {
    'Le tan': (
        crud('khachhang', 'add', 'change', 'view')
        + crud('lichhen', 'add', 'change', 'delete', 'view')
        + crud('thanhtoan', 'add', 'change', 'view')
        + crud('vacxin', 'view')
        + crud('phacdo', 'view')
    ),
    'Bac si': (
        crud('phieusangloc', 'add', 'change', 'view')
        + crud('khachhang', 'view')
        + crud('lichhen', 'change', 'view')
        + crud('vacxin', 'view')
        + crud('phacdo', 'view')
    ),
    'Dieu duong': (
        crud('muitiem', 'add', 'change', 'view')
        + crud('lovacxin', 'change', 'view')
        + crud('khachhang', 'view')
        + crud('vacxin', 'view')
        + crud('phacdo', 'view')
    ),
    'Thu kho': (
        crud('lovacxin', 'add', 'change', 'view')
        + crud('vacxin', 'view')
    ),
    # Quan tri: gan TAT CA quyen cua app core (xu ly rieng ben duoi)
    'Quan tri': '__all__',
    # Khach hang: tu dang ky, khong co quyen quan tri (chi xem ho so cua minh)
    'Khach hang': [],
}

# Tai khoan demo cho moi vai tro (username, password, group)
TAI_KHOAN_DEMO = [
    ('letan', 'letan123', 'Le tan', 'Nguyen Thi Le Tan'),
    ('bacsi', 'bacsi123', 'Bac si', 'Tran Van Bac Si'),
    ('dieuduong', 'dieuduong123', 'Dieu duong', 'Le Thi Dieu Duong'),
    ('thukho', 'thukho123', 'Thu kho', 'Pham Van Thu Kho'),
]


class Command(BaseCommand):
    help = 'Tao nhom vai tro, gan quyen va tao tai khoan demo'

    @transaction.atomic
    def handle(self, *args, **options):
        for ten_nhom, ma_quyen in QUYEN_VAI_TRO.items():
            nhom, _ = Group.objects.get_or_create(name=ten_nhom)
            if ma_quyen == '__all__':
                ds_quyen = Permission.objects.filter(content_type__app_label='core')
            else:
                ds_quyen = Permission.objects.filter(
                    codename__in=ma_quyen, content_type__app_label='core')
            nhom.permissions.set(ds_quyen)
            self.stdout.write(self.style.SUCCESS(
                f'  Nhom "{ten_nhom}": {ds_quyen.count()} quyen'))

        self.stdout.write('--- Tao tai khoan demo ---')
        for username, password, ten_nhom, ho_ten in TAI_KHOAN_DEMO:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'first_name': ho_ten, 'is_staff': True})
            user.is_staff = True          # can is_staff de vao trang Admin
            user.set_password(password)
            user.save()
            user.groups.set([Group.objects.get(name=ten_nhom)])
            trang_thai = 'tao moi' if created else 'cap nhat'
            self.stdout.write(
                f'  {username} / {password}  -> nhom {ten_nhom}  ({trang_thai})')

        self.stdout.write(self.style.SUCCESS(
            '\nXong. Tai khoan admin (superuser) van co toan quyen.'))
