import web
import firebase_config as token
import pyrebase

urls = (
    '/', 'index',
    '/login', 'login',
    '/signup', 'signup'
)
app = web.application(urls, globals())
render = web.template.render('templates')
firebase = pyrebase.initialize_app(token.firebaseConfig)
auth = firebase.auth()

class index:
    def GET(self):
        return 'index'

class login:
    def GET(self):
        return render.login()

    def POST(self):
        formulario = web.input()
        email = formulario.email
        password= formulario.password
        user = auth.sign_in_with_email_and_password(email, password)
        if user is not None:
            return "Bienvenido Usuario"
        else:
            None

class signup:
    def GET(self):
        return render.registrar()

    def POST(self):
        formulario = web.input()
        email = formulario.email
        password= formulario.password
        auth.create_user_with_email_and_password(email, password)
        return "Usuario Creado"

if __name__ == "__main__":
    app.run()