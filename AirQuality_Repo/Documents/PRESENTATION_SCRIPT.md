# KỊCH BẢN THUYẾT TRÌNH ĐỒ ÁN KHO DỮ LIỆU (Mục tiêu 10 Điểm)

## Slide 1: Giới thiệu
*   **Xin chào:** Chào thầy và các bạn. Nhóm em xin trình bày về đề tài "Xây dựng Kho dữ liệu Giám sát Chất lượng Không khí Đô thị".
*   **Lý do chọn đề tài:** Ô nhiễm không khí là vấn đề cấp bách tại Hà Nội. Việc lưu trữ và phân tích dữ liệu lịch sử giúp nhận diện xu hướng và cảnh báo sớm.

## Slide 2: Phân tích Nghiệp vụ (Business Analysis)
*   **Nguồn dữ liệu:** Dữ liệu quan trắc hàng giờ tại Hà Nội (Năm 2023).
*   **Đối tượng nghiên cứu:**
    *   Các chỉ số ô nhiễm: AQI, PM2.5, CO...
    *   Các chỉ số thời tiết: Nhiệt độ, Độ ẩm...
*   **Câu hỏi phân tích:** Chúng em muốn trả lời câu hỏi: "Thời tiết ảnh hưởng thế nào đến độ ô nhiễm?" và "Xu hướng ô nhiễm thay đổi ra sao theo giờ trong ngày?".

## Slide 3: Thiết kế Hệ thống (Architecture & ERD)
*   **Mô hình:** Sử dụng **Star Schema** (Lược đồ sao).
*   **Fact Table:** `FactHourlyMeasurement` - Chứa hàng triệu dòng dữ liệu đo đạc chi tiết.
*   **Dimension Tables:**
    *   `DimLocation`: Quản lý vị trí.
    *   `DimDate` & `DimTime`: Quản lý thời gian, cho phép phân tích sâu (Drill-down) từ Năm xuống Tháng, Ngày và Giờ.

## Slide 4: Quy trình ETL (SSIS)
*   *(Chiếu hình ảnh Data Flow trong Visual Studio)*
*   **Extract:** Đọc dữ liệu từ file CSV thô.
*   **Transform:**
    *   Sử dụng **Data Conversion** để chuẩn hóa kiểu dữ liệu.
    *   Sử dụng **Derived Column** để tách ngày/giờ, tạo khóa ngoại.
    *   Sử dụng **Lookup** để tham chiếu khóa với các bảng Dimension.
*   **Load:** Nạp dữ liệu sạch vào SQL Server.

## Slide 5: Demo OLAP & Truy vấn
*   *(Chiếu kết quả chạy SQL từ file 03_OLAP_EXAMPLES.sql)*
*   Chúng em đã thực hiện các kỹ thuật OLAP:
    *   **Slice:** Cắt dữ liệu để xem riêng ngày 1/1/2023.
    *   **Roll-up:** Tổng hợp AQI trung bình theo từng Tháng (Tháng 1 ô nhiễm hơn Tháng 5...).
    *   **Drill-down:** Đi sâu vào chi tiết từng giờ cao điểm trong ngày.

## Slide 6: Báo cáo Trực quan (Power BI Dashboard)
*   *(Mở file Power BI hoặc chiếu ảnh Dashboard)*
*   **Biểu đồ 1 (Line Chart):** Xu hướng AQI theo thời gian. (Nhận xét: AQI thường cao vào buổi sáng sớm và chiều tối).
*   **Biểu đồ 2 (Scatter Plot/Bar Chart):** Tương quan giữa Độ ẩm và PM2.5. (Nhận xét: Độ ẩm cao thường đi kèm với tích tụ bụi mịn).
*   **KPI Cards:** Hiển thị chỉ số AQI trung bình và cao nhất trong kỳ.

## Slide 7: Kết luận
*   Hệ thống đã hoàn thiện quy trình từ ETL đến Báo cáo.
*   Dữ liệu đã sẵn sàng để hỗ trợ ra quyết định về môi trường.
*   Cảm ơn thầy và các bạn đã lắng nghe.
