import pytest
import requests

#Create
BASE_URL = 'http://127.0.0.1:5000/'
tasks = []

def test_create_task():
    """
    Criação de tarefa
    """
    
    new_task = {
        "title": "Tarefa teste",
        "description": "Uma tarefa de teste "
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json['id'])
    
def test_get_tasks():
    """ 
    Leitura de tarefas
    """
    
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def test_get_task():
    """ 
    Leitura de uma única tarefas
    """
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['id'] == task_id
        
def test_update_task():
    if tasks:
        tasks_id = tasks[0]
        payload = {
            "title":"Teste passou",
            "description": "Significa que o teste passou",
            "completed":True
        }
        response = requests.put(f"{BASE_URL}/tasks/{tasks_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['message'] == "Tarefa atualizada com sucesso"

def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response  = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404