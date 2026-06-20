// Phieu sang loc - hien/an cac o tuy theo lua chon:
//  - tick "Dang su dung thuoc" -> hien o thuoc
//  - ket luan "Hoan tiem"       -> hien o ly do hoan
//  - ket luan "Chong chi dinh"  -> hien dropdown ly do chong
//      + chon "Khac"            -> hien o nhap ly do khac
(function () {
    'use strict';
    function toggle(el, hien) { if (el) el.style.display = hien ? '' : 'none'; }

    function init() {
        var chk = document.getElementById('chk_thuoc');
        var oThuoc = document.getElementById('o_thuoc');
        if (chk) {
            var f1 = function () { toggle(oThuoc, chk.checked); };
            chk.addEventListener('change', f1); f1();
        }

        var kl = document.getElementById('sl_ket_luan');
        var oHoan = document.getElementById('o_ly_do_hoan');
        var oChong = document.getElementById('o_chong');
        var slChong = document.getElementById('sl_ly_do_chong');
        var oChongKhac = document.getElementById('o_chong_khac');

        function capNhatChong() {
            toggle(oChongKhac, slChong && slChong.value === 'khac');
        }
        if (slChong) { slChong.addEventListener('change', capNhatChong); }

        if (kl) {
            var f2 = function () {
                toggle(oHoan, kl.value === 'hoan');
                toggle(oChong, kl.value === 'chong');
                capNhatChong();
            };
            kl.addEventListener('change', f2); f2();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
