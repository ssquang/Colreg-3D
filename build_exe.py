# -*- coding: utf-8 -*-
"""
COLREGS-3D Build Script: Tự động đóng gói thành file .exe độc lập
Sử dụng PyInstaller đóng gói run_app.py cùng simulator.html và thư mục js/
"""

import os
import sys
import subprocess
import shutil

def run_command(cmd, description):
    print(f"\n[TIẾN TRÌNH] {description}...")
    print(f"Lệnh: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"[LỖI] Bước '{description}' thất bại với mã lỗi {result.returncode}")
        return False
    return True

def main():
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(workspace_dir)
    print("=" * 70)
    print("  HỆ THỐNG ĐÓNG GÓI PHẦN MỀM COLREGS-3D THÀNH FILE .EXE ĐỘC LẬP")
    print("=" * 70)

    # 1. Kiểm tra môi trường đồ họa & đóng gói
    print("\n1. Kiểm tra các thư viện đóng gói...")
    
    # Kiểm tra động cơ hiển thị
    has_engine = False
    try:
        import PySide6.QtWebEngineWidgets
        print("  - Động cơ đồ họa: PySide6 QtWebEngine (Đã có sẵn)")
        has_engine = True
    except ImportError:
        pass

    if not has_engine:
        try:
            import webview
            print("  - Động cơ đồ họa: pywebview (Đã có sẵn)")
            has_engine = True
        except ImportError:
            print("  - Đang cài đặt thư viện đồ họa pywebview...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
                has_engine = True
            except Exception as e:
                print(f"  [CẢNH BÁO] Không thể cài pywebview: {e}")

    # Kiểm tra PyInstaller
    try:
        import PyInstaller
        print("  - Bộ đóng gói PyInstaller: Đã có sẵn")
    except ImportError:
        print("  - Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Xóa các bản build cũ nếu có
    build_dir = os.path.join(workspace_dir, "build")
    dist_dir = os.path.join(workspace_dir, "dist")
    spec_file = os.path.join(workspace_dir, "COLREGS_3D_Simulator.spec")

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir, ignore_errors=True)
    if os.path.exists(spec_file):
        os.remove(spec_file)

    # 3. Chạy lệnh PyInstaller
    # Lưu ý trên Windows, tham số --add-data dùng dấu chấm phẩy ';'
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--noconsole",
        "--name=COLREGS_3D_Simulator",
        "--add-data=simulator.html;.",
        "--add-data=js;js",
        "run_app.py"
    ]

    success = run_command(cmd, "Đóng gói mã nguồn và tài nguyên 3D vào file .exe")
    if not success:
        print("\n[THẤT BẠI] Quá trình đóng gói gặp sự cố. Vui lòng kiểm tra lại log ở trên.")
        input("Nhấn Enter để tiếp tục...")
        sys.exit(1)

    # 4. Kiểm tra file .exe kết quả
    exe_path = os.path.join(dist_dir, "COLREGS_3D_Simulator.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n" + "=" * 70)
        print("  🎉 ĐÓNG GÓI THÀNH CÔNG RỰC RỠ!")
        print("=" * 70)
        print(f"  Vị trí file chạy: {exe_path}")
        print(f"  Dung lượng file : {size_mb:.2f} MB")
        print("\n  👉 Bạn chỉ cần copy file 'COLREGS_3D_Simulator.exe' này và gửi cho")
        print("     người khác. Người nhận chỉ cần nhấp đúp là chạy ngay lập tức,")
        print("     máy tính không cần cài Python và không thể xem hay sửa mã nguồn.")
        print("=" * 70)
    else:
        print(f"\n[LƯU Ý] Không tìm thấy file tại {exe_path}. Hãy kiểm tra thư mục dist.")

if __name__ == '__main__':
    main()
