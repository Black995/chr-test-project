### Pasos a seguir para ejecutar el proyecto

- Una vez clonado el repositorio y estando en la carpeta raíz, ejecutar **pip install -r requirements.txt** , con el fin de poder instalar todas las librerías necesarias para el proyecto.
- Configurar las credenciales de acceso de PostgreSQL. Para ello hay que acceder al archivo /chr_project/chr_project/settings.py y colocar las credenciales de acceso requeridas ("NAME", "USER" Y "PASSWORD")

![image](https://user-images.githubusercontent.com/54086005/219528302-40d5daf6-7226-49ef-9233-dae47bf00847.png)

- Estando en la ruta /chr_project ejecutar los comandos:
		python manage.py makemigrations
		python manage.py migrate
para poder migrar los modelos de Django a la base de datos 
- Finalmente, ejecutar el siguiente comando para correr el servidor
		python manage.py runserver

#### Pasos opcionales para acceder al administrador de Django
- Para poder acceder a la vista administrador de django y poder gestionar los registros de los modelos, debe crear un súper usuario con el siguiente comando:
		python manage.py createsuperuser
después de este paso podrá acceder a la ruta http://localhost:8000/admin/ , colocando las credenciales registradas en el usuario creado

### Rutas disponibles para el proyecto

- http://localhost:8000/api/tasks/task1/bikes_santiago/ -> esta URL es de prueba para probar la conexión con la API Bike Santiago y el uso de la librería urllib3.
- http://localhost:8000/api/tasks/task1/bikes_santiago_create/ -> esta URL es para obtener la información de la API Bike Santiago y guardar los datos en la base de datos. Con el fin de evitar que se repita la información, esta se registra si no se encuentra algún dato con el mismo ID o UID en la BD.
- http://localhost:8000/api/tasks/task2/seia_sea/ -> esta URL es para correr el script que obtiene la información del portal de Servicio de Evaluación Ambiental, guarda dicha información en la base de datos para finalmente desplegar la lista de información registrada. Tome en cuenta que puede ser una solicitud que demore un tiempo considerable, dependiendo de su conexión de internet. El script fue creado mediante la librería **Selenium**
