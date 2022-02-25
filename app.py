#importa las librerias para el proyecto
import web
import firebase_config as token
import pyrebase
import json

#url y funcion de la aplicacion web
urls = (
    '/', 'bienvenida',
    '/login', 'login',
    '/signup', 'signup',
    '/bienvenida','bienvenida',
    '/logout', 'logout',
    '/recuperar', 'recuperar',
    '/usuarios', 'usuarios',
    '/actualizar_usuario/(.*)', 'actualizar_usuario',
)
app = web.application(urls, globals())
render = web.template.render('templates/', base = 'layout') #platillas html con una base
render_plain = web.template.render('templates/') #platillas html sin una base
firebase = pyrebase.initialize_app(token.firebaseConfig) #conexión a firebase
auth = firebase.auth() #verifica la conexion a firebase
db = firebase.database() #conexión a la base de datos

class index: #pagina raíz 
    def GET(self):
        return 'index'

class login: #pagina login
    def GET(self):
        message = None
        return render_plain.login(message) #muestra la pagina login.html

    def POST(self):
        try:
            #obtiene los datos del formulario
            message = None
            formulario = web.input() 
            email = formulario.email 
            password= formulario.password
            #autentica los datos con firebase
            user = auth.sign_in_with_email_and_password(email, password)
            #obtiene los datos del usuario
            informacion = auth.get_account_info(user['idToken']) 
            localId = user['localId'] #obtiene el localId del usuario
            #genera una cookie
            web.setcookie('localid', localId)
            return web.seeother('/bienvenida') #muestra la pagina de bienvenida.html, pero no redirecciona
        except Exception as error: #recopila y muestra los datos de algun error
            formato = json.loads(error.args[1])
            error = formato['error']
            message = error['message']
            print("Error login.POST: {}".format(message)) #imprime en la terminal el error
            return render_plain.login(message) #muestra la pagina login.html con el error

class signup: #pagin sign up
    def GET(self):
        message = None
        return render_plain.registrar(message)

    def POST(self):
        try:
            #obtiene los datos del formulario
            message = None
            formulario = web.input()
            email = formulario.email
            password= formulario.password
            nombre = formulario.nombre
            telefono = formulario.telefono
            user = auth.create_user_with_email_and_password(email, password) #crea un nuevo usuario en firebase
            datos = {'nombre': nombre , 'telefono': telefono , 'email':email} #crea un diccionario con los datos del usuario
            resultados = db.child("usuarios").child(user['localId']).set(datos) #guarda los datos en la base de datos
            return web.seeother('/login') #redirecciona a la pagina del login
        except Exception as error: #recopila los datos del error
            formato = json.loads(error.args[1])
            error = formato['error']
            message = error['message']
            print("Error signup.POST: {}".format(message)) #imprime en la terminal el error
            return render_plain.registrar(message) #muestra la pagina signup.html con el error

class bienvenida: 
    def GET(self):
        cookie = web.cookies().get('localid') #obtiene la cookie localid
        all_users = db.child("usuarios").get() #obtiene todos los usuarios de la base de datos
        for user in all_users.each(): #recorre todos los usuarios
            usuario = user.key() #obtiene la llave del usuario
            if usuario == cookie: #compara la llave con la cookie, si son iguales muestra la pagina bienvenida.html
                usuario = user.val() #obtiene los datos del usuario
                nombre = usuario['nombre'] #obtiene el nombre del usuario
                return render.bienvenida(nombre) #muestra la pagina bienvenida.html con el nombre del usuario
            else: #si no son iguales, redirecciona a la pagina de login
                return web.seeother('/login') #redireccion la pagina login.html
class logout:
    def GET(self):
        web.setcookie('localid', "None") #establece la cookie en None
        return web.seeother('/login') #regresa a la pagina de login

class recuperar:
    def GET(self):
        message = None
        return render_plain.recuperar(message)
    def POST(self):
        try:
            #obtiene los datos del formulario
            message = None
            formulario = web.input()
            email = formulario.email
            auth.send_password_reset_email(email) #envia un correo de recuperacion de contraseña
            return web.seeother('/login') #redirecciona a la pagina de login
        except Exception as error:
            formato = json.loads(error.args[1])
            error = formato['error']
            message = error['message']
            print("Error recuperar.POST: {}".format(message))
            return render_plain.recuperar(message)

class usuarios:
    def GET(self):
        try:
            users = db.child("usuarios").get() #obtiene todos los usuarios de la base de datos
            return render.usuarios(users) #muestra la pagina usuarios.html
        except Exception as error:
            print("Error usuarios.GET: {}".format(error))
            return render.usuarios(error)

class actualizar_usuario:
    def GET(self, localId):
        user = db.child('usuarios').child(localId).get() #obtiene todos los usuarios de la base de datos
        return render.actualizar_usuario(user)
    def POST(self, localId):
        try:
            #obtiene los datos del formulario
            formulario = web.input()
            id = formulario.id
            email = formulario.email
            nombre = formulario.nombre
            telefono = formulario.telefono
            datos = {'nombre': nombre , 'telefono': telefono , 'email':email} #crea un diccionario con los datos del usuario
            resultados = db.child("usuarios").child(id).update(datos) #guarda los datos en la base de datos
            return web.seeother('/usuarios') #redirecciona a la pagina de usuarios
        except Exception as error:
            print("Error actualizar_usuario.POST: {}".format(error)) #imprime en la terminal el error
            return web.seeother('/usuarios') #redirecciona a la pagina de usuarios

if __name__ == "__main__": 
    web.config.debug = False
    app.run()
    