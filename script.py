# encoding: utf-8
import web
from web import form
from web.contrib.template import render_mako
from pymongo import MongoClient
import feedparser
import tweepy


web.config.debug = False

urls = ( '/logout', 'logout',
        '/registro', 'registro',
        '/ver_perfil', 'ver_perfil',
        '/editar_perfil', 'editar_perfil',
        '/mas_visitadas', 'mas_visitadas',
        '/rss', 'rss',
        '/highchart', 'highchart',
        '/mapa', 'mapa',
        '/twitter', 'twitter',
        '/eventos_twitter', 'eventos_twitter',
        '/(.*)', 'login' 
    )

# Consumer keys and access tokens, used for OAuth
consumer_key = 'UbeG6c5YaR1a7gZYdLqqr7fFN'
consumer_secret = 'BTrE1bbvDz6SuxKxlKF1mHof955YheUjb7gzGoLk590fF4BpIQ'
access_token = '519720537-MsyxcBoaLUES8U0ECtzinEQ9ivbTMRO4CHBLtk98'
access_token_secret = 'XEhkECGK0z0uVuj9XfC1tMOeZxeSCvdReBzPxTyR1uEDS'
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Creation of the actual interface, using authentication
api = tweepy.API(auth)


feed= feedparser.parse('portada_elpais.xml')

app = web.application(urls, globals(), autoreload=True)

plantillas = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8'
        )

#Conexión a la base de datos
try:
    client = MongoClient()
    db = client.usuarios
    print "Conexión realizada con éxito"
except pymongo.errors.ConnectionFailure, e:
    print "Error al conectar con MongoDB: %s" % e


dias=range(1,32)
meses=range(1,13)
anios=range(1915,2015)

