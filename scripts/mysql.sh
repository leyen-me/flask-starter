docker run -idt -p 3306:3306 --privileged=true \
-e TZ=Asia/Shanghai \
-e MYSQL_DATABASE=flask \
-e MYSQL_ROOT_PASSWORD=pdBGKGjRyX3Jb2Hn \
--name flask_mysql mysql:8.0.20