// ===== Hieu ung dropdown cho thanh menu phu =====
// - Desktop: hover co do tre nho (hover-intent) de menu khong bi mat ngay khi
//   di chuot qua khe ho.
// - Mobile/touch: bam vao muc cha de mo/dong dropdown.
(function () {
    'use strict';

    function init() {
        var items = document.querySelectorAll('.submenu .has-dropdown');
        var DELAY = 180; // ms giu menu khi roi chuot

        items.forEach(function (item) {
            var timer = null;

            // Hover-intent (desktop)
            item.addEventListener('mouseenter', function () {
                clearTimeout(timer);
                closeOthers(item);
                item.classList.add('open');
            });
            item.addEventListener('mouseleave', function () {
                timer = setTimeout(function () {
                    item.classList.remove('open');
                }, DELAY);
            });

            // Touch / mobile: bam muc cha de toggle
            var link = item.querySelector('a');
            if (link) {
                link.addEventListener('click', function (e) {
                    if (window.matchMedia('(max-width: 768px)').matches) {
                        e.preventDefault();
                        item.classList.toggle('open');
                    }
                });
            }
        });

        // Bam ra ngoai thi dong het
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.submenu .has-dropdown')) {
                closeAll(items);
            }
        });

        initMenuAdmin();
        initFabChat();
    }

    // Hop chat mo tu nut tron noi (FAB)
    function initFabChat() {
        var openChat = document.getElementById('openChat');
        var chatbox = document.getElementById('chatbox');
        if (!openChat || !chatbox) return;
        var closeChat = document.getElementById('closeChat');
        var form = document.getElementById('chatForm');
        var input = document.getElementById('chatText');
        var body = document.getElementById('chatBody');

        var auth = chatbox.dataset.auth === '1';     // khach da dang nhap (chat that)
        var ten = chatbox.dataset.ten || '';
        var urlTin = chatbox.dataset.urlTin;
        var urlGui = chatbox.dataset.urlGui;
        var csrfEl = form.querySelector('[name=csrfmiddlewaretoken]');
        var csrf = csrfEl ? csrfEl.value : '';

        // Cau hoi goi y + tu khoa de khop khi go tu do
        var goiY = [
            { hoi: 'Bảng giá vắc-xin?', dap: 'Bạn xem chi tiết tại mục "Bảng giá". Giá tùy theo từng loại vắc-xin và độ tuổi.', link: '/bang-gia/', nhan: 'Xem bảng giá', tu: ['giá', 'gia', 'bao nhiêu', 'tiền', 'tien', 'phí'] },
            { hoi: 'Cách đặt lịch hẹn?', dap: 'Vào "Đặt lịch hẹn", chọn người tiêm, vắc-xin và ngày giờ mong muốn rồi gửi. Lễ tân sẽ xác nhận giúp bạn.', link: '/dat-lich/', nhan: 'Đặt lịch ngay', tu: ['đặt lịch', 'dat lich', 'lịch hẹn', 'hẹn', 'booking', 'đăng ký'] },
            { hoi: 'Chuẩn bị gì trước khi tiêm?', dap: 'Trước tiêm sẽ có khám sàng lọc. Bạn nên ăn nhẹ, mang theo sổ tiêm và giấy tờ tùy thân. Xem thêm ở "Cẩm nang".', link: '/cam-nang/', nhan: 'Xem cẩm nang', tu: ['chuẩn bị', 'truoc khi', 'trước khi'] },
            { hoi: 'Theo dõi sau tiêm?', dap: 'Ở lại theo dõi 30 phút sau tiêm; tiếp tục theo dõi tại nhà 24–48 giờ. Có dấu hiệu bất thường hãy gọi hotline ngay.', link: '/cam-nang/', nhan: 'Xem cẩm nang', tu: ['sau tiêm', 'theo dõi', 'phản ứng', 'sốt', 'sot', 'phan ung'] },
            { hoi: 'Giờ làm việc?', dap: 'Phòng khám mở cửa 7h30–17h00 các ngày trong tuần.', tu: ['giờ', 'gio lam', 'mở cửa', 'thời gian', 'lam viec', 'mấy giờ'] }
        ];

        function them(text, who) {
            var d = document.createElement('div');
            d.className = 'msg ' + who;
            d.textContent = text;
            body.appendChild(d);
            body.scrollTop = body.scrollHeight;
        }

        function themDap(g) {
            var d = document.createElement('div');
            d.className = 'msg bot';
            var p = document.createElement('div');
            p.textContent = g.dap;
            d.appendChild(p);
            if (g.link) {
                var a = document.createElement('a');
                a.href = g.link;
                a.className = 'chat-link';
                a.innerHTML = '<i class="bi bi-arrow-right-circle"></i> ' + g.nhan;
                d.appendChild(a);
            }
            body.appendChild(d);
            body.scrollTop = body.scrollHeight;
        }

        function dangTraLoi(cb) {                       // hieu ung "dang tra loi..."
            var d = document.createElement('div');
            d.className = 'msg bot text-muted';
            d.textContent = 'Đang trả lời...';
            body.appendChild(d);
            body.scrollTop = body.scrollHeight;
            setTimeout(function () { d.remove(); cb(); }, 600);
        }

        function hienGoiY() {
            var wrap = document.createElement('div');
            wrap.className = 'chat-suggestions';
            goiY.forEach(function (g) {
                var b = document.createElement('button');
                b.type = 'button';
                b.className = 'chat-suggest';
                b.textContent = g.hoi;
                b.addEventListener('click', function () {
                    them(g.hoi, 'user');
                    dangTraLoi(function () { themDap(g); });
                });
                wrap.appendChild(b);
            });
            body.appendChild(wrap);
        }

        function timFAQ(text) {                         // khop tu khoa
            var s = text.toLowerCase();
            for (var i = 0; i < goiY.length; i++) {
                var tu = goiY[i].tu || [];
                for (var j = 0; j < tu.length; j++) {
                    if (s.indexOf(tu[j]) !== -1) return goiY[i];
                }
            }
            return null;
        }

        // ===== Chat that voi nhan vien (khach da dang nhap) =====
        var soTin = 0, pollTimer = null;
        function taiHoiThoai() {
            fetch(urlTin).then(function (r) { return r.json(); }).then(function (d) {
                var tin = d.tin || [];
                for (var i = soTin; i < tin.length; i++) {
                    them(tin[i].noi_dung, tin[i].nv ? 'bot' : 'user');
                }
                soTin = tin.length;
            }).catch(function () {});
        }
        function batPoll() { if (!pollTimer) pollTimer = setInterval(taiHoiThoai, 8000); }
        function dungPoll() { clearInterval(pollTimer); pollTimer = null; }

        // ===== Mo / dong =====
        var khoiTao = false;
        openChat.addEventListener('click', function () {
            chatbox.classList.add('open');
            if (!khoiTao) {
                them('Xin chào' + (ten ? ' ' + ten : '') + '! Phòng khám Tiêm chủng An Tâm '
                    + 'có thể giúp gì cho bạn?', 'bot');
                hienGoiY();
                if (!auth) {
                    them('Bạn có thể chọn câu hỏi gợi ý ở trên, hoặc đăng nhập để chat '
                        + 'trực tiếp với nhân viên.', 'bot');
                }
                khoiTao = true;
            }
            if (auth) { taiHoiThoai(); batPoll(); }
            input.focus();
        });
        closeChat.addEventListener('click', function () {
            chatbox.classList.remove('open');
            dungPoll();
        });

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var t = input.value.trim();
            if (!t) return;
            input.value = '';
            if (auth) {
                var fd = new URLSearchParams();
                fd.append('noi_dung', t);
                fetch(urlGui, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: fd.toString()
                }).then(function () { taiHoiThoai(); }).catch(function () {});
            } else {
                them(t, 'user');
                var g = timFAQ(t);
                dangTraLoi(function () {
                    if (g) { themDap(g); }
                    else { them('Bạn vui lòng đăng nhập để chat trực tiếp với nhân viên, '
                        + 'hoặc gọi hotline 1900 1234. Bạn cũng có thể chọn câu hỏi gợi ý ở trên.', 'bot'); }
                });
            }
        });
    }

    // Menu hamburger (admin & dieu duong): hover de mo (desktop), van bam duoc nhu thuong
    function initMenuAdmin() {
        if (!window.bootstrap) return;
        function laDesktop() { return window.matchMedia('(min-width: 992px)').matches; }

        document.querySelectorAll('.menu-ad').forEach(function (menu) {
            var toggle = menu.querySelector('[data-bs-toggle="dropdown"]');
            if (!toggle) return;
            var dd = window.bootstrap.Dropdown.getOrCreateInstance(toggle);
            var timer = null;

            menu.addEventListener('mouseenter', function () {
                clearTimeout(timer);
                if (laDesktop()) dd.show();
            });
            menu.addEventListener('mouseleave', function () {
                if (laDesktop()) {
                    timer = setTimeout(function () { dd.hide(); }, 180);
                }
            });
        });
    }

    function closeOthers(current) {
        document.querySelectorAll('.submenu .has-dropdown.open').forEach(function (el) {
            if (el !== current) el.classList.remove('open');
        });
    }

    function closeAll(items) {
        items.forEach(function (el) { el.classList.remove('open'); });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
