import os

from src.products.entities.product import Product

# Implementación con Firestore para el repositorio de libros.

class FirestoreProductsRepository():
    
    def __init__(self, firestore_client, test = False):

        # Obtener el nombre de la colección desde variables de entorno.
        # Si "test" es true, se le agrega un sufijo, útil para que 
        # las pruebas de integración no sobreescriban los datos existentes.

        self.test = test
        collection_name = os.environ["FIRESTORE_COLLECTION_NAME"]

        if test:
            collection_name += "_test"

        self.collection = firestore_client.collection(collection_name)

    def get_products(self, name = None, description = None, quantity = None, status = None, seller_user = None, transactions = None, category = None):

        # Trae una lista de libros desde la colección de Firestore.
        # Al buscarlos, los transforma a entidad Product antes de retornarlos.
        # Opcionalmente puede recibir parámetros para filtrar por algún campo.

        results = self.collection.where("deleted_at", "==", None)

        if name:
            results = results.where("name", "==", name)

        if description: 
            results = results.where("description", "==", description)

        if quantity:
            results = results.where("quantity", "==", quantity)

        if status:  
            results = results.where("status", "==", status)
        
        if seller_user:
            results = results.where("seller_user", "==", seller_user)

        if transactions:    
            results = results.where("transactions", "==", transactions)

        if category:
            results = results.where("category", "==", category)

        

        products = []
        
        for document in results.stream():

            content = document.to_dict()
            content["id"] = document.id

            product = Product.from_dict(content)
            products.append(product)

        return products

    def get_product(self, product_id):

        content = self.collection.document(product_id).get().to_dict()

        if content and content.get("deleted_at") == None:

            content["id"] = product_id
            product = Product.from_dict(content)
            
            return product

        else:
            return None

    def create_product(self, product):

        content = product.to_dict()
        content.pop("id")

        document = self.collection.document()
        document.set(content)

        product.id = document.id
        
        return product

    def update_product(self, product_id, fields):

        # Actualiza la lista de campos recibida el documento especificado.

        document = self.collection.document(product_id).update(fields)
        return self.get_product(product_id)

    def hard_delete_product(self, product_id):

        # Hace un borrado real de un libro. Sólo usado durante tests.

        if self.test:
            self.collection.document(product_id).delete()

    def hard_delete_all_products(self):

        # Borra todos los libros de la colección. Sólo usado durante tests.

        if self.test:

            for document in self.collection.stream():
                self.hard_delete_product(document.id)