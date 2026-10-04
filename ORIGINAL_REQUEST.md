# Original User Request

## 2026-10-03T13:30:32Z

<USER_REQUEST>
Nâng cấp toàn diện nền tảng mô phỏng hàng hải 3D (COLREGS-3D) trên nền Web/Mobile (Three.js & Capacitor) hoạt động 100% Offline, tích hợp 5 phân hệ chuyên sâu: Kịch bản đa tàu & môi trường phức tạp (TSS, luồng hẹp, sương mù, dạt gió/dòng), Hệ thống còi & chớp sáng chuẩn Part D, Hộp đen VDR Replay & xuất chứng chỉ PDF, Chế độ giảng viên Classroom qua QR/JSON & Bảng xếp hạng, và Trực quan hóa buồng lái WebXR 360°.

Working directory: d:/marine
Integrity mode: development

## Requirements

### R1. Kịch bản hàng hải đa tàu & Môi trường vật lý thực tế (Advanced Scenarios & Environment)
- Mở rộng hệ thống mô phỏng từ đối đầu 1v1 sang tình huống đa tàu (Multi-vessel: 3 đến 5 tàu mục tiêu cùng xuất hiện) với các hướng đi, tốc độ và nghĩa vụ tránh va đan xen phức tạp (như vừa vượt tàu trước mặt vừa nhường đường cho tàu cắt hướng mạn phải).
- Bổ sung môi trường luồng hẹp (Rule 9) và Hệ thống phân luồng giao thông hàng hải (TSS - Rule 10) với hệ thống phao tiêu dẫn luồng chuẩn IALA (Region A & B).
- Bổ sung chế độ thời tiết sương mù dày đặc (3D Fog) và đêm tối không trăng (Rule 19), che khuất tầm nhìn mắt thường và buộc người điều động dựa hoàn toàn vào Radar ARPA cùng tín hiệu âm thanh sương mù.
- Tích hợp mô hình vật lý trôi dạt do dòng chảy (Current Drift) và gió (Wind Leeway) tác động trực tiếp lên hướng di chuyển thực tế (COG) so với hướng mũi tàu (HDG).

### R2. Hệ thống Âm thanh hàng hải & Tín hiệu còi - đèn (Sound & Light Signals - Part D)
- Tích hợp hệ thống âm thanh còi 3D (Spatial Audio qua Web Audio API) theo đúng chuẩn COLREG 72 Part D:
  - Tín hiệu điều động (Rule 34): 1 hồi ngắn (đổi hướng sang phải), 2 hồi ngắn (đổi hướng sang trái), 3 hồi ngắn (đang lùi máy), 5 hồi ngắn dồn dập (nghi ngờ hành động / báo động nguy hiểm).
  - Tín hiệu âm thanh khi tầm nhìn bị hạn chế (Rule 35): phát tự động theo chu kỳ 2 phút (1 hồi dài cho tàu máy đang hành trình, 2 hồi dài liên tiếp cho tàu máy dừng trôi).
- Đồng bộ hiệu ứng đèn chớp trắng đa hướng trên cột buồm tương ứng với từng hồi còi theo Rule 34.

### R3. Hộp đen hàng hải VDR Replay & Xuất báo cáo chứng nhận (VDR & Analytics)
- Hệ thống ghi dữ liệu hành trình (Voyage Data Recorder - VDR): ghi nhận liên tục từng giây các thông số hành trình (vị trí GPS x/y, HDG, COG, tốc độ, góc bẻ lái, khoảng cách CPA và thời gian TCPA đến từng mục tiêu).
- Giao diện VDR Replay: cho phép tua lại (Play/Pause/Scrub timeline) toàn bộ quỹ đạo di chuyển của tàu ta và các tàu bạn trên hải đồ 2D/3D kèm đồ thị biến thiên CPA/TCPA theo thời gian để học viên phân tích sai sót.
- Công cụ xuất chứng chỉ / Báo cáo kết quả đào tạo ra file PDF trực tiếp trên trình duyệt/thiết bị di động (client-side PDF): hiển thị đầy đủ thông tin học viên, tên bài tập, biểu đồ kết quả, cự ly an toàn nhỏ nhất, các lỗi vi phạm và chứng nhận hoàn thành.

