import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db_usuarios, db_productos

client = TestClient(app)

@pytest.fixture(autouse=True)
def limpiar_base_de_datos():
    """Limpia las listas simuladas antes de ejecutar cada test."""
    db_usuarios.clear()
    db_productos.clear()


def test_1_1_registro_usuario_exitoso():
    """Test 1.1: Datos válidos -> 201 Created"""
    payload = {"username": "usuario_valido", "edad": 25}
    response = client.post("/users/registro", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["usuario"]["username"] == "usuario_valido"
    assert data["usuario"]["edad"] == 25

def test_1_2_registro_usuario_edad_invalida():
    """Test 1.2: Edad menor a 18 años -> 422 Unprocessable Entity"""
    payload = {"username": "usuario_joven", "edad": 15}
    response = client.post("/users/registro", json=payload)
    
    assert response.status_code == 422

def test_1_3_registro_usuario_duplicado():
    """Test 1.3: Nombre de usuario ya existente -> 400 Bad Request"""
    payload = {"username": "usuario_repetido", "edad": 20}
    # Primer registro exitoso
    client.post("/users/registro", json=payload)
    
    # Segundo registro con el mismo nombre debe fallar
    response = client.post("/users/registro", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "El usuario ya existe en la base de datos"

def test_1_4_busqueda_por_id_exitoso_y_defecto():
    """Test 1.4a: ID existente -> 200 OK y valor por defecto 'general'"""
    client.post("/users/registro", json={"username": "usuario_test", "edad": 30})
    
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["categoria"] == "general"

def test_1_4_busqueda_por_id_no_encontrado():
    """Test 1.4b: ID no existente -> 404 Not Found"""
    response = client.get("/users/999")
    assert response.status_code == 404

def test_1_4_busqueda_por_id_invalido():
    """Test 1.4c: ID <= 0 -> 422 Unprocessable Entity"""
    response = client.get("/users/0")
    assert response.status_code == 422


def test_2_1_agregar_producto_token_correcto():
    """Test 2.1: POST con token correcto -> 201 Created"""
    payload = {"nombre": "Notebook", "precio": 1200.50}
    response = client.post("/products/?token=nivel-intermedio-2026", json=payload)
    
    assert response.status_code == 401
    assert response.json()["producto"]["nombre"] == "Notebook"

def test_2_2_agregar_producto_token_incorrecto():
    """Test 2.2: POST con token erróneo o ausente -> 401 Unauthorized"""
    payload = {"nombre": "Teclado", "precio": 50.0}
    
    # Intento sin token
    response_sin_token = client.post("/products/", json=payload)
    assert response_sin_token.status_code == 401

    # Intento con token erróneo
    response_token_erroneo = client.post("/products/?token=token_invalido", json=payload)
    assert response_token_erroneo.status_code == 401

def test_3_1_listar_productos_sin_token_bloqueado_globalmente():
    """Test 3.1: GET sin token protegido por la dependencia del router -> 401 Unauthorized"""
    response = client.get("/products/")
    assert response.status_code == 401