from app.database import Base, engine


from app.models import (
    avaliacao,
    cart,
    pedido,
    perfume,
    user
)

print("Tabelas detectadas:", Base.metadata.tables.keys())

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
