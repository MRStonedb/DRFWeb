# 启动

#### 前端启动(vue.js)
- cd front_end_pc
- live-server

#### 服务启动
- cd /meiduo_mall/apps/
- python  ../../manage.py runserver

#### celery task 启动
- cd meiduo_mall (在celery_tasks 文件夹的同级目录)
- celery -A celery_tasks.main worker -l info
