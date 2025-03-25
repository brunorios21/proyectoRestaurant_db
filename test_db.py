from app import app, Pedido  # Importa la aplicación y el modelo Pedido

with app.app_context():
    pedidos = Pedido.query.all()
    print(pedidos)