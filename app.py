from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuración para Docker y local
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/restaurant_db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)

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
    producto_nombre = db.Column(db.String(100))
    producto_precio = db.Column(db.Numeric(10, 2))
    total_precio = db.Column(db.Numeric(10, 2))
    estado = db.Column(db.String(50), default='pendiente')
    creado_en = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __repr__(self):
        return f'<Pedido {self.id} - Cliente: {self.cliente}>'

# Formulario de pedido
class PedidoForm(FlaskForm):
    cliente = StringField('Cliente', validators=[DataRequired(), Length(max=100)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    metodo_pago = SelectField('Método de Pago', choices=[('tarjeta', 'Tarjeta'), ('efectivo', 'Efectivo')], validators=[DataRequired()])
    submit = SubmitField('Realizar Pedido')

# Formulario de inicio de sesión
class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# Formulario de registro
class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

# Context processor para usuario en todas las plantillas
@app.context_processor
def inject_usuario():
    return dict(usuario_nombre=session.get('usuario_nombre'))

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

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
        flash(f'Pedido creado exitosamente. Total: ${total_price:.2f}', 'success')
        return redirect(url_for('index'))
    return render_template('catalogo.html', productos=productos)

# Ruta "Crear Pedido"
@app.route('/crear_pedido', methods=['GET', 'POST'])
def crear_pedido():
    entradas = [
        {"id": 1, "nombre": "Bruschettas"},
        {"id": 2, "nombre": "Empanadas"},
        {"id": 3, "nombre": "Ensalada César"}
    ]
    platos = [
        {"id": 1, "nombre": "Pizza Margarita"},
        {"id": 2, "nombre": "Hamburguesa Gourmet"},
        {"id": 3, "nombre": "Pasta Alfredo"},
        {"id": 4, "nombre": "Lasaña"}
    ]
    bebidas = [
        {"id": 1, "nombre": "Limonada"},
        {"id": 2, "nombre": "Cerveza Artesanal"},
        {"id": 3, "nombre": "Vino Tinto"}
    ]
    form = PedidoForm()
    if form.validate_on_submit():
        # Aquí puedes procesar el pedido según tu lógica
        flash('Pedido creado exitosamente.', 'success')
        return redirect(url_for('index'))
    return render_template('crear_pedido.html', form=form, entradas=entradas, platos=platos, bebidas=bebidas)

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
            flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

# Ruta "Registro"
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('register'))
        usuario = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            direccion=form.direccion.data,
            email=form.email.data
        )
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Ruta "Logout"
@app.route('/logout')
def logout():
    session.pop('usuario_nombre', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('index'))

# Manejo de errores 404
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)