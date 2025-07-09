Reconocimiento Facial de Empleados

Descripción  
Este programa abre la cámara conectada a la computadora y toma una foto (tambien podria hacerse en un loop para que muestre el frame a frame en vez de solo una foto) y compara las caras detectadas contra una base de datos de empleados. Si encuentra coincidencia (<0.6 de distancia), abre la foto, dibuja un rectángulo alrededor de la cara y muestra el nombre, ademas, registra nombre y hora de ingreso en `registro.csv`.  

Requisitos  
- Python 3.7+  
- CV2
- CMAKE
- datetime
- os
- face_recognition  
- numpy  

DIRECTORIOS:
en Empleados/ se colocan todas las fotos de los empleados, cada foto debe tener como nombre el nombre completo del empleado.
registro.csv se puede crear previamente aunque de igual manera se crea automaticamente con el primer registro. 
