traitamgiamso2.dangkythamgap.hw.io.vn

Trại tạm giam số 2: đăng ký thăm gặp thân nhân

I. Backup (xuất file .sql)
```bash
docker exec -t flask_db pg_dump -U myuser visit_db > backup_v1.sql
```

II. Restore
```bash
cat backup_v1.sql | docker exec -i flask_db psql -U myuser -d visit_db
```

III. Flask Cli
```bash
docker exec -it flask_app flask create-admin
```