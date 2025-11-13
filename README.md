## TP Aseguradoras

TP Aseguradoras es un sistema backoffice que ejemplifica el uso de bases de datos NoSQL para la gestión de información de una compañía de seguros.
El objetivo de este proyecto es implementar y comprender la persistencia poliglota utilizando MongoDB (como System of Record) y Neo4j (como grafo de relaciones), accedidas a través de una API REST desarrollada con FastAPI.

##  Prerequisitos

Para ejecutar el proyecto, necesitás tener instaladas las siguientes herramientas:

* Docker
* Docker Compose
(ya incluido en las versiones modernas de Docker para Windows y macOS; los usuarios de Linux deben instalarlo por separado).

No es necesario un entorno virtual (.venv) local, ya que todo el entorno se ejecuta dentro de los contenedores Docker.

🚀 Ejecución de TP Aseguradoras

Primero, cloná el proyecto y entrá al directorio raíz:

git clone git@github.com:KatiaMenshikoff/tpo_bd2.git
cd tpo_bd2


Luego, copiá el archivo de variables de entorno de ejemplo:

```bash
cp .env.example .env
```

Asegurate de que las variables estén configuradas correctamente, por ejemplo:
```bash
# MongoDB
MONGO_URI="mongodb://mongo:27017"
MONGO_DB="aseguradora_tp"

# Neo4j
NEO4J_URI="bolt://neo4j:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"
```
Si se ejecuta por primera vez el proyecto, o se tiene una cantidad masiva de datos a insertar a la DB, se puede importar en bulk datos desde archivos CSV. Para eso, debe ubicarse los csv a importar en el directorio src/data del proyecto. Si este no existe, por favor crearlo y copiar los archivos allí. Luego, desde la interfaz gráfica disponible en localhost:8000/docs, ejecutamos el llamado al endpoint en import/data “Importar datos”. Veamos los requerimientos de dicho endpoint:

Finalmente, levantá los contenedores con el siguiente comando:
```bash
docker compose up -d --build
```

Esto descargará las imágenes oficiales de MongoDB y Neo4j desde Docker Hub (si no las tenés localmente) e instanciará tres contenedores conectados en una red virtual interna:

tp_app → FastAPI (lógica y API REST)

tp_mongo → MongoDB (base de datos documental)

tp_neo4j → Neo4j (base de datos de grafo)

Toda esta configuración se ejecuta automáticamente.

Para detener la aplicación pero mantener los datos:
```bash
docker compose down
```

Si querés detener la aplicación y eliminar los datos y volúmenes asociados:
```bash
docker compose down -v
```

Una vez levantada, la API estará disponible en
👉 http://localhost:8000

🌐 Endpoints principales

La API REST, desarrollada con FastAPI, puede ser accedida mediante herramientas como curl, Postman, Insomnia, o directamente desde el navegador.
FastAPI también genera una interfaz visual de documentación en Swagger.

Acceso a Swagger UI:
👉 http://localhost:8000/docs

### `/clientes`
GET /clientes

Obtiene un listado de todos los clientes registrados.

POST /clientes

Crea un nuevo cliente en la base de datos.

Ejemplo de cuerpo JSON:
```json
{
  "id_cliente": 1001,
  "nombre": "Juan",
  "apellido": "Pérez",
  "direccion": "Calle Falsa 123",
  "activo": true
}
```
### `/clientes/{id}`

PATCH /clientes/{id}

Actualiza parcialmente los datos del cliente con el ID especificado.

DELETE /clientes/{id}

Elimina el cliente cuyo ID es el especificado.

### `/polizas`
POST /polizas

Emite una nueva póliza, validando que el cliente y el agente existan y estén activos.
Ejemplo:
```json
{
  "nro_poliza": "P-105",
  "id_cliente": 3,
  "id_agente": 1,
  "tipo": "Automotor",
  "fecha_inicio": "01/01/2025",
  "fecha_fin": "31/12/2025",
  "prima_mensual": 15000,
  "cobertura_total": 1000000,
  "estado": "Activa"
}
```
### `/siniestros`
POST /siniestros

Reporta un nuevo siniestro asociado a una póliza existente.
Ejemplo:
```json
{
  "id_siniestro": 501,
  "nro_poliza": "P-105",
  "fecha": "12/02/2025",
  "tipo": "Accidente",
  "descripcion": "Colisión leve",
  "monto_estimado": 20000,
  "estado": "Abierto"
}
```
Consultas (Q1–Q12)

Las consultas predefinidas del sistema permiten explorar información combinada entre MongoDB y Neo4j.
Ejemplo de endpoints:

Endpoint	Descripción
/q1	Clientes activos con sus pólizas vigentes
/q2	Siniestros abiertos con tipo, monto y cliente afectado
/q3	Vehículos asegurados con su cliente y póliza (Neo4j)
/q4	Clientes sin pólizas activas (Neo4j)
/q5	Agentes activos con cantidad de pólizas asignadas (Neo4j)
/q7	Top 10 clientes por cobertura total

Ejemplo de uso:

curl "http://localhost:8000/q7"

👨‍💻 Autores

Trabajo realizado por: Grupo 1
Katia Menshikoff
Agostina Squillari
Javier Peral Belmont
Tomas Pinausig
Instituto Tecnológico de Buenos Aires (ITBA)
Año 2025
