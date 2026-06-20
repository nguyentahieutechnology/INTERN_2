from django.contrib.auth import views as auth_views
from django.urls import path

from core import views

urlpatterns = [
    path('', views.index, name='index'),

    # Thanh menu phu (cong khai)
    path('dich-vu/', views.dich_vu, name='dich_vu'),
    path('vac-xin/tre-em/', views.vac_xin_tre_em, name='vac_xin_tre_em'),
    path('vac-xin/nguoi-lon/', views.vac_xin_nguoi_lon, name='vac_xin_nguoi_lon'),
    path('goi-vac-xin/', views.goi_vac_xin, name='goi_vac_xin'),
    path('goi-vac-xin/tre-em/', views.goi_vac_xin_tre_em, name='goi_vac_xin_tre_em'),
    path('goi-vac-xin/nguoi-lon/', views.goi_vac_xin_nguoi_lon, name='goi_vac_xin_nguoi_lon'),
    path('cam-nang/', views.cam_nang, name='cam_nang'),
    path('bang-gia/', views.bang_gia, name='bang_gia'),

    path('sau-dang-nhap/', views.sau_dang_nhap, name='sau_dang_nhap'),
    path('tong-quan/', views.dashboard, name='dashboard'),
    path('ca-nhan/', views.ca_nhan, name='ca_nhan'),
    path('ca-nhan/them-nguoi-than/', views.them_nguoi_than, name='them_nguoi_than'),
    path('ca-nhan/<int:pk>/', views.ho_so_chi_tiet, name='ho_so_chi_tiet'),
    path('ca-nhan/<int:pk>/sua/', views.khach_sua_ho_so, name='khach_sua_ho_so'),
    path('ca-nhan/<int:pk>/so-tiem-pdf/', views.so_tiem_pdf, name='so_tiem_pdf'),
    path('mui-tiem/<int:pk>/phieu-pdf/', views.phieu_tiem_pdf, name='phieu_tiem_pdf'),
    path('mui-tiem/<int:pk>/phieu/', views.phieu_tiem_xem, name='phieu_tiem_xem'),
    path('lich-hen/<int:lich_id>/huy/', views.khach_huy_lich, name='khach_huy_lich'),
    path('thanh-toan/<int:pk>/phieu-pdf/', views.phieu_thanh_toan_pdf, name='phieu_thanh_toan_pdf'),
    path('dat-lich/', views.dat_lich, name='dat_lich'),
    path('theo-doi-sau-tiem/', views.theo_doi_sau_tiem, name='theo_doi_sau_tiem'),
    path('thong-bao/<int:pk>/', views.xem_thong_bao, name='xem_thong_bao'),
    path('thong-bao/doc-het/', views.doc_het_thong_bao, name='doc_het_thong_bao'),
    path('ho-tro/tin/', views.ho_tro_tin, name='ho_tro_tin'),
    path('ho-tro/gui/', views.ho_tro_gui, name='ho_tro_gui'),
    path('le-tan/ho-tro/', views.le_tan_ho_tro, name='le_tan_ho_tro'),
    path('bao-cao/nhac-mui/', views.bao_cao_nhac_mui, name='bao_cao_nhac_mui'),

    # Khu vuc le tan
    path('le-tan/', views.le_tan_dashboard, name='le_tan_dashboard'),
    path('le-tan/bao-cao/pdf/', views.le_tan_bao_cao_pdf, name='le_tan_bao_cao_pdf'),
    path('le-tan/thong-ke/', views.le_tan_thong_ke, name='le_tan_thong_ke'),
    path('le-tan/lich-hen/', views.le_tan_lich_hen, name='le_tan_lich_hen'),
    path('le-tan/dang-ky-tiem/', views.le_tan_dang_ky_tiem, name='le_tan_dang_ky_tiem'),
    path('le-tan/tai-kham/', views.le_tan_tai_kham, name='le_tan_tai_kham'),
    path('bao-cao/nhac-mui/<int:pk>/nhac/', views.nhac_khach, name='nhac_khach'),
    path('le-tan/lich-hen/<int:pk>/da-den/', views.le_tan_da_den, name='le_tan_da_den'),
    path('le-tan/lich-hen/<int:pk>/<str:trang_thai>/', views.le_tan_doi_trang_thai, name='le_tan_doi_trang_thai'),
    path('le-tan/khach-hang/', views.le_tan_khach_hang, name='le_tan_khach_hang'),
    path('le-tan/khach-hang/<int:pk>/sua/', views.le_tan_khach_hang_sua, name='le_tan_khach_hang_sua'),

    # Quy trinh tiem
    path('quy-trinh/', views.quy_trinh_list, name='quy_trinh_list'),
    path('quy-trinh/<int:pk>/', views.quy_trinh_chi_tiet, name='quy_trinh_chi_tiet'),
    path('quy-trinh/<int:pk>/tiep-don/', views.qt_tiep_don, name='qt_tiep_don'),
    path('quy-trinh/<int:pk>/sang-loc/', views.qt_sang_loc, name='qt_sang_loc'),
    path('quy-trinh/<int:pk>/kham/', views.qt_kham, name='qt_kham'),
    path('quy-trinh/<int:pk>/thanh-toan/', views.qt_thanh_toan, name='qt_thanh_toan'),
    path('quy-trinh/<int:pk>/xuat-kho/', views.qt_xuat_kho, name='qt_xuat_kho'),
    path('quy-trinh/<int:pk>/nhan-vacxin/', views.qt_nhan_vacxin, name='qt_nhan_vacxin'),
    path('quy-trinh/<int:pk>/tiem/', views.qt_tiem, name='qt_tiem'),
    path('quy-trinh/<int:pk>/theo-doi/', views.qt_theo_doi, name='qt_theo_doi'),

    # Khu vuc quan tri (custom)
    path('quan-tri/tai-khoan/', views.quan_tri_tai_khoan, name='quan_tri_tai_khoan'),
    path('quan-tri/tai-khoan/<int:pk>/sua/', views.quan_tri_tai_khoan_sua, name='quan_tri_tai_khoan_sua'),
    path('quan-tri/tai-khoan/<int:pk>/khoa/', views.quan_tri_tai_khoan_khoa, name='quan_tri_tai_khoan_khoa'),
    path('quan-tri/vac-xin/', views.quan_tri_vac_xin, name='quan_tri_vac_xin'),
    path('quan-tri/vac-xin/<int:pk>/sua/', views.quan_tri_vac_xin_sua, name='quan_tri_vac_xin_sua'),
    path('quan-tri/vac-xin/<int:pk>/xoa/', views.quan_tri_vac_xin_xoa, name='quan_tri_vac_xin_xoa'),
    path('quan-tri/phac-do/', views.quan_tri_phac_do, name='quan_tri_phac_do'),
    path('quan-tri/phac-do/<int:pk>/sua/', views.quan_tri_phac_do_sua, name='quan_tri_phac_do_sua'),
    path('quan-tri/phac-do/<int:pk>/xoa/', views.quan_tri_phac_do_xoa, name='quan_tri_phac_do_xoa'),
    path('quan-tri/lich-su/', views.quan_tri_lich_su, name='quan_tri_lich_su'),
    path('quan-tri/yeu-cau-mat-khau/', views.quan_tri_yeu_cau_mat_khau, name='quan_tri_yeu_cau_mat_khau'),
    path('quan-tri/yeu-cau-mat-khau/<int:pk>/xu-ly/', views.quan_tri_yeu_cau_xu_ly, name='quan_tri_yeu_cau_xu_ly'),
    path('quan-tri/yeu-cau-mat-khau/<int:pk>/tu-choi/', views.quan_tri_yeu_cau_tu_choi, name='quan_tri_yeu_cau_tu_choi'),

    # Trang lam viec rieng theo vai tro
    path('bac-si/', views.bac_si_dashboard, name='bac_si_dashboard'),
    path('bac-si/lich-su/', views.bac_si_lich_su, name='bac_si_lich_su'),
    path('dieu-duong/', views.dieu_duong_dashboard, name='dieu_duong_dashboard'),
    path('dieu-duong/xu-ly-phan-ung/<int:pk>/', views.dieu_duong_xu_ly_phan_ung, name='dieu_duong_xu_ly_phan_ung'),
    path('thu-kho/', views.thu_kho_dashboard, name='thu_kho_dashboard'),
    path('thu-kho/lich-su/', views.thu_kho_lich_su, name='thu_kho_lich_su'),
    path('thu-kho/xuat/<int:pk>/phieu-pdf/', views.phieu_xuat_kho_pdf, name='phieu_xuat_kho_pdf'),
    path('thu-kho/lich-su-nhap/', views.thu_kho_nhap_lich_su, name='thu_kho_nhap_lich_su'),
    path('thu-kho/nhap-excel/', views.thu_kho_nhap_excel, name='thu_kho_nhap_excel'),
    path('thu-kho/nhap-excel/mau/', views.thu_kho_excel_mau, name='thu_kho_excel_mau'),
    path('thu-kho/bao-cao/', views.thu_kho_bao_cao, name='thu_kho_bao_cao'),
    path('thu-kho/bao-cao/xem-pdf/', views.thu_kho_bao_cao_xem, name='thu_kho_bao_cao_xem'),
    path('thu-kho/bao-cao/pdf/', views.thu_kho_bao_cao_pdf, name='thu_kho_bao_cao_pdf'),
    path('thu-kho/huy/', views.thu_kho_huy, name='thu_kho_huy'),

    # Dang nhap / dang xuat / dang ky rieng (giao dien Bootstrap dong bo site)
    path('dang-nhap/', views.DangNhapView.as_view(), name='dang_nhap'),
    path('dang-xuat/', auth_views.LogoutView.as_view(), name='dang_xuat'),
    path('dang-ky/', views.dang_ky, name='dang_ky'),
    path('quen-mat-khau/', views.quen_mat_khau, name='quen_mat_khau'),
    path('chung-nhan/<int:pk>/', views.chung_nhan_tiem, name='chung_nhan_tiem'),
]
