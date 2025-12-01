"""
Unit tests untuk Kasir Digital API
Menggunakan pytest framework
"""

import pytest
import json
import os
from app import app
from auth import AuthManager


@pytest.fixture
def client():
    """Setup Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def cleanup():
    """Cleanup test files"""
    yield
    # Clean up test data files
    if os.path.exists('users.json'):
        os.remove('users.json')
    if os.path.exists('transaksi.json'):
        os.remove('transaksi.json')


class TestHome:
    """Test home endpoint"""
    
    def test_home_endpoint(self, client):
        """Test GET / returns welcome message"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'message' in data
        assert data['version'] == '2.0.0'


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user_success(self, client, cleanup):
        """Test successful user registration"""
        response = client.post('/auth/register', 
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'User berhasil terdaftar' in data['message']
    
    def test_register_user_duplicate(self, client, cleanup):
        """Test registering duplicate username"""
        # Register first user
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        
        # Try register same username
        response = client.post('/auth/register',
            json={"username": "testuser", "password": "password456"},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'sudah terdaftar' in data['message']
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        response = client.post('/auth/register',
            json={"username": "testuser"},  # Missing password
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_success(self, client, cleanup):
        """Test successful login"""
        # Register user first
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        
        # Login
        response = client.post('/auth/login',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'token' in data
    
    def test_login_wrong_password(self, client, cleanup):
        """Test login with wrong password"""
        # Register user
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        
        # Try login with wrong password
        response = client.post('/auth/login',
            json={"username": "testuser", "password": "wrongpassword"},
            content_type='application/json'
        )
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post('/auth/login',
            json={"username": "nonexistent", "password": "password123"},
            content_type='application/json'
        )
        assert response.status_code == 401


class TestProtectedRoutes:
    """Test protected API endpoints"""
    
    def test_get_produk_without_token(self, client):
        """Test accessing protected route without token"""
        response = client.get('/api/produk')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Token tidak ditemukan' in data['message']
    
    def test_get_produk_with_invalid_token(self, client):
        """Test accessing protected route with invalid token"""
        response = client.get('/api/produk',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'tidak valid' in data['message']
    
    def test_get_produk_success(self, client, cleanup):
        """Test getting product list with valid token"""
        # Register and login
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        login_response = client.post('/auth/login',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        token = json.loads(login_response.data)['token']
        
        # Get products
        response = client.get('/api/produk',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'data' in data
        assert data['total'] >= 3


class TestTransactions:
    """Test transaction endpoints"""
    
    def test_create_transaction_success(self, client, cleanup):
        """Test creating transaction successfully"""
        # Setup: register and login
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        login_response = client.post('/auth/login',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        token = json.loads(login_response.data)['token']
        
        # Create transaction
        response = client.post('/api/transaksi',
            json={"nama": "Test User", "kode_produk": "ML_86"},
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['harga'] == 20000
    
    def test_create_transaction_invalid_product(self, client, cleanup):
        """Test creating transaction with invalid product code"""
        # Setup
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        login_response = client.post('/auth/login',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        token = json.loads(login_response.data)['token']
        
        # Try invalid product
        response = client.post('/api/transaksi',
            json={"nama": "Test User", "kode_produk": "INVALID"},
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'tidak ditemukan' in data['message']
    
    def test_get_riwayat_success(self, client, cleanup):
        """Test getting transaction history"""
        # Setup
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        login_response = client.post('/auth/login',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        token = json.loads(login_response.data)['token']
        
        # Create transaction
        client.post('/api/transaksi',
            json={"nama": "Test User", "kode_produk": "ML_86"},
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        
        # Get history
        response = client.get('/api/riwayat',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['total'] >= 1
    
    def test_get_laporan_success(self, client, cleanup):
        """Test getting sales report"""
        # Setup
        client.post('/auth/register',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        login_response = client.post('/auth/login',
            json={"username": "testuser", "password": "password123"},
            content_type='application/json'
        )
        token = json.loads(login_response.data)['token']
        
        # Get report
        response = client.get('/api/laporan',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'total_transaksi' in data['data']
        assert 'total_penjualan' in data['data']


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error for nonexistent endpoint"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_missing_json_body(self, client):
        """Test error when JSON body is missing"""
        response = client.post('/auth/register')
        assert response.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