form_reg = form.Form(
    form.Textbox('user', form.notnull, description="Nombre de Usuario"),
    form.Textbox('nombre', form.notnull, form.regexp('^[A-Z, a-z]', 'No hay nadie en el mundo cuyo nombre tenga números.¡Use letras!'), description="Nombre"),
    form.Textbox('apellidos', form.notnull, form.regexp('^[A-Z, a-z]', 'No hay nadie en el mundo cuyo apellido tenga números.¡Use letras!'), description="Apellido"),
    form.Textbox('correo', form.notnull,  form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', 'Introduzca un correo válido'), description="Correo electrónico"),

    form.Dropdown('dias', dias, description="Dia"),
    form.Dropdown('meses', meses, description="Mes"),
    form.Dropdown('anios', anios, description="Anio"),

    form.Textarea('direccion', form.notnull,  description="Dirección"),
    form.Password('clave', form.notnull, description="Contraseña"),
    form.Password('clave2', form.notnull, description="Repetir contraseña"),
    form.Radio('pago', ['Contra reembolso', 'Tarjeta VISA'], description="Forma de pago"),
    form.Textbox('visa', form.regexp('((\d{4})[\-,\s](\d{4})[\-,\s](\d{4})[\-,\s](\d{4}))', 'Introduzca un número de tarjeta VISA válido'), description="Tarjeta VISA"),
    form.Checkbox('clausula', form.Validator("Acepta las clausulas", lambda i: i == 'true'), value='true', description="¿Nos vende su alma?"),
    form.Button('Registrarse'),
    validators = [form.Validator("Fecha de nacimiento no válida.", lambda i: (((int(i.meses) == 2) and  ((int(i.dias) <= 28) and ((int(i.anios) % 4) != 0) or (int(i.dias) <= 29) and ((int(i.anios) % 4) == 0))) or ((int(i.dias) <= 31) and ((int(i.meses) == 1) or (int(i.meses) == 3) or (int(i.meses) == 5) or (int(i.meses) == 7) or (int(i.meses) == 8) or (int(i.meses) == 10) or (int(i.meses) == 12))) or ((int(i.dias) <= 30) and ((int(i.meses) == 4) or (int(i.meses) == 6) or (int(i.meses) == 9) or (int(i.meses) == 11))))), form.Validator("Las contraseñas no coinciden.", lambda i: i.clave == i.clave2),  form.Validator('Míninmo 7 caracteres', lambda x:len(x.clave)>=7), form.Validator('Míninmo 7 caracteres', lambda x:len(x.clave2)>=7)]

)

form_log = form.Form(
    form.Textbox('usuario'),
    form.Password('contrasenia'),
    form.Button('Login')
)

form_twitter_palabra = form.Form(
    form.Textbox('twitter_palabra', form.notnull, description="Palabra"),
    form.Textbox('num_resultados', form.notnull, description="Numero de resultados"),
    form.Button('Buscar')
)

form_twitter_usuario = form.Form(
    form.Textbox('usuario', form.notnull, description="Nombre de Usuario"),
    form.Textbox('num_resultados', form.notnull, description="Numero de resultados"),
    form.Button('Buscar')
)

form_twitter_eventos = form.Form(
    form.Textbox('twitter_palabra', form.notnull, description="", id="texto_evento"),
    form.Button('Buscar', id="boton_evento")
)


class registro:
    def GET(self):
        res=""
        r = form_reg()
        web.header('Content-Type', 'text/html; charset=utf-8')
        try: 
            res="Bienvenido usuario: %s " % (web.cookies().user)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "registro")
            return plantillas.pagina_registro_conectado(formulario=res, registro=r.render())
        except:
            l=form_log()
            res = l.render()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_registro_desconectado(formulario=res, registro=r.render())

    def POST(self):
        r = form_reg()
        l=form_log()
        res=""
        if not r.validates():
            web.header('Content-Type', 'text/html; charset=utf-8')
            try: 
                res="Bienvenido usuario: %s " % (web.cookies().user)
                return plantillas.pagina_registro_conectado(formulario=res, registro=r.render())
            except:
                l=form_log()
                return plantillas.pagina_registro_desconectado(formulario=l.render(), registro=r.render())
        else:
            web.header('Content-Type', 'text/html; charset=utf-8')
            post = {"user": r.d.user,
                    "nombre": r.d.nombre,
                    "apellidos": r.d.apellidos,
                    "correo": r.d.correo,
                    "dia": r.d.dias,
                    "mes": r.d.meses,
                    "anio": r.d.anios,
                    "direccion": r.d.direccion,
                    "password": r.d.clave,
                    "pago": r.d.pago,
                    "visa": r.d.visa,
                    }

            posts=db.posts
            query=posts.find({"user":r.d.user})
            if query.count() == 0: 
                post_id = posts.insert(post)           
                mensaje = "Enhorabuena te has registrado con exito."
                web.header('Content-Type', 'text/html; charset=utf-8')
                try: 
                    res="Bienvenido usuario: %s " % (web.cookies().user)
                    return plantillas.pagina_registro_conectado(formulario=res, registro=mensaje)
                except:
                    l=form_log()
                    return plantillas.pagina_registro_desconectado(formulario=l.render(), registro=mensaje)
            else:
                mensaje=r.render()+"Ya existe un usuario con ese nombre de usuario."
                try: 
                    res="Bienvenido usuario: %s " % (web.cookies().user)
                    return plantillas.pagina_registro_conectado(formulario=res, registro=mensaje)
                except:
                    l=form_log()
                    return plantillas.pagina_registro_desconectado(formulario=l.render(), registro=mensaje)



class login:
    def GET(self, name):
        try: 
            mensaje="Bienvenido usuario: %s" % (web.cookies().user)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "login")
            return plantillas.pagina_conectado(formulario=mensaje)
        except:
        	l=form_log()
        	web.header('Content-Type', 'text/html; charset=utf-8')
        	return plantillas.pagina_desconectado(formulario=l.render(), mensaje="")

    def POST(self,name):
        l=form_log()
        if l.validates():
            posts=db.posts
            query=posts.find({"user":l['usuario'].value})
            if query.count() != 0:
                usuario = query[0]["user"]
                password = query[0]["password"]
                if password != l['contrasenia'].value:
                    web.header('Content-Type', 'text/html; charset=utf-8')
                    return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Contrasenia incorrecta.")
                else:
                    web.setcookie('user', usuario)
                    web.setcookie('pagina1',"")
                    web.setcookie('pagina2',"")
                    web.setcookie('pagina3',"")
                    mensaje="Bienvenido usuario: %s " % (usuario)
                    web.header('Content-Type', 'text/html; charset=utf-8')
                    return plantillas.pagina_conectado(formulario=mensaje)
            else:
                web.header('Content-Type', 'text/html; charset=utf-8')
                return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Usuario incorrecto.")