### R4. Tính năng Giảng dạy (Classroom / LMS) & Bảng xếp hạng Offline
- Chế độ Giảng viên (Instructor Studio): Giao diện trực quan cho phép giảng viên tự cấu hình tình huống (vị trí tọa độ tàu ta và các tàu mục tiêu, tốc độ, loại tàu, thời tiết, luồng lạch) và trích xuất kịch bản thành Mã QR hoặc chuỗi mã PIN/JSON.
- Học viên quét mã QR hoặc nhập chuỗi kịch bản để vào bài thi ngay lập tức mà không cần kết nối mạng Internet hay máy chủ bên ngoài.
- Hệ thống Bảng xếp hạng (Leaderboard) lưu trữ cục bộ (Local Storage/IndexedDB) theo dõi điểm số bài thi trắc nghiệm (ngân hàng 500 câu) và điểm đánh giá điều động an toàn giữa các học viên trên cùng thiết bị.

### R5. Trải nghiệm Buồng lái Thực tế ảo WebXR (VR Bridge Mode)
- Tích hợp chuẩn WebXR vào Three.js cho phép người học sử dụng kính thực tế ảo (Meta Quest, kính VR di động) hoặc cảm biến con quay hồi chuyển (Gyroscope) của điện thoại để xoay góc nhìn 360° tự do trên buồng lái.
- Người học có thể quan sát trực tiếp các đèn hành trình, dấu hiệu ban ngày và phao tiêu biển xung quanh với tỷ lệ và khoảng cách thị giác chân thực.

## Verification Resources & Mechanisms

- Multi-target Logic Engine Test: Kiểm tra thuật toán vector CPA/TCPA tính toán song song chính xác cho 5 mục tiêu đồng thời trong cùng một vòng lặp render, không gây giật lag (đạt >= 60 FPS trên thiết bị thông thường).
- TSS & Rule 10 Compliance Validator: Kiểm tra tự động phát hiện tàu đi ngược chiều luồng TSS, cắt ngang luồng ở góc không vuông góc, hoặc đi vào vùng phân cách không đúng quy định.
- Fog & Audio Timing Verification: Kiểm tra đồng hồ timer chu kỳ 2 phút phát đúng âm thanh Rule 35, tính toán độ suy giảm âm thanh theo khoảng cách (Distance Attenuation) và đồng bộ ánh sáng đèn chớp.
- VDR Data Integrity & PDF Export Check: Kiểm tra mảng dữ liệu VDR không bị rò rỉ bộ nhớ sau 15 phút mô phỏng; kiểm tra tệp PDF xuất ra định dạng A4 chuẩn, chứa đầy đủ thông số đánh giá và biểu đồ.
- Offline / Mobile Package Verification: Toàn bộ tính năng mới hoạt động trơn tru khi chạy offline không mạng, đồng bộ đầy đủ vào gói đóng gói Android Capacitor (build-apk.yml).

## Acceptance Criteria

### 1. Kịch bản & Quy tắc hàng hải (R1)
- [ ] Mô phỏng đồng thời từ 3 đến 5 tàu mục tiêu chuyển động độc lập, mỗi tàu có cờ hiệu, đèn hành trình và vector radar riêng biệt.
- [ ] Vùng luồng hẹp và TSS hiển thị rõ làn đi, vùng phân cách và hệ thống phao tiêu IALA (phao mạn trái màu đỏ, mạn phải màu xanh lá cây hoặc theo Region B).
- [ ] Chế độ sương mù kích hoạt hiệu ứng che khuất tầm nhìn trong phạm vi bán kính cho phép, buộc người dùng sử dụng Radar ARPA để định vị.
- [ ] Tàu bị trôi dạt theo hướng gió và dòng chảy, hiển thị rõ sự chênh lệch giữa góc mũi tàu (HDG) và hướng thực tế qua đất (COG).

