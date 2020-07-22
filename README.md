# metroBus
Aplicaion para saber la ubicaion por unidad y alcaldia tiene archivos de configuracion de docker. tiene contenedores python y postgres

se tienen que agrega un cron para que se pueda importar la informacion del servidor algo como esto

---5 * * * * docker exec dockerimages_web_1 python getInformation.py---
