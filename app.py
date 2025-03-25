from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurant_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)  # Aumentar la longitud del campo

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de Pedido
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    producto_nombre = db.Column(db.String(100), nullable=False)
    producto_precio = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Pedido {self.id} - Cliente: {self.cliente}>'

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Formulario de contacto
class ContactoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Enviar')

# Formulario de login
class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# Formulario de registro
class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# Formulario de pedido
class PedidoForm(FlaskForm):
    cliente = StringField('Cliente', validators=[DataRequired(), Length(max=100)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    metodo_pago = SelectField('Método de Pago', choices=[('tarjeta', 'Tarjeta'), ('efectivo', 'Efectivo')], validators=[DataRequired()])
    producto_nombre = StringField('Nombre del Producto', validators=[DataRequired(), Length(max=100)])
    producto_precio = DecimalField('Precio del Producto', validators=[DataRequired()])
    submit = SubmitField('Crear Pedido')

# Ruta principal
@app.route('/')
def index():
    usuario_nombre = session.get('usuario_nombre')
    return render_template('index.html', usuario_nombre=usuario_nombre)

# Ruta "Catálogo"
@app.route('/catalogo', methods=['GET', 'POST'])
def catalogo():
    productos = [
        {"id": 1, "nombre": "Pizza Margarita", "precio": 10.99, "descripcion": "Pizza clásica con tomate, mozzarella y albahaca."},
        {"id": 2, "nombre": "Hamburguesa", "precio": 8.99, "descripcion": "Hamburguesa con queso, lechuga y tomate."},
        {"id": 3, "nombre": "Ensalada César", "precio": 7.99, "descripcion": "Ensalada fresca con pollo, crutones y aderezo César."},
        {"id": 4, "nombre": "Lasaña", "precio": 12.99, "descripcion": "Lasaña de carne con queso y salsa de tomate."},
        {"id": 5, "nombre": "Tacos", "precio": 9.99, "descripcion": "Tacos de pollo con guacamole y salsa picante."}
    ]

    if request.method == 'POST':
        selected_products = request.form.getlist('productos')
        total_price = sum(float(productos[int(id) - 1]['precio']) for id in selected_products)
        metodo_pago = request.form.get('metodo_pago')
        return render_template('resumen_pedido.html', productos=productos, selected_products=selected_products, total_price=total_price, metodo_pago=metodo_pago, int=int)

    return render_template('catalogo.html', productos=productos)

# Ruta "Crear Pedido"
@app.route('/crear_pedido', methods=['GET', 'POST'])
def crear_pedido():
    form = PedidoForm()
    if form.validate_on_submit():
        nuevo_pedido = Pedido(
            cliente=form.cliente.data,
            direccion=form.direccion.data,
            metodo_pago=form.metodo_pago.data,
            producto_nombre=form.producto_nombre.data,
            producto_precio=form.producto_precio.data
        )
        db.session.add(nuevo_pedido)
        db.session.commit()

        flash('Pedido creado exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('crear_pedido.html', form=form)

# Ruta "Contacto"
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        mensaje = form.mensaje.data

        # Aquí puedes manejar los datos, como enviarlos por correo o guardarlos en la base de datos
        print(f"Nombre: {nombre}, Email: {email}, Mensaje: {mensaje}")

        flash('¡Gracias por contactarnos! Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('index'))

    return render_template('contacto.html', form=form)

# Ruta "Login"
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            session['usuario_nombre'] = usuario.nombre
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo electrónico o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

# Ruta "Registro"
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = form.password.data
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. ¡Bienvenido, {}!'.format(nombre), 'success')
        return redirect(url_for('bienvenida', nombre=nombre))
    return render_template('register.html', form=form)

# Ruta "Bienvenida"
@app.route('/bienvenida/<nombre>')
def bienvenida(nombre):
    return render_template('bienvenida.html', nombre=nombre)

# Ruta "Logout"
@app.route('/logout')
def logout():
    session.pop('usuario_nombre', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('index'))

# Ruta "Comentarios"
@app.route('/comentarios')
def comentarios():
    comentarios = [
        {"nombre": "María", "rating": 5, "comentario": "Siempre están rapidísimas y muy buenas."},
        {"nombre": "Roxana Elva Ottaviano", "rating": 4, "comentario": "Falta que gratinen las empanadas como antes, ya que da otro toque que los hace distintos."},
        {"nombre": "Pablo", "rating": 5, "comentario": "Primera vez que utilizo la app. Excelente servicio."}
    ]
    return render_template('comentarios.html', comentarios=comentarios)

# Manejo de errores 404
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