class logout:
    def GET(self):
        web.setcookie('user', web.cookies().user, -3600)
        web.setcookie('pagina1', web.cookies().pagina1, -3600)
        web.setcookie('pagina2', web.cookies().pagina2, -3600)
        web.setcookie('pagina3', web.cookies().pagina3, -3600)
        l=form_log()
        web.header('Content-Type', 'text/html; charset=utf-8')
        return plantillas.pagina_desconectado(formulario=l.render(), mensaje="")


class ver_perfil:
    def GET(self):
        try: 
            posts=db.posts
            query=posts.find({"user":web.cookies().user})
            usuario1 = query[0]["user"]
            password1 = query[0]["password"]
            nombre1 = query[0]["nombre"]
            apellidos1 = query[0]["apellidos"]
            correo1 = query[0]["correo"]
            dia1 = query[0]["dia"]
            mes1 = query[0]["mes"]
            anio1 = query[0]["anio"]
            direccion1 = query[0]["direccion"]
            pago1 = query[0]["pago"]
            visa1 = query[0]["visa"]
            res="Bienvenido usuario: %s " % (usuario1)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "ver_perfil")
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.datos_perfil(formulario=res, mensaje="", usuario = usuario1, password = password1, nombre= nombre1, apellidos=apellidos1, correo=correo1, dia=dia1, mes=mes1, anio=anio1, direccion=direccion1, pago=pago1, visa=visa1)
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")

