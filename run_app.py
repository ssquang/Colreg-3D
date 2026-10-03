# -*- coding: utf-8 -*-
"""
COLREGS-3D Marine Bridge Simulator - Desktop Native Launcher
Chạy mô phỏng hàng hải dưới dạng ứng dụng máy tính độc lập (Desktop App).
Tự động nạp qua PySide6 WebEngine (sẵn có trên máy) hoặc pywebview,
khóa hoàn toàn DevTools, F12 và menu ngữ cảnh chuột phải.
"""

import os
import sys
import traceback

def get_base_dir():
    """Lấy thư mục gốc chứa tài nguyên (hoạt động chuẩn cả khi chạy file .py và khi đóng gói qua PyInstaller)."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def run_with_pyside6(html_file):
    """Khởi chạy ứng dụng qua PySide6 QtWebEngine (chuẩn desktop công nghiệp, tăng tốc GPU WebGL)."""
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWebEngineCore import QWebEngineSettings
    from PySide6.QtCore import QUrl, Qt

    app = QApplication(sys.argv)
    app.setApplicationName("COLREGS-3D | Mô Phỏng Buồng Lái & Tránh Va Hàng Hải")

    window = QMainWindow()
    window.setWindowTitle("COLREGS-3D | HỆ THỐNG MÔ PHỎNG BUỒNG LÁI & TRÁNH VA HÀNG HẢI (COLREGs 72)")
    window.resize(1520, 940)
    window.setMinimumSize(1100, 720)

    browser = QWebEngineView(window)
    # Khóa hoàn toàn chuột phải (NoContextMenu) để chống xem mã nguồn
    browser.setContextMenuPolicy(Qt.NoContextMenu)

    # Kích hoạt tăng tốc WebGL & bảo mật
    settings = browser.settings()
    settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
    settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
    settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

    window.setCentralWidget(browser)

    abs_path = os.path.abspath(html_file)
    file_url = QUrl.fromLocalFile(abs_path)
    browser.setUrl(file_url)

    window.show()
    sys.exit(app.exec())

def run_with_webview(html_file):
    """Khởi chạy ứng dụng qua pywebview (dùng Edge Chromium WebView2)."""
    import webview
    base_dir = get_base_dir()

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    three_path = os.path.join(base_dir, 'js', 'three.min.js')
    orbit_path = os.path.join(base_dir, 'js', 'OrbitControls.js')

    if os.path.exists(three_path):
        with open(three_path, 'r', encoding='utf-8') as f:
            three_js = f.read()
        html_content = html_content.replace('<script src="js/three.min.js"></script>', f'<script>\n{three_js}\n</script>')

    if os.path.exists(orbit_path):
        with open(orbit_path, 'r', encoding='utf-8') as f:
            orbit_js = f.read()
        html_content = html_content.replace('<script src="js/OrbitControls.js"></script>', f'<script>\n{orbit_js}\n</script>')

    quiz_path = os.path.join(base_dir, 'js', 'quiz_bank.js')
    if os.path.exists(quiz_path):
        with open(quiz_path, 'r', encoding='utf-8') as f:
            quiz_js = f.read()
        html_content = html_content.replace('<script src="js/quiz_bank.js"></script>', f'<script>\n{quiz_js}\n</script>')

    window = webview.create_window(
        title='COLREGS-3D | HỆ THỐNG MÔ PHỎNG BUỒNG LÁI & TRÁNH VA HÀNG HẢI',
        html=html_content,
        width=1520,
        height=940,
        resizable=True,
        fullscreen=False,
        min_size=(1100, 720),
        background_color='#040c14'
    )
    webview.start(debug=False, private_mode=True)

def main():
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_error.log")
    try:
        base_dir = get_base_dir()
        html_file = os.path.join(base_dir, 'simulator.html')

        if not os.path.exists(html_file):
            print(f"[ERROR] Không tìm thấy file: {html_file}")
            input("Nhấn Enter để thoát...")
            return

        # 1. Thử dùng PySide6 trước (đã có sẵn trong môi trường Python trên máy)
        try:
            import PySide6.QtWebEngineWidgets
            print("[INFO] Đang khởi chạy với động cơ đồ họa PySide6 WebEngine...")
            run_with_pyside6(html_file)
            return
        except ImportError as e:
            print(f"[INFO] PySide6 chưa sẵn sàng ({e}), chuyển sang pywebview...")

        # 2. Thử dùng pywebview
        try:
            import webview
            print("[INFO] Đang khởi chạy với pywebview...")
            run_with_webview(html_file)
            return
        except ImportError:
            pass

        # 3. Tự động cài đặt pywebview nếu cả 2 chưa có
        print("[INFO] Đang chuẩn bị thư viện hiển thị Desktop...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
        run_with_webview(html_file)

    except Exception as e:
        with open(log_file, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        print(f"\n[LỖI KHỞI CHẠY]: {e}")
        traceback.print_exc()
        input("\nNhấn Enter để đóng cửa sổ...")

if __name__ == '__main__':
    main()
