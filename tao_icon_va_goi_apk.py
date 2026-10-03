# -*- coding: utf-8 -*-
"""
COLREGS-3D Mobile App & APK Packager
Tự động tạo bộ icon ứng dụng Android (192x192, 512x512)
và đóng gói toàn bộ mã nguồn thành tệp ZIP sẵn sàng tạo file .APK.
"""

import os
import sys
import zipfile
import math
import struct
import zlib

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def make_fallback_png(width, height):
    """Tạo tệp PNG hợp lệ 100% bằng thư viện chuẩn zlib/struct của Python mà không cần Pillow."""
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = zlib.crc32(c) & 0xffffffff
        return struct.pack('>I', len(data)) + c + struct.pack('>I', crc)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    raw_rows = []
    cx, cy = width / 2.0, height / 2.0
    r_outer = width * 0.42
    r_inner = width * 0.28
    r_hub = width * 0.08

    for y in range(height):
        row = bytearray(b'\x00')
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = math.hypot(dx, dy)
            # Viền bánh lái cyan
            if abs(dist - r_outer) < width * 0.035:
                row.extend([0, 229, 255, 255])
            elif abs(dist - r_inner) < width * 0.025:
                row.extend([0, 229, 255, 220])
            elif dist < r_hub:
                row.extend([0, 229, 255, 255])
            elif width * 0.05 <= x <= width * 0.95 and width * 0.05 <= y <= width * 0.95:
                # Nền xanh biển đậm
                row.extend([4, 16, 26, 255])
            else:
                row.extend([2, 8, 14, 255])
        raw_rows.append(bytes(row))

    idat = chunk(b'IDAT', zlib.compress(b''.join(raw_rows)))
    iend = chunk(b'IEND', b'')
    return header + ihdr + idat + iend

def generate_icons(base_dir):
    """Vẽ icon ứng dụng Android chuẩn hàng hải sắc nét (192x192 và 512x512)."""
    icons_dir = os.path.join(base_dir, 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    has_pillow = False
    try:
        from PIL import Image, ImageDraw, ImageFont
        has_pillow = True
    except Exception:
        has_pillow = False

    for size in [192, 512]:
        out_path = os.path.join(icons_dir, f'icon-{size}.png')
        if has_pillow:
            try:
                img = Image.new('RGBA', (size, size), (4, 16, 26, 255))
                draw = ImageDraw.Draw(img)

                # Vẽ viền bo tròn cyan phát sáng
                margin = int(size * 0.04)
                corner_r = int(size * 0.22)
                draw.rounded_rectangle(
                    [margin, margin, size - margin, size - margin],
                    radius=corner_r,
                    fill=(6, 22, 36, 255),
                    outline=(0, 229, 255, 255),
                    width=max(2, int(size * 0.02))
                )

                # Tâm của icon
                cx, cy = size // 2, int(size * 0.46)
                r = int(size * 0.28)

                # Vẽ vành bánh lái tàu (Ship Steering Helm)
                draw.ellipse(
                    [cx - r, cy - r, cx + r, cy + r],
                    outline=(0, 229, 255, 255),
                    width=max(3, int(size * 0.035))
                )

                inner_r = int(r * 0.6)
                draw.ellipse(
                    [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
                    outline=(0, 229, 255, 200),
                    width=max(2, int(size * 0.02))
                )

                # Các nan hoa bánh lái (8 spokes with handles)
                spoke_r = int(r * 1.25)
                for i in range(8):
                    angle = i * (math.pi / 4)
                    x1 = cx + math.cos(angle) * (inner_r * 0.5)
                    y1 = cy + math.sin(angle) * (inner_r * 0.5)
                    x2 = cx + math.cos(angle) * spoke_r
                    y2 = cy + math.sin(angle) * spoke_r
                    draw.line([x1, y1, x2, y2], fill=(0, 229, 255, 255), width=max(2, int(size * 0.025)))

                # Vẽ trục giữa bánh lái & mỏ neo
                hub_r = int(size * 0.065)
                draw.ellipse(
                    [cx - hub_r, cy - hub_r, cx + hub_r, cy + hub_r],
                    fill=(0, 229, 255, 255),
                    outline=(255, 255, 255, 255),
                    width=max(1, int(size * 0.01))
                )

                # Vẽ dòng chữ "COLREGS 3D"
                text_y = int(size * 0.78)
                draw.text(
                    (size // 2, text_y),
                    "COLREGS 3D",
                    fill=(255, 255, 255, 255),
                    anchor="mm"
                )

                img.save(out_path, 'PNG')
                print(f"[OK] Đã tạo icon (Pillow): {out_path}")
                continue
            except Exception as e:
                print(f"[WARN] Lỗi khi vẽ bằng Pillow ({e}), chuyển sang fallback chuẩn zlib...")

        # Fallback tạo PNG không cần Pillow
        with open(out_path, 'wb') as f:
            f.write(make_fallback_png(size, size))
        print(f"[OK] Đã tạo icon chuẩn: {out_path}")

def create_mobile_zip(base_dir):
    """Đóng gói toàn bộ tài nguyên web thành file ZIP sạch sẽ để upload lên Cloud APK Builder."""
    zip_path = os.path.join(base_dir, 'COLREGS_3D_Mobile_Package.zip')
    files_to_pack = [
        'simulator.html',
        'manifest.json',
        'sw.js',
        'colreg-72-viet-ver.pdf',
        'colreg-72-eng-ver.pdf',
        os.path.join('js', 'three.min.js'),
        os.path.join('js', 'OrbitControls.js'),
        os.path.join('js', 'quiz_bank.js'),
        os.path.join('js', 'colreg_text.js'),
        os.path.join('icons', 'icon-192.png'),
        os.path.join('icons', 'icon-512.png'),
        os.path.join('icons', 'icon.svg'),
    ]

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Tự động nén cả index.html (để AppsGeyser / WebIntoApp nhận diện trang chủ ngay lập tức)
        sim_path = os.path.join(base_dir, 'simulator.html')
        if os.path.exists(sim_path):
            zf.write(sim_path, 'index.html')
            print("[ZIP] Đã nén: index.html (từ simulator.html)")

        for rel_path in files_to_pack:
            full_path = os.path.join(base_dir, rel_path)
            if os.path.exists(full_path):
                zf.write(full_path, rel_path)
                print(f"[ZIP] Đã nén: {rel_path}")
            else:
                print(f"[BỎ QUA] Tệp chưa có: {rel_path}")

    print(f"\n[THÀNH CÔNG] Đã tạo gói đóng gói: {zip_path}")
    print(f"Kích thước gói: {os.path.getsize(zip_path) / 1024:.1f} KB")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("=" * 68)
    print("   ĐANG TẠO ICON VÀ GÓI TÀI NGUYÊN ĐÓNG GÓI APK CHO ANDROID")
    print("=" * 68)
    generate_icons(base_dir)
    create_mobile_zip(base_dir)
    print("=" * 68)

if __name__ == '__main__':
    main()
