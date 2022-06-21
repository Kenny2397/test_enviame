import os

from src.categories.entities.category import Category

# Implementación con Firestore para el repositorio de libros.

class FirestoreCategoriesRepository():
    
    def __init__(self, firestore_client, test = False):

        # Obtener el nombre de la colección desde variables de entorno.
        # Si "test" es true, se le agrega un sufijo, útil para que 
        # las pruebas de integración no sobreescriban los datos existentes.

        self.test = test
        collection_name = os.environ["FIRESTORE_COLLECTION_NAME"]

        if test:
            collection_name += "_test"

        self.collection = firestore_client.collection(collection_name)

    def get_categories(self, name = None, description = None, products = None, status = None, seller_user = None, transactions = None, category = None):

        # Trae una lista de libros desde la colección de Firestore.
        # Al buscarlos, los transforma a entidad Category antes de retornarlos.
        # Opcionalmente puede recibir parámetros para filtrar por algún campo.

        results = self.collection.where("deleted_at", "==", None)

        if name:
            results = results.where("name", "==", name)

        if description:
            results = results.where("description", "==", description)

        if products:
            results = results.where("products", "==", products)
            

        categories = []
        
        for document in results.stream():

            content = document.to_dict()
            content["id"] = document.id

            category = Category.from_dict(content)
            categories.append(category)

        return categories

    def get_category(self, category_id):

        content = self.collection.document(category_id).get().to_dict()

        if content and content.get("deleted_at") == None:

            content["id"] = category_id
            category = Category.from_dict(content)
            
            return category

        else:
            return None

    def create_category(self, category):

        content = category.to_dict()
        content.pop("id")

        document = self.collection.document()
        document.set(content)

        category.id = document.id
        
        return category

    def update_category(self, category_id, fields):

        # Actualiza la lista de campos recibida el documento especificado.

        document = self.collection.document(category_id).update(fields)
        return self.get_category(category_id)

    def hard_delete_category(self, category_id):

        # Hace un borrado real de un libro. Sólo usado durante tests.

        if self.test:
            self.collection.document(category_id).delete()

    def hard_delete_all_categories(self):

        # Borra todos los libros de la colección. Sólo usado durante tests.

        if self.test:

            for document in self.collection.stream():
                self.hard_delete_category(document.id)