# Sử dụng Python image nhẹ (slim) để giảm dung lượng image
FROM python:3.13-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Ngăn Python tạo ra các file .pyc và cho phép log hiển thị ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt các thư viện hệ thống cần thiết (nếu có thư viện đặc biệt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Pip requirements / Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy toàn bộ mã nguồn vào container
COPY . .
