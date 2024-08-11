import pytest 
import responses

@pytest.fixture
def mock_authentication():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.GET,
            url='http://127.0.0.1:5000/getUser?user_id=1',
            json={
            'id':1,            
            "username":"Deepak",
            "email":"deepakkolapati@gmail.com",
            'issuperuser':True,
            'isverified':True
        },
        status=200,
        )
        return res

@pytest.fixture
def mock_normal_user_authentication():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.GET,
            url='http://127.0.0.1:5000/getUser?user_id=1',
            json={
            'id':1,            
            "username":"Deepak",
            "email":"deepakkolapati@gmail.com",
            'issuperuser':False,
            'isverified':True
        },
        status=200,
        )
        return res

@pytest.mark.add_book_success
def test_add_book_return_success(book_client , mock_authentication , token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 70,
        "quantity":  15
    }

    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    assert response.status_code == 201
 


def test_add_book_normal_user_return_failure(book_client , mock_normal_user_authentication , token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 70,
        "quantity":  15
    }

    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    assert response.status_code == 403
  

def test_add_book_wrong_validation_return_failure(book_client,mock_authentication,token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": "jdrd",
        "quantity":  15
    }
    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    assert response.status_code == 400

def test_get_book_return_success(book_client,mock_authentication,token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 20,
        "quantity":  15
           }
    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    get_response=book_client.get('/api/books',headers={"Content-Type": "application/json" , "Authorization": token})
    assert get_response.status_code == 200

def test_put_book_return_success(book_client,mock_authentication,token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 20,
        "quantity":  15
           }
    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    updated_data={
        "title": "hi yo yo",
        "author": "hi yo",
        "price": 25,
        "quantity":  15
    }
    put_response=book_client.put('/api/books?id=1', json=updated_data , headers={"Content-Type": "application/json" , "Authorization": token})
    assert put_response.status_code == 201

def test_put_book_invalid_user_return_failure(book_client,mock_authentication,token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 20,
        "quantity":  15
           }
    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    updated_data={
        "title": "hi yo yo",
        "author": "hi yo",
        "price": 25,
        "quantity":  15
    }
    put_response=book_client.put('/api/books?id=1', json=updated_data , headers={"Content-Type": "application/json" , "Authorization": token+"b"})
    assert put_response.status_code == 401

def test_put_book_invalid_book_details_return_failure(book_client,mock_authentication,token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 20,
        "quantity":  15
           }
    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    updated_data={
        "title": "hi yo yo",
        "author": "hi yo",
        "price": "hfjn",
        "quantity":  15
    }
    put_response=book_client.put('/api/books?id=1', json=updated_data , headers={"Content-Type": "application/json" , "Authorization": token})
    assert put_response.status_code == 400


def test_delete_book_return_success(book_client,mock_authentication,token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 20,
        "quantity":  15
           }
    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    
    delete_response=book_client.delete('/api/books?id=1' , headers={"Content-Type": "application/json" , "Authorization": token})
    assert delete_response.status_code == 204

def test_delete_book_user_invalid_return_failure(book_client,mock_authentication,token):
    data = {
        "title": "hi yo",
        "author": "hi yo",
        "price": 20,
        "quantity":  15
           }
    response = book_client.post('/api/books', json=data , headers={"Content-Type": "application/json" , "Authorization": token})
    
    delete_response=book_client.delete('/api/books?id=1' , headers={"Content-Type": "application/json" , "Authorization": token+"a"})
    assert delete_response.status_code == 401

    