class editar_perfil:
    def GET(self):
        try:
            posts=db.posts
            query=posts.find({"user":web.cookies().user})
            form_reg_editar = form.Form(
                form.Textbox('nombre', form.notnull, form.regexp('^[A-Z, a-z]', 'No hay nadie en el mundo cuyo nombre tenga números.¡Use letras!'), description="Nombre", value=query[0]["nombre"]),
                form.Textbox('apellidos', form.notnull, form.regexp('^[A-Z, a-z]', 'No hay nadie en el mundo cuyo apellido tenga números.¡Use letras!'), description="Apellido", value=query[0]["apellidos"]),
                form.Textbox('correo', form.notnull,  form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', 'Introduzca un correo válido'), description="Correo electrónico", value=query[0]["correo"]),

                form.Dropdown('dias', dias, description="Dia", value=int(query[0]["dia"])),
                form.Dropdown('meses', meses, description="Mes", value=int(query[0]["mes"])),
                form.Dropdown('anios', anios, description="Anio", value=int(query[0]["anio"])),

                form.Textarea('direccion', form.notnull,  description="Dirección", value=query[0]["direccion"]),
                form.Password('clave', form.notnull, description="Contraseña", value=query[0]["password"]),
                form.Password('clave2', form.notnull, description="Repetir contraseña", value=query[0]["password"]),
                form.Radio('pago', ['Contra reembolso', 'Tarjeta VISA'], description="Forma de pago", value=query[0]["pago"]),
                form.Textbox('visa', form.regexp('((\d{4})[\-,\s](\d{4})[\-,\s](\d{4})[\-,\s](\d{4}))', 'Introduzca un número de tarjeta VISA válido'), description="Tarjeta VISA", value=query[0]["visa"]),
                form.Button('Editar'),
                validators = [form.Validator("Fecha de nacimiento no válida.", lambda i: (((int(i.meses) == 2) and  ((int(i.dias) <= 28) and ((int(i.anios) % 4) != 0) or (int(i.dias) <= 29) and ((int(i.anios) % 4) == 0))) or ((int(i.dias) <= 31) and ((int(i.meses) == 1) or (int(i.meses) == 3) or (int(i.meses) == 5) or (int(i.meses) == 7) or (int(i.meses) == 8) or (int(i.meses) == 10) or (int(i.meses) == 12))) or ((int(i.dias) <= 30) and ((int(i.meses) == 4) or (int(i.meses) == 6) or (int(i.meses) == 9) or (int(i.meses) == 11))))), form.Validator("Las contraseñas no coinciden.", lambda i: i.clave == i.clave2),  form.Validator('Míninmo 7 caracteres', lambda x:len(x.clave)>=7), form.Validator('Míninmo 7 caracteres', lambda x:len(x.clave2)>=7)]
            )
            res="Bienvenido usuario: %s " % (web.cookies().user)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "editar_perfil")
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.editar_perfil(formulario=res, registro=form_reg_editar.render())
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")


    def POST(self):
        try:
            posts=db.posts
            query=posts.find({"user":web.cookies().user})
            form_reg_editar = form.Form(
                form.Textbox('nombre', form.notnull, form.regexp('^[A-Z, a-z]', 'No hay nadie en el mundo cuyo nombre tenga números.¡Use letras!'), description="Nombre", value=query[0]["nombre"]),
                form.Textbox('apellidos', form.notnull, form.regexp('^[A-Z, a-z]', 'No hay nadie en el mundo cuyo apellido tenga números.¡Use letras!'), description="Apellido", value=query[0]["apellidos"]),
                form.Textbox('correo', form.notnull,  form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', 'Introduzca un correo válido'), description="Correo electrónico", value=query[0]["correo"]),

                form.Dropdown('dias', dias, description="Dia", value=int(query[0]["dia"])),
                form.Dropdown('meses', meses, description="Mes", value=int(query[0]["mes"])),
                form.Dropdown('anios', anios, description="Anio", value=int(query[0]["anio"])),

                form.Textarea('direccion', form.notnull,  description="Dirección", value=query[0]["direccion"]),
                form.Password('clave', form.notnull, description="Contraseña", value=query[0]["password"]),
                form.Password('clave2', form.notnull, description="Repetir contraseña", value=query[0]["password"]),
                form.Radio('pago', ['Contra reembolso', 'Tarjeta VISA'], description="Forma de pago", value=query[0]["pago"]),
                form.Textbox('visa', form.regexp('((\d{4})[\-,\s](\d{4})[\-,\s](\d{4})[\-,\s](\d{4}))', 'Introduzca un número de tarjeta VISA válido'), description="Tarjeta VISA", value=query[0]["visa"]),
                form.Button('Editar'),
                validators = [form.Validator("Fecha de nacimiento no válida.", lambda i: (((int(i.meses) == 2) and  ((int(i.dias) <= 28) and ((int(i.anios) % 4) != 0) or (int(i.dias) <= 29) and ((int(i.anios) % 4) == 0))) or ((int(i.dias) <= 31) and ((int(i.meses) == 1) or (int(i.meses) == 3) or (int(i.meses) == 5) or (int(i.meses) == 7) or (int(i.meses) == 8) or (int(i.meses) == 10) or (int(i.meses) == 12))) or ((int(i.dias) <= 30) and ((int(i.meses) == 4) or (int(i.meses) == 6) or (int(i.meses) == 9) or (int(i.meses) == 11))))), form.Validator("Las contraseñas no coinciden.", lambda i: i.clave == i.clave2),  form.Validator('Míninmo 7 caracteres', lambda x:len(x.clave)>=7), form.Validator('Míninmo 7 caracteres', lambda x:len(x.clave2)>=7)]
            )
            res="Bienvenido usuario: %s " % (web.cookies().user)
            if form_reg_editar.validates():
                posts.update( { "user": web.cookies().user }, { '$set': { "nombre": form_reg_editar.d.nombre}})
                posts.update( { "user": web.cookies().user }, { '$set': { "apellidos": form_reg_editar.d.apellidos}})
                posts.update( { "user": web.cookies().user }, { '$set': { "correo": form_reg_editar.d.correo}})
                posts.update( { "user": web.cookies().user }, { '$set': { "dia" : form_reg_editar.d.dias}})
                posts.update( { "user": web.cookies().user }, { '$set': { "mes" : form_reg_editar.d.meses}})
                posts.update( { "user": web.cookies().user }, { '$set': { "anio" : form_reg_editar.d.anios}})
                posts.update( { "user": web.cookies().user }, { '$set': { "direccion": form_reg_editar.d.direccion}})
                posts.update( { "user": web.cookies().user }, { '$set': { "password" : form_reg_editar.d.clave}})
                posts.update( { "user": web.cookies().user }, { '$set': { "pago" : form_reg_editar.d.pago}})
                posts.update( { "user": web.cookies().user }, { '$set': { "visa" : form_reg_editar.d.visa}})
                web.header('Content-Type', 'text/html; charset=utf-8')
                return plantillas.editar_perfil(formulario=res, registro="Cambios realizados correctamente.")
            else:
                web.header('Content-Type', 'text/html; charset=utf-8')
                return plantillas.editar_perfil(formulario=res, registro=form_reg_editar.render())
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")

class mas_visitadas:

    def GET(self):
        try:
            res="Bienvenido usuario: %s " % (web.cookies().user)
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.mas_visitadas(formulario=res, pagina1=web.cookies().pagina1, pagina2=web.cookies().pagina2, pagina3=web.cookies().pagina3)
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")        

class rss:

    def GET(self):
        res=""
        web.header('Content-Type', 'text/html; charset=utf-8')
        try: 
            res="Bienvenido usuario: %s " % (web.cookies().user)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "rss")
            return plantillas.rss_conectado(formulario=res, feed=feed)
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")     


