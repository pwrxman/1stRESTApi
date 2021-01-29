from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

#cadena de conexion a la base de datos flaskmysql en el motor de mysql
#previamente debde de existir o crearse dicha base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Andres24@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

ma = Marshmallow(app)

# El ORM crea una tabla Task basada en el modelo con las columnas descrito
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    #El constructor de cada Task
    def __init__(self, title, description):
        self.title = title
        self.description = description

#ionstruccion para crear el modelo Task y su constructor para ejecutar cada tarea
db.create_all()

#Crear el esquema para interactuar con el modelo de Task
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()        
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])

def create_task():

    #aqui se utiliza la app POSTMAN para probar si las peticiones ya llegan al localhost:5000
    #antes de continuar con el resto del tutorial
    #print(request.json)
    #return 'received chingon'

    #Una vez que funciona la prueba del postman continuamos
    #se reciben los datos que envia el cliente
    #cada uno de los datos recibidos se guardan en variables
    title = request.json['title']
    description = request.json['description']

    #Se genera una nueva tarea task
    new_task = Task(title, description)

    #se guarda en la base de datos
    db.session.add(new_task)
    db.session.commit()

    #cuando el servidor acaba la tarea se requiere que nos de respuesta
    return task_schema.jsonify(new_task)

#Ahora haremos una tarea para consultar el contenido completo de la tabla task
#es decir el equivalente a un 'select * from task'
@app.route('/tasks', methods=['GET'])    
def get_tasks():
    #Se hace la consulta a la tabla y el resultado se guarda en una variable
    all_tasks = Task.query.all()
    #se recibe el resultado y se almacena en una variable para mostrar al cliente
    result = tasks_schema.dump(all_tasks)

    return jsonify(result)
    #hasta aqui y via el POSTMAN se puede ir probando que los POST al server funcionan OK
    #Tambien se puede validar que cada peticion genera un nuevo registgro en la tabla task


#Ahora haremos una tarea para consultar el contenido especifico de la tabla task
#es decir el equivalente a un 'select * from task WHERE una condicion'
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

#Ahora haremos una tarea para modificar el contenido especifico de la tabla task
#es decir el equivalente a un 'UPDATE campo from task WHERE una condicion'
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    #se define la tarea quew quiereo actualizar
    task = Task.query.get(id)
    #sson los datos que se quiereo actualizar
    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)    


#Ahora haremos una tarea para eliminar el contenido especifico de la tabla task
#es decir el equivalente a un 'DELETE campo from task WHERE una condicion'
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    #se define la tarea quew quiereo actualizar
    task = Task.query.get(id)
    
    db.session.delete(task)
    db.session.commit()
    
    return task_schema.jsonify(task)   

#solo para que se vea mas amigable
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Wwlcome Buddys'})


if __name__ == "__main__":
    app.run(debug=True)





