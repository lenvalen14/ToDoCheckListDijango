# To-Do Checklist App (Django)

Đây là một ứng dụng quản lý công việc cá nhân (To-Do Checklist) được xây dựng bằng **Django**.  
Mục tiêu của project là rèn luyện kỹ năng backend với Django Framework, và hiểu cách xây dựng một ứng dụng CRUD đơn giản.

## Công nghệ sử dụng

- Python 3.10+
- Django 4.x
- MySQL
- HTML/CSS, Django Template

## Tính năng chính

- [x] Tạo epic
- [x] Tạo task, sub-task mới
- [x] Đánh dấu task, sub-task đã hoàn thành
- [x] Xóa task, sub-task

## Cài đặt & chạy project

### 1. Clone project
```bash
git clone https://github.com/ten-nguoi-dung/to-do-checklist.git
cd to-do-checklist
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Trên Mac/Linux
venv\Scripts\activate          # Trên Windows
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Chạy migration
```bash
python manage.py migrate
```

### 5. Tạo tài khoản admin
```bash
python manage.py createsuperuser
```

### 6. Chạy server
```bash
python manage.py runserver
```
Truy cập http://127.0.0.1:8000/

## Cấu trúc thư mục
<pre lang="markdown">
ToDoCheckList/
├── .venv/                    # Virtual environment
├── templates/                # Thư mục chứa HTML template
├── todo/                     # App chính
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── enum.py
│   ├── forms.py
│   ├── models.py             # Khai báo model Task
│   ├── tests.py
│   ├── urls.py               # Định nghĩa route cho app
│   └── views.py              # Logic xử lý request
├── ToDoCheckList/            # Cấu hình project Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env                      # Biến môi trường
├── .gitignore
├── manage.py
</pre>
