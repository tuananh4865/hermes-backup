---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 Next.js Authentication (extracted)
  - 🔗 JWT vs Database Sessions (extracted)
  - 🔗 NextAuth.js Providers (extracted)
  - 🔗 UAT Process (extracted)
relationship_count: 4
---

# Bài viết kiến thức: Triển khai xác thực NextAuth.js

## Metadata
```yaml
title: "Triển khai Xác thực NextAuth.js cho Ứng dụng Next.js"
date: 2026-04-10
tags: ["Next.js", "Authentication", "NextAuth.js", "UAT", "Security"]
sources: ["Morning Ritual transcript"]
```

---

## Tổng quan (Executive Summary)
Bài viết này trình bày quy trình triển khai hệ thống xác thực cho ứng dụng Next.js sử dụng thư viện **NextAuth.js** với nhà cung cấp (provider) dựa trên **Credentials**. Mục tiêu chính là giải quyết sự cố nghiêm trọng khiến 54 nhiệm vụ kiểm thử (UAT) bị lỗi do thiếu cơ chế xác thực người dùng. Hiện tại, hệ thống đang sử dụng phiên làm việc dựa trên **JWT** (JSON Web Token) thay vì lưu trữ trong cơ sở dữ liệu, đây là giải pháp tạm thời cho đến khi cấu hình lưu trữ dữ liệu bền vững (Turso/Supabase) được hoàn tất.

## Các khái niệm và định nghĩa chính
*   **NextAuth.js**: Thư viện tiêu chuẩn ngành (de-facto standard) giúp tích hợp tính năng xác thực vào các ứng dụng Next.js một cách đơn giản và an toàn.
*   **Credentials Provider**: Một loại nhà cung cấp xác thực của NextAuth.js cho phép người dùng đăng nhập bằng cách nhập tên đăng nhập và mật khẩu trực tiếp trên giao diện web, tương tự như các trang đăng nhập truyền thống.
*   **JWT Sessions (JSON Web Token)**: Cơ chế lưu trữ trạng thái đăng nhập bằng cách mã hóa thông tin người dùng vào một token và gửi nó về trình duyệt của khách hàng. Đây là giải pháp hiện tại để duy trì phiên đăng nhập mà không cần cơ sở dữ liệu trung tâm.
*   **UAT (User Acceptance Testing)**: Giai đoạn kiểm thử chấp nhận người dùng, nơi các tính năng được xác minh để đảm bảo chúng đáp ứng yêu cầu nghiệp vụ trước khi đưa vào sử dụng thực tế.

## Phân tích chi tiết
Dựa trên các thông tin từ bản ghi nhớ buổi họp sáng, quá trình triển khai xác thực đã giải quyết được một nút thắt cổ chai quan trọng trong dự án:

1.  **Triển khai giao diện và bảo vệ route**: Hệ thống đã thành công trong việc xây dựng các trang đăng nhập (login) và đăng ký (register) cũng như bảo vệ các route cần xác thực bằng cách tích hợp **NextAuth.js Credentials provider**. Điều này đảm bảo rằng chỉ những người dùng đã xác thực mới có thể truy cập vào các chức năng cụ thể của ứng dụng.
2.  **Giải quyết sự cố UAT**: Việc triển khai này đã loại bỏ nguyên nhân gây lỗi cho **54 nhiệm vụ kiểm thử UAT** trước đó. Những nhiệm vụ này từng bị thất bại do hệ thống không có cơ chế xác thực người dùng, dẫn đến việc các tính năng bị khóa hoặc trả về lỗi.
3.  **Hạn chế kỹ thuật hiện tại**: Mặc dù hệ thống đã hoạt động được, nhưng cơ chế phiên (session) đang chạy dựa trên **JWT** lưu trữ ở trình duyệt khách hàng. Đây được xác định là một giải pháp **tạm thời** (temporary solution). Để đảm bảo tính ổn định lâu dài và khả năng mở rộng, việc cấu hình lưu trữ phiên trên cơ sở dữ liệu (như Turso hoặc Supabase) vẫn đang trong quá trình thực hiện và chưa được hoàn tất.

## Các thông tin có thể áp dụng ngay (Actionable Insights)
*   **Ưu tiên hoàn thiện lưu trữ**: Ngay lập tức lên kế hoạch và bắt đầu cấu hình cơ sở dữ liệu (Turso hoặc Supabase) để chuyển đổi từ mô hình lưu trữ JWT trên client sang mô hình lưu trữ phiên (session storage) trên server/database. Điều này sẽ giúp hệ thống quản lý người dùng an toàn hơn và có thể mở rộng quy mô.
*   **Kiểm tra lại các route**: Đảm bảo rằng tất cả các route quan trọng trong ứng dụng đã được bảo vệ đúng cách sau khi tích hợp NextAuth.js để tránh các lỗ hổng bảo mật tiềm ẩn trong quá trình phát triển tiếp theo.

## Các chủ đề liên quan
*   [[Next.js Authentication]] - Tổng quan về xác thực trong Next.js.
*   [[JWT vs Database Sessions]] - So sánh giữa lưu trữ phiên trên client và server.
*   [[NextAuth.js Providers]] - Các nhà cung cấp xác thực khác nhau của NextAuth.js.
*   [[UAT Process]] - Quy trình kiểm thử chấp nhận người dùng.