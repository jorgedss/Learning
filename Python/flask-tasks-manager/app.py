from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

tasks = []
task_id_control= 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control,title=data.get('title'), description=data.get('description'))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso", "id":new_task.id})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks":len(task_list)
        }
    return output
    

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((task for task in tasks if task.id==id),None)
    if task:
        return jsonify(task.to_dict())
    else:
        return jsonify({"message": "Tarefa não econtrada"}), 404
    
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task  = next((task for task in tasks if task.id == id), None)
    
    if task is None:
        return jsonify({"message":"Task não encontrada"}), 404
    
    data = request.get_json()
    task.title = data.get('title')
    task.description = data.get('description')
    task.completed = data.get('completed')
    
    return jsonify({"message":"Tarefa atualizada com sucesso"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task_to_delete = next((task for task in tasks if task.id==id ), None)
    
    if task_to_delete:
        tasks.remove(task_to_delete)
        return jsonify({"message":"Tarefa deletada com sucesso"})
    
    return jsonify({"message":"Tarefa não encontrada"}), 404

if __name__=="__main__":
    """
    Verifica se o script está sendo executado diretamente (não importado como módulo)
    e inicia o servidor Flask em modo de desenvolvimento (debug=True)
    """
    app.run(debug=True, )
    
