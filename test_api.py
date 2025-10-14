#!/usr/bin/env python3
"""
Script para testar a API Netflix Catalog
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Testa o endpoint de health"""
    print("Testando /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_catalog():
    """Testa o endpoint de catálogo"""
    print("Testando /catalog...")
    response = requests.get(f"{BASE_URL}/catalog")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Items encontrados: {len(data.get('items', []))}")
    if data.get('items'):
        print(f"Primeiro item: {data['items'][0]}")
    print()

def test_catalog_item():
    """Testa o endpoint de item específico"""
    print("Testando /catalog/<id>...")
    # Primeiro, pega um item do catálogo
    response = requests.get(f"{BASE_URL}/catalog")
    if response.status_code == 200:
        items = response.json().get('items', [])
        if items:
            item_id = items[0]['id']
            response = requests.get(f"{BASE_URL}/catalog/{item_id}")
            print(f"Status: {response.status_code}")
            print(f"Item: {response.json()}")
        else:
            print("Nenhum item encontrado no catálogo")
    print()

def test_watch():
    """Testa o endpoint de visualização"""
    print("Testando POST /watch...")
    # Primeiro, pega um item do catálogo
    response = requests.get(f"{BASE_URL}/catalog")
    if response.status_code == 200:
        items = response.json().get('items', [])
        if items:
            item_id = items[0]['id']
            payload = {"userId": "user123", "itemId": item_id}
            response = requests.post(f"{BASE_URL}/watch", json=payload)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        else:
            print("Nenhum item encontrado no catálogo")
    print()

def test_recommendations():
    """Testa o endpoint de recomendações"""
    print("Testando /recommendations/<userId>...")
    response = requests.get(f"{BASE_URL}/recommendations/user123")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Recomendações para user123: {len(data.get('recommendations', []))} itens")
    if data.get('recommendations'):
        print(f"Primeira recomendação: {data['recommendations'][0]}")
    print()

if __name__ == "__main__":
    print("Testando API Netflix Catalog\n")
    
    try:
        test_health()
        test_catalog()
        test_catalog_item()
        test_watch()
        test_recommendations()
        
        print("Todos os testes concluidos!")
        
    except requests.exceptions.ConnectionError:
        print("Erro: Nao foi possivel conectar ao servidor.")
        print("Certifique-se de que o servidor Flask esta rodando em http://127.0.0.1:8000")
    except Exception as e:
        print(f"Erro inesperado: {e}")
