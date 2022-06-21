import os

from src.users.entities.user import User

# Implementación con Firestore para el repositorio de libros.

class FirestoreUsersRepository():
    
    def __init__(self, firestore_client, test = False):

        # Obtener el nombre de la colección desde variables de entorno.
        # Si "test" es true, se le agrega un sufijo, útil para que 
        # las pruebas de integración no sobreescriban los datos existentes.

        self.test = test
        collection_name = os.environ["FIRESTORE_COLLECTION_NAME"]

        if test:
            collection_name += "_test"

        self.collection = firestore_client.collection(collection_name)

    def get_users(self, name = None, email = None, password = None, is_admin = None):

        # Trae una lista de libros desde la colección de Firestore.
        # Al buscarlos, los transforma a entidad User antes de retornarlos.
        # Opcionalmente puede recibir parámetros para filtrar por algún campo.

        results = self.collection.where("deleted_at", "==", None)

        if name:
            results = results.where("name", "==", name)
        
        if email:
            results = results.where("email", "==", email)

        if password:
            results = results.where("password", "==", password)
        
        if is_admin:
            results = results.where("is_admin", "==", is_admin)


        users = []
        
        for document in results.stream():

            content = document.to_dict()
            content["id"] = document.id

            user = User.from_dict(content)
            users.append(user)

        return users

    def get_user(self, user_id):

        content = self.collection.document(user_id).get().to_dict()

        if content and content.get("deleted_at") == None:

            content["id"] = user_id
            user = User.from_dict(content)
            
            return user

        else:
            return None

    def create_user(self, user):

        content = user.to_dict()
        content.pop("id")

        document = self.collection.document()
        document.set(content)

        user.id = document.id
        
        return user

    def update_user(self, user_id, fields):

        # Actualiza la lista de campos recibida el documento especificado.

        document = self.collection.document(user_id).update(fields)
        return self.get_user(user_id)

    def hard_delete_user(self, user_id):

        # Hace un borrado real de un libro. Sólo usado durante tests.

        if self.test:
            self.collection.document(user_id).delete()

    def hard_delete_all_users(self):

        # Borra todos los libros de la colección. Sólo usado durante tests.

        if self.test:

            for document in self.collection.stream():
                self.hard_delete_user(document.id)