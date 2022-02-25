# AWI4
Haciendo uso de [Web.py](https://webpy.org/) y [Pyrebase](https://github.com/nhorvath/Pyrebase4) para el backend, Html y [Bootstrap](https://getbootstrap.com/) para el frontend

---
Instalar las librerias necesarias

```
pip install web.py
```
```
pip install pyrebase
```
---
## Pagina de Login
![login](https://telegra.ph/file/1f38ddb8ca31724665fb4.png)

```
user = auth.sign_in_with_email_and_password(email, password)
```

Establece una conexion a [firebase](https://console.firebase.google.com/) y valida los datos del usuario

---
## Pagina de Sign Up
![signup](https://telegra.ph/file/4ecf03fa891f641d2b262.png)

```
user = auth.create_user_with_email_and_password(email, password)
```

Establece una conexion a [firebase](https://console.firebase.google.com/) y registra los datos del nuevo usuario, ademas que haciendo uso del Realtime Database, guarda los datos del usuario para hacer su uso posterior.

```
datos = {'nombre': nombre , 'telefono': telefono, 'email':email} 
resultados = db.child("usuarios").child(user['localId']).set(datos)
```

![rdb](https://telegra.ph/file/d53b75a50fb644a0f6dbb.png)

--- 
## Recuperar Contraseña
![recuperarcontra](https://telegra.ph/file/067f87ac89736ef91b151.png)

```
auth.send_password_reset_email(email)
```
Envia el correo a [firebase](https://console.firebase.google.com/), verifica su existencia y mediante una platilla envia el link para cambiar la contraseña

--- 
## Errores
![error](https://telegra.ph/file/c7f056946737041387871.png)

1. Enviamos el error a la plantilla html
```
return render_plain.registrar(message)
```
2. Recibimos la plantilla en el html
```
$def with (message)
```
3. Mostramos el error
```
$if message is not None:
    <div class="alert alert-danger" role="alert">
        <strong>$message</strong>
    </div>
```
---
## Bienvenida
![bienvenida](https://telegra.ph/file/7b78d72a772c353134105.png)

1. Crearemos una cookie para validar el usuario
2. Validaremos su informacion con la base de datos
3. Mostraremos su nombre

---
## Usuarios
![usuarios](https://telegra.ph/file/5aac3db536f1cf996eec1.png)

1. Realizamos una conexion a la base de datos
2. Enviamos la variable con los usuarios al html
3. Ordenamos los usuarios en una tabla
```
$for user in users:
    <tr>
        <td>$user.val().get('nombre')</td>
        <td>$user.val().get('email')</td>
        <td>$user.val().get('telefono')</td>
        <td><a href="/actualizar_usuario/$user.key()">Actualizar</a></td>
    </tr>
```
---
## Actualizar Usuario
![actualizar](https://telegra.ph/file/4cfe8469b65b34175efbf.png)

1. Mediante un formulario obtenemos los datos
2. Una vez modificados, se guardan en la base de datos
3. Nos regresa a la parte de usuarios, con los cambios aplicados
 ![cambios](https://telegra.ph/file/4aa270c86b2d2de6838c8.png)

---

### Mas datos en el archivo [app.py](https://github.com/luisgar289/AWI4/blob/main/app.py)




