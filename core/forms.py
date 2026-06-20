from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from core.models import (KhachHang, LichHen, LoVacXin, MuiTiem,
                         PhacDo, PhacDoChiTiet, TheoDoiSauTiem, VacXin)


class DangKyForm(UserCreationForm):
    """Form khach hang tu dang ky tai khoan + tao ho so KhachHang."""
    ho_ten = forms.CharField(label='Họ và tên', max_length=100)
    gioi_tinh = forms.ChoiceField(label='Giới tính', choices=KhachHang.GIOI_TINH)
    so_dien_thoai = forms.CharField(label='Số điện thoại', max_length=15)
    ngay_sinh = forms.DateField(
        label='Ngày sinh',
        widget=forms.DateInput(attrs={'type': 'date'}))

    field_order = ['username', 'ho_ten', 'gioi_tinh', 'so_dien_thoai', 'ngay_sinh',
                   'password1', 'password2']

    class Meta:
        model = User
        fields = ['username']
        labels = {'username': 'Tên đăng nhập'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password2'].label = 'Xác nhận mật khẩu'
        for name, field in self.fields.items():
            # Select dung 'form-select', cac o khac dung 'form-control'
            css = 'form-select' if name == 'gioi_tinh' else 'form-control'
            field.widget.attrs['class'] = css

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['ho_ten']
        user.is_staff = False                       # khach hang KHONG vao trang quan tri
        if commit:
            user.save()
            # Tao ho so khach hang gan voi tai khoan
            KhachHang.objects.create(
                user=user,
                ho_ten=self.cleaned_data['ho_ten'],
                gioi_tinh=self.cleaned_data['gioi_tinh'],
                ngay_sinh=self.cleaned_data['ngay_sinh'],
                so_dien_thoai=self.cleaned_data['so_dien_thoai'])
            # Gan vao nhom "Khach hang"
            nhom, _ = Group.objects.get_or_create(name='Khach hang')
            user.groups.add(nhom)
        return user


class DatLichForm(forms.ModelForm):
    """Form khach hang dat lich hen tiem."""

    class Meta:
        model = LichHen
        fields = ['khach_hang', 'vac_xin', 'phac_do', 'ngay_hen', 'gio_hen',
                  'loai_chi_dinh', 'benh_vien', 'bac_si_chi_dinh', 'ghi_chu']
        labels = {
            'khach_hang': 'Người được tiêm',
            'vac_xin': 'Vắc-xin đăng ký',
            'phac_do': 'Gói tiêm / Phác đồ (tùy chọn)',
            'ngay_hen': 'Ngày hẹn',
            'gio_hen': 'Giờ hẹn (tùy chọn)',
            'loai_chi_dinh': 'Hình thức chỉ định',
            'benh_vien': 'Bệnh viện chỉ định',
            'bac_si_chi_dinh': 'Bác sĩ chỉ định',
            'ghi_chu': 'Ghi chú (tùy chọn)',
        }
        widgets = {
            'ngay_hen': forms.DateInput(attrs={'type': 'date'}),
            'gio_hen': forms.TimeInput(attrs={'type': 'time'}),
            'loai_chi_dinh': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'ghi_chu': forms.TextInput(),
        }

    def __init__(self, *args, ho_so=None, **kwargs):
        super().__init__(*args, **kwargs)
        if ho_so is not None:
            self.fields['khach_hang'].queryset = ho_so
        self.fields['vac_xin'].required = True   # khach phai chon vac-xin
        for name, field in self.fields.items():
            if name == 'loai_chi_dinh':
                continue                       # radio - khong gan form-control
            css = 'form-select' if name in ('khach_hang', 'vac_xin', 'phac_do') else 'form-control'
            field.widget.attrs['class'] = css

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('loai_chi_dinh') == 'benh_vien' and not cleaned.get('benh_vien'):
            self.add_error('benh_vien', 'Vui lòng nhập tên bệnh viện chỉ định.')
        return cleaned


class TaiKhamForm(forms.ModelForm):
    """Le tan dat lich tai kham sau phan ung (chi thong tin co ban)."""

    class Meta:
        model = LichHen
        fields = ['khach_hang', 'ngay_hen', 'gio_hen', 'ghi_chu']
        labels = {
            'khach_hang': 'Người được tiêm',
            'ngay_hen': 'Ngày hẹn',
            'gio_hen': 'Giờ hẹn',
            'ghi_chu': 'Ghi chú',
        }
        widgets = {
            'ngay_hen': forms.DateInput(attrs={'type': 'date'}),
            'gio_hen': forms.TimeInput(attrs={'type': 'time'}),
            'ghi_chu': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, ho_so=None, **kwargs):
        super().__init__(*args, **kwargs)
        if ho_so is not None:
            self.fields['khach_hang'].queryset = ho_so
        for name, field in self.fields.items():
            css = 'form-select' if name == 'khach_hang' else 'form-control'
            field.widget.attrs['class'] = css


class NguoiThanForm(forms.ModelForm):
    """Form them ho so nguoi than."""

    class Meta:
        model = KhachHang
        fields = ['ho_ten', 'quan_he', 'gioi_tinh', 'ngay_sinh', 'so_dien_thoai']
        labels = {
            'ho_ten': 'Họ và tên',
            'quan_he': 'Quan hệ với bạn',
            'gioi_tinh': 'Giới tính',
            'ngay_sinh': 'Ngày sinh',
            'so_dien_thoai': 'Số điện thoại',
        }
        widgets = {'ngay_sinh': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quan_he'].choices = [c for c in KhachHang.QUAN_HE if c[0] != 'ban_than']
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css


class TheoDoiForm(forms.ModelForm):
    """Form khach hang ghi nhan theo doi sau tiem (chi mui tiem cua minh)."""

    class Meta:
        model = TheoDoiSauTiem
        fields = ['mui_tiem', 'thoi_diem', 'nhiet_do', 'trieu_chung', 'muc_do', 'ghi_chu']
        labels = {
            'mui_tiem': 'Mũi tiêm',
            'thoi_diem': 'Thời điểm theo dõi',
            'nhiet_do': 'Nhiệt độ (°C)',
            'trieu_chung': 'Triệu chứng (nếu có)',
            'muc_do': 'Mức độ',
            'ghi_chu': 'Ghi chú',
        }
        widgets = {
            'ghi_chu': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, mui_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if mui_queryset is not None:
            self.fields['mui_tiem'].queryset = mui_queryset
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css


class KhachHangForm(forms.ModelForm):
    """Form le tan them khach hang (tiep don tai quay)."""

    class Meta:
        model = KhachHang
        fields = ['ho_ten', 'gioi_tinh', 'ngay_sinh', 'so_dien_thoai', 'cccd', 'dia_chi']
        labels = {
            'ho_ten': 'Họ và tên',
            'gioi_tinh': 'Giới tính',
            'ngay_sinh': 'Ngày sinh',
            'so_dien_thoai': 'Số điện thoại',
            'cccd': 'CCCD/CMND',
            'dia_chi': 'Địa chỉ',
        }
        widgets = {'ngay_sinh': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css

    def clean_ho_ten(self):
        # Viet hoa chu cai dau moi tu
        ten = self.cleaned_data.get('ho_ten', '').strip()
        return ' '.join(w.capitalize() for w in ten.split())

    def clean_so_dien_thoai(self):
        sdt = self.cleaned_data.get('so_dien_thoai', '').strip()
        if not sdt.isdigit() or len(sdt) != 10:
            raise forms.ValidationError('Số điện thoại phải gồm đúng 10 chữ số.')
        return sdt


class TaiKhoanNhanVienForm(forms.Form):
    """Admin tao tai khoan nhan vien + gan vai tro."""
    VAI_TRO = [
        ('Le tan', 'Lễ tân'),
        ('Bac si', 'Bác sĩ'),
        ('Dieu duong', 'Điều dưỡng'),
        ('Thu kho', 'Thủ kho'),
        ('Quan tri', 'Quản trị'),
    ]
    username = forms.CharField(label='Tên đăng nhập', max_length=150)
    ho_ten = forms.CharField(label='Họ và tên', max_length=150, required=False)
    mat_khau = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput, min_length=6)
    vai_tro = forms.ChoiceField(label='Vai trò', choices=VAI_TRO)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'form-select' if name == 'vai_tro' else 'form-control'
            field.widget.attrs['class'] = css

    def clean_username(self):
        u = self.cleaned_data['username'].strip()
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('Tên đăng nhập đã tồn tại.')
        return u

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['mat_khau'],
            first_name=self.cleaned_data.get('ho_ten', ''))
        user.is_staff = True
        user.save()
        nhom, _ = Group.objects.get_or_create(name=self.cleaned_data['vai_tro'])
        user.groups.add(nhom)
        return user


class SuaNhanVienForm(forms.Form):
    """Admin sua thong tin + vai tro + mat khau nhan vien."""
    ho_ten = forms.CharField(label='Họ và tên', max_length=150, required=False)
    vai_tro = forms.ChoiceField(label='Vai trò', choices=TaiKhoanNhanVienForm.VAI_TRO)
    mat_khau_moi = forms.CharField(label='Mật khẩu mới (để trống nếu không đổi)',
                                   widget=forms.PasswordInput, required=False, min_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'form-select' if name == 'vai_tro' else 'form-control'
            field.widget.attrs['class'] = css


class VacXinForm(forms.ModelForm):
    """Admin them/sua vac-xin."""

    class Meta:
        model = VacXin
        fields = ['ten', 'phong_benh', 'nha_san_xuat', 'nuoc_san_xuat',
                  'do_tuoi_min_thang', 'do_tuoi_max_thang', 'han_dung_thang', 'gia']
        labels = {
            'ten': 'Tên vắc-xin',
            'phong_benh': 'Phòng bệnh',
            'nha_san_xuat': 'Nhà sản xuất',
            'nuoc_san_xuat': 'Nước sản xuất',
            'do_tuoi_min_thang': 'Tuổi tối thiểu (tháng)',
            'do_tuoi_max_thang': 'Tuổi tối đa (tháng)',
            'han_dung_thang': 'Tổng hạn dùng (tháng)',
            'gia': 'Giá (VND)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LoVacXinForm(forms.ModelForm):
    """Form thu kho nhap lo vac-xin."""

    class Meta:
        model = LoVacXin
        fields = ['vac_xin', 'so_lo', 'ngay_san_xuat', 'ngay_nhap', 'han_su_dung', 'so_luong_ton']
        labels = {
            'vac_xin': 'Vắc-xin',
            'so_lo': 'Số lô',
            'ngay_san_xuat': 'Ngày sản xuất',
            'ngay_nhap': 'Ngày nhập',
            'han_su_dung': 'Hạn sử dụng',
            'so_luong_ton': 'Số lượng',
        }
        widgets = {
            'ngay_san_xuat': forms.DateInput(attrs={'type': 'date'}),
            'ngay_nhap': forms.DateInput(attrs={'type': 'date'}),
            'han_su_dung': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css

    def clean(self):
        cleaned = super().clean()
        nhap = cleaned.get('ngay_nhap')
        han = cleaned.get('han_su_dung')
        vx = cleaned.get('vac_xin')
        sx = cleaned.get('ngay_san_xuat')
        if sx and nhap and sx > nhap:
            self.add_error('ngay_san_xuat', 'Ngày sản xuất phải trước hoặc bằng ngày nhập.')
        if sx and han and sx >= han:
            self.add_error('ngay_san_xuat', 'Ngày sản xuất phải trước hạn sử dụng.')
        if nhap and han and han <= nhap:
            self.add_error('han_su_dung', 'Hạn sử dụng phải sau ngày nhập.')
        elif nhap and han and vx:
            con_lai = (han - nhap).days
            tong = vx.han_dung_thang * 30          # tong han dung (xap xi ngay)
            if con_lai < tong / 2:
                self.add_error('han_su_dung',
                    f'HSD còn lại {con_lai} ngày — chưa đạt 50% tổng hạn dùng '
                    f'({vx.han_dung_thang} tháng ≈ {tong} ngày). '
                    f'Cần còn tối thiểu {tong // 2} ngày tính từ ngày nhập.')
        return cleaned


class PhacDoForm(forms.ModelForm):
    """Admin tao/sua phac do (phan master)."""

    class Meta:
        model = PhacDo
        fields = ['ten', 'nhom', 'doi_tuong', 'mo_ta']
        labels = {
            'ten': 'Tên phác đồ',
            'nhom': 'Nhóm đối tượng',
            'doi_tuong': 'Đối tượng áp dụng',
            'mo_ta': 'Mô tả',
        }
        widgets = {
            'doi_tuong': forms.TextInput(
                attrs={'placeholder': 'Vd: Trẻ từ 2 tháng tuổi, người lớn...'}),
            'mo_ta': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css


class PhacDoChiTietForm(forms.ModelForm):
    """Mot mui trong phac do (vac-xin + khoang cach)."""

    class Meta:
        model = PhacDoChiTiet
        fields = ['mui_so', 'vac_xin', 'khoang_cach_ngay']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select form-select-sm'
            else:
                field.widget.attrs['class'] = 'form-control form-control-sm'


class BasePhacDoChiTietFormSet(forms.BaseInlineFormSet):
    """Kiem tra hop le toan bo cac mui trong 1 phac do."""

    def clean(self):
        super().clean()
        if any(self.errors):
            return  # da co loi tung dong -> khong kiem tra cheo

        mui_list = []   # (mui_so, khoang_cach, form) cua cac dong hop le, chua xoa
        for form in self.forms:
            if not getattr(form, 'cleaned_data', None):
                continue
            if form.cleaned_data.get('DELETE'):
                continue
            mui_so = form.cleaned_data.get('mui_so')
            vac_xin = form.cleaned_data.get('vac_xin')
            if mui_so is None or vac_xin is None:
                continue
            mui_list.append((mui_so, form.cleaned_data.get('khoang_cach_ngay'), form))

        if not mui_list:
            raise forms.ValidationError('Phác đồ phải có ít nhất 1 mũi tiêm.')

        so_list = [m[0] for m in mui_list]

        # 1) Khong trung mui so
        trung = sorted({s for s in so_list if so_list.count(s) > 1})
        if trung:
            raise forms.ValidationError(
                'Mũi số bị trùng: ' + ', '.join(str(s) for s in trung) +
                '. Mỗi mũi phải có số thứ tự khác nhau.')

        # 2) Mui so phai bat dau tu 1 va lien tuc (1, 2, 3...)
        so_sorted = sorted(so_list)
        if so_sorted != list(range(1, len(so_sorted) + 1)):
            raise forms.ValidationError(
                'Mũi số phải bắt đầu từ 1 và liên tục (1, 2, 3…). '
                'Hiện đang là: ' + ', '.join(str(s) for s in so_sorted) + '.')

        # 3) Khoang cach: mui 1 = 0, mui sau > 0
        for mui_so, khoang_cach, form in mui_list:
            if mui_so == 1 and khoang_cach:
                form.add_error('khoang_cach_ngay', 'Mũi 1 phải để khoảng cách = 0.')
            elif mui_so > 1 and not khoang_cach:
                form.add_error('khoang_cach_ngay',
                               'Mũi từ 2 trở đi phải có khoảng cách > 0 ngày.')


# Formset chi tiet mui gan voi mot PhacDo (them/sua/xoa mui trong 1 lan luu)
PhacDoChiTietFormSet = forms.inlineformset_factory(
    PhacDo, PhacDoChiTiet, form=PhacDoChiTietForm,
    formset=BasePhacDoChiTietFormSet, extra=1, can_delete=True)

