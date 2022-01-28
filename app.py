#importa las librerias para el proyecto
import web
import firebase_config as token
import pyrebase
#crea las urls para la aplicación web
urls = (
    '/', 'index',
    '/login', 'login',
    '/signup', 'signup'
)
app = web.application(urls, globals())
render = web.template.render('templates') #directorio de los archivos html
firebase = pyrebase.initialize_app(token.firebaseConfig) #conexión a firebase
auth = firebase.auth()

class index: #pagina raíz 
    def GET(self):
        return 'index'

class login: #pagina login
    def GET(self):
        return render.login()

    def POST(self):
        #obtiene los datos del formulario
        formulario = web.input() 
        email = formulario.email 
        password= formulario.password
        user = auth.sign_in_with_email_and_password(email, password) #autentica los datos con firebase
        if user is not None: #evalua la respuesta de firebase
            return "Bienvenido Usuario"
        else:
            None

class signup: #pagin sign up
    def GET(self):
        return render.registrar()

    def POST(self):
        #obtiene los datos del formulario
        formulario = web.input()
        email = formulario.email
        password= formulario.password
        auth.create_user_with_email_and_password(email, password) #crea un nuevo usuario en firebase
        return "Usuario Creado"

if __name__ == "__main__":
    app.run()
    