from src.frameworks.db.firestore import create_firestore_client
from src.frameworks.db.redis import create_redis_client
from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app


from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.users.usecases.manage_users_usecase import ManageUsersUsecase
from src.users.http.users_blueprint import create_users_blueprint
from src.users.repositories.firestore_users_repository import FirestoreUsersRepository

from src.products.repositories.sqlalchemy_products_repository import SQLAlchemyProductsRepository
from src.products.usecases.manage_products_usecase import ManageProductsUsecase
from src.products.http.products_blueprint import create_products_blueprint
from src.products.repositories.firestore_products_repository import FirestoreProductsRepository

from src.categories.repositories.sqlalchemy_categories_repository import SQLAlchemyCategoriesRepository
from src.categories.usecases.manage_categories_usecase import ManageCategoriesUsecase
from src.categories.http.categories_blueprint import create_categories_blueprint
from src.categories.repositories.firestore_categories_repository import FirestoreCategoriesRepository

from src.greeting.http.greeting_blueprint import create_greeting_blueprint
from src.greeting.repositories.redis_greeting_cache import RedisGreetingCache
from src.greeting.usecases.greeting_usecase import GreetingUsecase

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

redis_client = create_redis_client()
redis_greeting_cache = RedisGreetingCache(redis_client)

# firestore instance
firestore_client = create_firestore_client()


# repositories firestore  instances
firestore_users_repository = FirestoreUsersRepository(firestore_client)
firestore_products_repository = FirestoreProductsRepository(firestore_client)
firestore_categories_repository = FirestoreCategoriesRepository(firestore_client)

# sqlalchemy instance
sqlalchemy_client = SQLAlchemyClient()

# repositories sqlachemy instances
sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_products_repository = SQLAlchemyProductsRepository(sqlalchemy_client)
sqlalchemy_categories_repository = SQLAlchemyCategoriesRepository(sqlalchemy_client)


sqlalchemy_client.create_tables()

greeting_usecase = GreetingUsecase(redis_greeting_cache)

# manage_books_usecase = ManageBooksUsecase(firestore_books_repository)


manage_users_usecase = ManageUsersUsecase(sqlalchemy_users_repository)
manage_products_usecase = ManageProductsUsecase(sqlalchemy_products_repository)
manage_categories_usecase = ManageCategoriesUsecase(sqlalchemy_categories_repository)

blueprints = [
    create_greeting_blueprint(greeting_usecase),
    create_users_blueprint(manage_users_usecase),
    create_products_blueprint(manage_products_usecase),
    create_categories_blueprint(manage_categories_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)