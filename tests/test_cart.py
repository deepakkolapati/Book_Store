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
def mock_get_book():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.GET,
            url='http://127.0.0.1:7000/getBook?id=1',
            json={
            'id':1,
            'title': "Time",
            'author':"abhishek",
            'price': 40,
            'quantity': 5,
            'userid': 1
        },
        status=200,
        )
        return res

@pytest.fixture
def mock_get_no_book():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.GET,
            url='http://127.0.0.1:7000/getBook?id=2',
            json={
           "message": "Book is not found", "status": 404}
        ,
        status=404,
        )
        return res


def test_add_cart_item_return_success(cart_client,mock_get_book,mock_authentication,token):
    data={
        "bookid":1,
        "quantity": 4
    }
    response=cart_client.post('/api/cart',json=data,headers={"Content-Type": "application/json" , "Authorization": token})
    assert response.status_code == 201
    assert response.json["message"] == "Book added to cart successfully"

def test_add_cart_item_return_failure(cart_client,mock_get_no_book,mock_authentication,token):
    data={
        "bookid":2,
        "quantity": 4
    }
    response=cart_client.post('/api/cart',json=data,headers={"Content-Type": "application/json" , "Authorization": token})
    assert response.status_code == 404


def test_add_cart_item_wrong_data_return_failure(cart_client,mock_get_book,mock_authentication,token):
    data={
        "bookid":"fdsd",
        "quantity": 4
    }
    response=cart_client.post('/api/cart',json=data,headers={"Content-Type": "application/json" , "Authorization": token})
    assert response.status_code == 400

def test_get_cart_item_return_success(cart_client,mock_get_book,mock_authentication,token):
    data={
        "bookid":1,
        "quantity": 4
    }
    response=cart_client.post('/api/cart',json=data,headers={"Content-Type": "application/json" , "Authorization": token})
    get_response=cart_client.get('/api/cart',headers={"Content-Type": "application/json" , "Authorization": token})
    assert get_response.status_code == 200

