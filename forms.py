from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class PedidoForm(FlaskForm):
    cliente = StringField('Cliente', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    metodo_pago = SelectField('Método de Pago', choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta')], validators=[DataRequired()])
    estado_envio = SelectField('Estado de Envío', choices=[('pendiente', 'Pendiente'), ('enviado', 'Enviado')], validators=[DataRequired()])
    submit = SubmitField('Crear Pedido')

class DetallePedidoForm(FlaskForm):
    producto_id = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()])
    submit = SubmitField('Agregar Producto')