class highchart:

    def GET(self):
        res=""
        web.header('Content-Type', 'text/html; charset=utf-8')
        try: 
            res="Bienvenido usuario: %s " % (web.cookies().user)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "highchart")
            return plantillas.highchart(formulario=res)
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")     


class mapa:

    def GET(self):
        res=""
        web.header('Content-Type', 'text/html; charset=utf-8')
        try: 
            res="Bienvenido usuario: %s " % (web.cookies().user)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "mapa")
            return plantillas.mapa(formulario=res)
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")     



class twitter:
    def GET(self):
        try:
            l = form_twitter_palabra();
            l2 = form_twitter_usuario();
            base_datos=""
            rt_medio=0
            res="Bienvenido usuario: %s " % (web.cookies().user)
            web.setcookie('pagina3', web.cookies().pagina2)
            web.setcookie('pagina2', web.cookies().pagina1)
            web.setcookie('pagina1', "twitter")
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.twitter(base_datos=base_datos, formulario=res, form_twitter= l.render(), form_twitter2=l2.render(), mensaje_busqueda="", tweets="", rt_medio=rt_medio)
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")


    def POST(self):
        try:
            l = form_twitter_palabra();
            l2 = form_twitter_usuario();
            base_datos=""
            res="Bienvenido usuario: %s " % (web.cookies().user)
            mensaje=""
            rt_medio=0
            if l.validates():
                tweets = api.search(q=l.d.twitter_palabra, count=l.d.num_resultados)
                tweets2 = tweets
                posts=db.posts
                for i in range(len(tweets)):
                    rt_medio+=int(tweets[i].retweet_count)

                rt_medio=rt_medio/len(tweets)
                post = {"palabra": l.d.twitter_palabra,
                        "retweet_medio" : rt_medio
                }
                post_id = posts.insert(post)   
                posts=db.posts
                base_datos=posts.find({"palabra":l.d.twitter_palabra})
                web.header('Content-Type', 'text/html; charset=utf-8')
                mensaje = "Ultimos %s tweets que incluyen la palabra '%s' :" % (l.d.num_resultados, l.d.twitter_palabra)
                return plantillas.twitter(base_datos=base_datos, formulario=res, form_twitter= l.render(), form_twitter2=l2.render(), mensaje_busqueda=mensaje, tweets=tweets, rt_medio=rt_medio)
            elif l2.validates():
                tweets = api.user_timeline(screen_name = l2.d.usuario, include_rts = True, result_type = "recent", count = l2.d.num_resultados)
                for i in range(len(tweets)):
                    rt_medio+=int(tweets[i].retweet_count)

                rt_medio=rt_medio/len(tweets)
                mensaje = "Ultimos %s tweets del usuario '%s' :" % (l2.d.num_resultados, l2.d.usuario)
                return plantillas.twitter(base_datos=base_datos, formulario=res, form_twitter= l.render(), form_twitter2=l2.render(), mensaje_busqueda=mensaje, tweets=tweets, rt_medio=rt_medio) 
            else:
                web.header('Content-Type', 'text/html; charset=utf-8')
                return plantillas.twitter(base_datos=base_datos, formulario=res, form_twitter= l.render(), form_twitter2=l2.render(), mensaje_busqueda=mensaje, tweets="Error de busqueda", rt_medio=rt_medio)
        except:
            l=form_log()
            web.header('Content-Type', 'text/html; charset=utf-8')
            return plantillas.pagina_desconectado(formulario=l.render(), mensaje="Se ha producido algun error. Inicie sesion de nuevo.")

class eventos_twitter:

    def GET(self):
            l = form_twitter_eventos();
            return plantillas.eventos_twitter(form=l.render(), tweets="", locations="")

    def POST(self):
        l = form_twitter_eventos();
        locations=[];
        if l.validates():
            tweets = api.search(q=l.d.twitter_palabra, count=100)
            for tweet in tweets:
                if tweet.coordinates is not None:
                    locations.append(tweet.coordinates['coordinates'][1])
                    locations.append(tweet.coordinates['coordinates'][0])

            return plantillas.eventos_twitter(form= l.render(), tweets=tweets, locations=locations)


if __name__ == "__main__":
    app.run()