### 2. Âm thanh & Tín hiệu còi - đèn (R2)
- [ ] Các nút còi điều động (1 ngắn, 2 ngắn, 3 ngắn, 5 ngắn) phát đúng tần số và thời lượng âm thanh còi tàu biển tiêu chuẩn.
- [ ] Chế độ sương mù tự động kích hoạt còi theo chu kỳ 2 phút một lần khi người lái bật chế độ hành trình trong tầm nhìn hạn chế.
- [ ] Đèn hiệu cột buồm chớp sáng trắng đồng bộ với thời gian phát còi và quan sát được rõ ràng từ góc nhìn buồng lái và tàu đối diện.

### 3. Hộp đen VDR & Báo cáo PDF (R3)
- [ ] Hộp đen VDR ghi nhận toàn bộ tọa độ và trạng thái điều động với tần suất ít nhất 1 lần/giây.
- [ ] Chế độ Replay cho phép tua tới/lui, tạm dừng và hiển thị trực quan vệt di chuyển của các tàu kèm đồ thị CPA theo thời gian.
- [ ] Nút xuất báo cáo PDF tạo ra chứng chỉ đào tạo định dạng A4 chuyên nghiệp, có thể lưu về máy hoặc chia sẻ ngay trên điện thoại mà không cần internet.

### 4. Giảng viên LMS & Bảng xếp hạng (R4)
- [ ] Giảng viên có thể tùy biến vị trí, hướng đi của tàu mục tiêu trên bản đồ và xuất ra mã QR / JSON ngắn gọn.
- [ ] Ứng dụng hỗ trợ quét hoặc dán mã kịch bản để tải ngay màn chơi mới.
- [ ] Bảng xếp hạng lưu trữ danh sách kết quả thi trắc nghiệm và điểm thực hành điều động, cho phép sắp xếp theo thứ hạng điểm cao.

### 5. WebXR Buồng lái (R5)
- [ ] Giao diện hỗ trợ nút chuyển sang chế độ "VR Buồng lái".
- [ ] Khi bật WebXR trên kính VR hoặc bật chế độ Gyroscope trên điện thoại, góc nhìn buồng lái tự động quay mượt mà theo cử động đầu của người dùng 360 độ.

### 6. Đóng gói & Tương thích
- [ ] Tất cả tài nguyên (âm thanh, thư viện PDF, kịch bản, WebXR) được nhúng gọn trong dự án offline, không phụ thuộc CDN bên ngoài.
- [ ] Ứng dụng tương thích hoàn hảo khi đóng gói APK Android và chạy mượt mà trên trình duyệt di động.
</USER_REQUEST>

## Follow-up — 2026-10-04T06:29:11Z

The server was restarted and the user has explicitly requested: '/teamwork-preview tiếp tục dự án'.
Please revive the orchestrator and continue the project from your current status in d:/marine/.agents/teamwork_preview_orchestrator_1/progress.md. Proceed with M1 review, Milestone M2 (Sound & Light Signals Part D), M3 (VDR & PDF), M4 (Classroom LMS), M5 (WebXR), and M6.

## Follow-up — 2026-10-04T08:23:54Z

USER CHANGE OF SCOPE: Skip Milestone M3 (VDR Black Box & PDF export) entirely. After M2 passes its gate, go directly to M4 (Classroom LMS & offline leaderboard) and then M5 (WebXR cockpit), then M6 final verification. Update PROJECT.md/progress.md and adjust the E2E test expectations so that M3-related tests (VDR/PDF) are excluded rather than counted as failures.

## Follow-up — 2026-10-04T08:29:10Z

USER DIRECTIVE to conserve quota: reduce gate review rounds. For each remaining milestone (M2, M4, M5, M6) use a single lean gate: at most 1 reviewer + 1 forensic auditor (headless runtime check + E2E suite), instead of 5 agents. Allow at most ONE remediation iteration per milestone; only fail on real runtime errors or spec violations, not stylistic/edge-case nitpicks. Avoid spawning redundant explorers. M3 stays skipped.

## Follow-up — 2026-10-04T12:06:31Z

Server has restarted and user says 'tiếp tục dự án'. Resume execution with M3 skipped and lean gate reviews.
