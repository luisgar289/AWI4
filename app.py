#importa las librerias para el proyecto
import web
import firebase_config as token
import pyrebase
import json

#url y funcion de la aplicacion web
urls = (
    '/', 'index',
    '/login', 'login',
    '/signup', 'signup',
    '/bienvenida','bienvenida',
    '/logout', 'logout'
)
app = web.application(urls, globals())
render = web.template.render('templates') #directorio de los archivos html
firebase = pyrebase.initialize_app(token.firebaseConfig) #conexión a firebase
auth = firebase.auth() #verifica la conexion a firebase

class index: #pagina raíz 
    def GET(self):
        return 'index'

class login: #pagina login
    def GET(self):
        return render.login() #muestra la pagina login.html

    def POST(self):
        try:
            #obtiene los datos del formulario
            formulario = web.input() 
            email = formulario.email 
            password= formulario.password
            user = auth.sign_in_with_email_and_password(email, password) #autentica los datos con firebase
            informacion = auth.get_account_info(user['idToken'])
            usuarios = informacion['users']
            usuario = usuarios[0]
            localId = usuario['localId']
            web.setcookie('localid', localId)
            return web.seeother('bienvenida') #muestra la pagina de bienvenida.html, pero no redirecciona
        except Exception as error: #recopila y muestra los datos de algun error
            formato = json.loads(error.args[1])
            error = formato['error']
            message = error['message']
            print(formato)
            #print("Error Login.POST: {}".format(message)) #imprime en la terminal el error
            if message == "INVALID_EMAIL": 
                return render.loginerror_mail() #muestra la pagina loginerror_mail
            elif message == "EMAIL_NOT_FOUND": 
                return render.loginerror_mail() #muestra la pagina loginerror_mail
            else:
                return render.loginerror_pass() #muestra la pagina loginerror_pass

class signup: #pagin sign up
    def GET(self):
        return render.registrar()

    def POST(self):
        try:
            #obtiene los datos del formulario
            formulario = web.input()
            email = formulario.email
            password= formulario.password
            auth.create_user_with_email_and_password(email, password) #crea un nuevo usuario en firebase
            return web.seeother('login') #redirecciona a la pagina del login
        except Exception as error: #recopila los datos del error
            formato = json.loads(error.args[1])
            error = formato['error']
            message = error['message']
            print("Error Login.POST: {}".format(message)) #imprime en la terminal el error
            if message == "EMAIL_EXISTS":
                return render.registrarerror_mail() #muestra la pagina registrarerror_mail
            else:
                return render.registrarerror_pass() #muestra la pagina registrarerror_pass

class bienvenida: 
    def GET(self):
        return render.bienvenida()

    def POST(self):
        cookie = web.cookies().get('localid')
        if cookie is not None:
            return web.seeother('bienvenida')
        else:
            return web.seeother('login')
    
class logout:
    def GET(self):
        web.setcookie('localid', None)
        cookie = web.cookies().get('localid')
        print(cookie)
        return web.seeother('login')
            

if __name__ == "__main__":
    web.config.debug = False
    app.run()
    