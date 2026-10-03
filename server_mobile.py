# -*- coding: utf-8 -*-
"""
COLREGS-3D Mobile & Local Network Server
Phục vụ mô phỏng hàng hải cho cả máy tính và điện thoại di động qua WiFi nội bộ.
Sử dụng 100% thư viện chuẩn có sẵn của Python, không phụ thuộc bất kỳ thư viện ngoài nào.
"""

import os
import sys
import socket
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Cấu hình UTF-8 cho console Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

def get_local_ip():
    """Tự động phát hiện địa chỉ IP trong mạng WiFi/LAN nội bộ của máy tính."""
    # Cách 1: Thử kết nối UDP ảo đến địa chỉ công cộng (không gửi dữ liệu thực tế)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            return ip
    except Exception:
        pass

    # Cách 2: Lấy qua danh sách IP nội bộ theo hostname nếu máy tính không có Internet ngoài
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith('127.') and not ip.startswith('169.254.'):
                return ip
    except Exception:
        pass

    return '127.0.0.1'

class MarineRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Tránh cache để trình duyệt điện thoại luôn tải bản mới nhất
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Giảm bớt log rác, chỉ ghi lại nếu có lỗi hoặc trang chính
        if any(code in args[1] for code in ('200', '304')):
            return
        super().log_message(format, *args)

def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(base_dir)
        local_ip = get_local_ip()

        candidate_ports = [8080, 8088, 8081, 8082, 8000, 8888, 9000]
        httpd = None
        active_port = None

        for port in candidate_ports:
            try:
                httpd = HTTPServer(('0.0.0.0', port), MarineRequestHandler)
                active_port = port
                break
            except OSError:
                continue

        if httpd is None:
            try:
                httpd = HTTPServer(('0.0.0.0', 0), MarineRequestHandler)
                active_port = httpd.server_port
            except Exception as e:
                print(f"[LỖI] Không thể tạo máy chủ HTTP: {e}")
                input("\nNhấn phím Enter để đóng...")
                sys.exit(1)

        pc_url = f"http://localhost:{active_port}/simulator.html"
        mobile_url = f"http://{local_ip}:{active_port}/simulator.html"

        print("=" * 72)
        print("      ⚓ MÁY CHỦ MÔ PHỎNG COLREGS-3D ĐANG CHẠY CHO DI ĐỘNG & PC ⚓")
        print("=" * 72)
        print()
        print("  💻 TRÊN MÁY TÍNH CỦA BẠN:")
        print(f"     👉 {pc_url}")
        print()
        print("  📱 TRÊN ĐIỆN THOẠI DI ĐỘNG (iPhone / iPad / Android):")
        print(f"     👉 {mobile_url}")
        print()
        print("  ----------------------------------------------------------------------")
        print("  HƯỚNG DẪN MỞ TRÊN ĐIỆN THOẠI:")
        print("  1. Kết nối điện thoại vào CÙNG MẠNG WIFI với máy tính này.")
        print("  2. Mở trình duyệt web (Safari trên iPhone hoặc Chrome trên Android).")
        print("  3. Nhập chính xác dòng sau vào thanh địa chỉ:")
        print(f"     {mobile_url}")
        print()
        print("  💡 MẸO SỬ DỤNG TRÊN ĐIỆN THOẠI:")
        print("     - Xoay ngang màn hình điện thoại để trải nghiệm buồng lái tốt nhất.")
        print("     - Nhấn vào menu 'Thêm vào MH chính' (Add to Home Screen) trong")
        print("       trình duyệt để tạo icon như một app thực thụ!")
        print("  ----------------------------------------------------------------------")
        print()
        print("  (Giữ cửa sổ này mở trong suốt quá trình học. Nhấn Ctrl + C để dừng)")
        print("=" * 72)
        print()

        # Mở trình duyệt tự động trên máy tính
        try:
            webbrowser.open(pc_url)
        except Exception:
            pass

        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n[INFO] Đã dừng máy chủ mô phỏng theo yêu cầu.")
    except Exception as e:
        print(f"\n[LỖI] Có sự cố xảy ra: {e}")
        import traceback
        traceback.print_exc()
        input("\nNhấn Enter để đóng...")

if __name__ == '__main__':
    main()
