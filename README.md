# Backend Test Envíame

La siguiente prueba requiere realizar el diseño y desarrollo de un microservicio de marketplace ecommerce.

El proyecto está enfocado en los aspectos operacionales de un proceso de marketplace ecommerce típico, por lo tanto **debes descartar procesos relacionados a pago y facturación**.

## Requerimientos técnicos
Deberás elegir entre uno de los siguientes lenguajes + frameworks:
1. Python + flask
2. NodeJS + express

- Deberás utilizar docker / docker-compose para proveer una aplicación Dockerizada.
- La API desarrollada deberá considerar algún mecanismo de autenticación como: API Key, Bearer Token, Basic Auth, OAuth
Si no estás familiarizado con Docker, hemos compartido un template para Python y NodeJS. El que ha sido estructurado siguiendo los proncipios definidos por [clean architecture]

Te alentamos a que uses la plantilla provista y te recompensaremos con puntos adicionales las siguientes dos razones: 
- Leer y entender el código escrito por otro desarrollador es una habilidad necesaria y que valoramos.
- Es deseable la comprensión de los principios de clean architecture.

La plantilla proporciona bases de datos mysql, firestore y redis listas para usar. Sientente libre de usar cualquiera de estas herramientas o cualquier combinación de ellas.

## Plazo
Debes entregar la prueba en 72 horas (3 días)

## Antes de comenzar

- Entrega un **repositorio privado de GitHub** con tu código y agrega a los siguiente usuarios como colaboradores: **@rolivagon @rsebjara @vmolina-enviame @vham @rcarrascop**.
- No te olvides de incluir:
    - Debes entregar un microservicio Dockerizada con las instrucciones apropiadas para ejecutar la servicio.
    - README.md con las instrucciones sobre como ejecutar tu app.
    - **Colección de Postman o archivo req.http** con ejemplos e instrucciones sobre como probar todos los endpoints de tu servicio.
    - Archivo de variables de ambiente de ejemplo **(no ignorar archivo .env)** con todas las variables de entorno requeridas.
    - Un archivo **Dockerfile y docker-compose.yml** necesarios para ejecutar tu servicio.
    - Provee un método para poblar la base de datos con datos de prueba.
- Por favor, antes de entregar tu prueba, asegurate de probar tu servicio en un ambiente limpio desde el inicio, con esto te asegurarás de probar en similares condiciones que las que tendrá nuestro equipo Dev para revisar tu prueba. **Si no podemos ejecutar tu servicio, tu prueba será descartada inmediatamente**.
- Dado que se trata de una prueba de backend concéntrate en entregar una API donde podamos probar todas las funcionalidades requeridas. **No es necesario que desarrolles ninguna vista de frontend, ya que tampoco serán evaluadas**.

En caso de cualquier pregunta técnica [contáctanos](mailto:tech-test@enviame.io)

Una vez comenzada la revisión de tu prueba podríamos enviarte algunas preguntas, por lo que apreciaremos tus respuestas oportunas.

## Requerimiento:
1. Desarrolle un microservicio (ms) de marketplace ecommerce basandose en el siguiente modelo ![image](backend%20test%20model.drawio.png).
2. En el sistema deben existir las siguientes entidades:
    - usuarios: USER
    - productos: PRODUCT
    - categorías de productos: CATEGORY
    - transacciones de compra: TRANSACTION
3. En el sistema se deben implementar las siguientes reglas de negocio:    
    - Un USER puede ser comprador (BUYER) y/o vendedor (SELLER).
    - Un USER es SELLER si existe al menos tiene un producto asociado.
    - Un USER es BUYER si existe al menos tiene una transacción de compra de producto.
    - Un producto siempre pertenece a una categoría y a un usuario, quien lo pone a la venta.
    - Un producto no puede estar en más de una categoría.
    - Una transacción siempre requiere a un usuario comprador y uno o mas productos comprados.
    - Un producto tiene una cantidad de unidades, las que se van descontando en la medida en que las unidades son compradas. Una vez que su cantidad llega a cero el producto cambia su status a inactivo. Solo se pueden comprar productos activos, y un producto estará activo si existen unidades disponibles de el.
    - En el caso de una transacción cancelada se debe restituir el stock del producto. 

4. Desarrolle una API que implemente:
    - CRUD de USER, PRODUCT, CATEGORY y TRANSACTION
    - Listado de USER por tipo (BUYER y SELLER)
    - Listado de transacciones por tipo de USER
    - Listado de CATEGORY relacionados con un BUYER USER

5. Asegure lo siguiente:
    - La creación de TRANSACTION descuente unidades de producto.
    - Cuando la cantidad de unidades de un producto llegue a cero ese producto se desactiva y no puede ser vendido hasta que se agreguen más unidades.


## Aspectos a evaluar

Es importante que escribas un archivo README.md con toda las instrucciones necesarias para ejecutar tu servicio, y una collección de postman o un archivo req.http con ejemplos e instrucciones para tu API adecuadamente. 
**Si el README.md está incompleto y/o no proporcionas una colección de Postman o archivo req.http no podremos probar tu servicio, por lo que no podremos evaluar tu prueba**.

- Funcionalidad (45 pts)
- Documentación (7 pts)
    - README.md 
    - Colección de Postman o archivo req.http
- Estilo de programación (6 pts)
- Uso apropiado de respuestas http (4 pts)
- Manejo adecuado de errores y excepciones (4 pts)
- Uso apropiado del template de Clean Architecture (4 pts)

## Aspectos que serán ignorados

- Diseño visual de la solución (frontend)
- Despliegue de la solución

