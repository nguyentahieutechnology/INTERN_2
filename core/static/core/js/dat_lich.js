// Form dat lich:
//  1) An/hien khoi "Benh vien chi dinh" theo radio "Hinh thuc chi dinh".
//  2) Loc dropdown "Goi/Phac do" theo vac-xin da chon.
(function () {
    'use strict';

    function initChiDinh() {
        var khoi = document.getElementById('khoi-chi-dinh');
        if (!khoi) return;
        var radios = document.querySelectorAll('input[name="loai_chi_dinh"]');

        function capNhat() {
            var chon = document.querySelector('input[name="loai_chi_dinh"]:checked');
            khoi.style.display = (chon && chon.value === 'benh_vien') ? '' : 'none';
        }
        radios.forEach(function (r) { r.addEventListener('change', capNhat); });
        capNhat();
    }

    function initVacXin() {
        var vx = document.getElementById('id_vac_xin');
        if (!vx) return;
        var pd = document.getElementById('id_phac_do');
        var mapEl = document.getElementById('phacDoVacXin');
        var tonEl = document.getElementById('vacXinTon');
        var canhBao = document.getElementById('khoCanhBao');
        var canhBaoText = document.getElementById('khoCanhBaoText');

        var map = mapEl ? JSON.parse(mapEl.textContent) : {};       // {phac_do_id: [vac_xin_id,...]}
        var ton = tonEl ? JSON.parse(tonEl.textContent) : null;     // {vac_xin_id: so_ton}
        var allOptions = pd ? Array.prototype.slice.call(pd.options) : [];

        // 1) Danh dau vac-xin het hang trong kho: boi xam + them "- Het hang"
        if (ton) {
            Array.prototype.forEach.call(vx.options, function (opt) {
                if (opt.value === '') return;
                var con = parseInt(ton[opt.value] || 0, 10);
                opt.dataset.ton = con;
                if (con <= 0 && opt.textContent.indexOf('Hết hàng') === -1) {
                    opt.textContent += ' — Hết hàng';
                    opt.style.color = '#aaa';
                }
            });
        }

        // 2) Loc dropdown phac do theo vac-xin dang chon
        function locPhacDo() {
            if (!pd || !mapEl) return;
            var sel = parseInt(vx.value, 10);
            var dangChon = pd.value;
            pd.innerHTML = '';
            allOptions.forEach(function (opt) {
                var hopLe = opt.value === '' ||
                    (map[opt.value] || []).indexOf(sel) !== -1;
                if (hopLe) pd.appendChild(opt.cloneNode(true));
            });
            pd.value = dangChon;
        }

        vx.addEventListener('change', function () {
            var opt = vx.options[vx.selectedIndex];
            // Chon phai vac-xin het hang -> bao + khong cho chon
            if (ton && opt && opt.value !== '' && parseInt(opt.dataset.ton, 10) <= 0) {
                if (canhBao && canhBaoText) {
                    canhBaoText.textContent = 'Vắc-xin "' +
                        opt.textContent.replace(' — Hết hàng', '') +
                        '" đã hết trong kho. Vui lòng chọn loại khác.';
                    canhBao.classList.remove('d-none');
                }
                vx.value = '';                         // huy lua chon
            } else if (canhBao) {
                canhBao.classList.add('d-none');
            }
            locPhacDo();
        });

        locPhacDo();
    }

    function init() { initChiDinh(); initVacXin(); }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
