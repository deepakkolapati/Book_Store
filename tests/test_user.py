import pytest

@pytest.fixture 
def super_user():
    return {
    "username":"Deepak",
    "email":"deepakkolapati@gmail.com",
    "password": "Kc5656$3ed",
    "superkey":"hf783hboef283920hdchbvb9822991"
}

@pytest.fixture
def  normal_user():
    return {
        "username": "Deepak",
        "email": "deepakkolapati@gmail.com",
        "password": "Hyr345&hd"
    }

@pytest.fixture 
def failure_super_user():
    return {
    "username":"Shrawan",
    "email":"sk0094@srmist.edu.in",
    "password": "Kc5656$3ed",
    "superkey":"hf783hboe"
}


@pytest.fixture 
def invalid_password_user():
    return {
    "username":"Shrawan",
    "email":"sk0094@srmist.edu.in",
    "password": "Kc56563ed"
}

@pytest.fixture
def  invalid_username_user():
    return {
        "username": "De",
        "email": "deepakkolapati@gmail.com",
        "password": "Hyr345&hd"
    }
@pytest.fixture
def  invalid_email_user():
    return {
        "username": "Deepak",
        "email": "deepakkolapatigmail.com",
        "password": "Hyr345&hd"
    }

@pytest.fixture
def login_user():
    return{
    "username":"Deepak",
    "password": "Kc5656$3ed"
    }


@pytest.mark.register_user_success
def test_register_super_user_success(user_client , super_user):
    response = user_client.post('/api/user', json=super_user , headers={"Content-Type": "application/json"})
    assert response.status_code == 201

def test_register_normal_user_success(user_client,normal_user):
    response = user_client.post('/api/user', json=normal_user , headers={"Content-Type": "application/json"})
    assert response.status_code == 201

def test_register_super_user_failure(user_client,failure_super_user):
    response = user_client.post('/api/user', json=failure_super_user , headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_register_invalid_password_user_failure(user_client,invalid_password_user):
    response = user_client.post('/api/user', json=invalid_password_user , headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_register_invalid_username_failuer(user_client,invalid_username_user):
    response = user_client.post('/api/user', json=invalid_username_user , headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_register_invalid_email_failure(user_client,invalid_email_user):
    response = user_client.post('/api/user', json=invalid_email_user , headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_verify_user_return_success(user_client,super_user):
    response=user_client.post('/api/user', json=super_user , headers={"Content-Type": "application/json"})
    data=response.json
    token=data['token']
    verify_response=user_client.get(f'/api/user?token={token}')
    assert verify_response.status_code == 200
    assert verify_response.json['message'] == "User Verified Successfully"

def test_verify_user_return_failure(user_client,super_user):
    response=user_client.post('/api/user', json=super_user , headers={"Content-Type": "application/json"})
    data=response.json
    token=data['token']
    verify_response=user_client.get(f'/api/user?token=')
    assert verify_response.status_code == 404
    
def test_login_user_should_return_success(user_client,super_user,login_user):
    response=user_client.post('/api/user', json=super_user , headers={"Content-Type": "application/json"})
    data=response.json
    login_response=user_client.post('/api/login',json=login_user, headers={"Content-Type": "application/json"})
    assert login_response.status_code == 200
   
def test_login_user_should_return_failure(user_client,super_user):
    response=user_client.post('/api/user', json=super_user , headers={"Content-Type": "application/json"})
    data=response.json
    login_data={
         "username":"Deepak",
    "password": "Kc56563ed"
    }
    login_response=user_client.post('/api/login',json=login_data, headers={"Content-Type": "application/json"})
    assert login_response.status_code == 401
    assert login_response.json['message'] == "Username or Password is incorrect"



def test_reset_password_should_return_success(user_client,super_user):
    response=user_client.post('/api/user', json=super_user , headers={"Content-Type": "application/json"})
    data=response.json
    email_data={
        "email" : "deepakkolapati@gmail.com"
    }
    forget_response = user_client.post('/api/reset',json=email_data, headers={"Content-Type": "application/json"})
    token= forget_response.json['token']
    reset_password_data={
        "newpassword": "Kbv6&*rhb",
        "confirmpassword": "Kbv6&*rhb"
    }
    reset_response=user_client.put(f'/api/reset?token={token}',json=reset_password_data, headers={"Content-Type": "application/json"})
    assert reset_response.status_code == 200
    assert reset_response.json['message'] == "Password changed succesfully"

def test_reset_password_should_return_failure(user_client,super_user):
    response=user_client.post('/api/user', json=super_user , headers={"Content-Type": "application/json"})
    data=response.json
    email_data={
        "email" : "deepakkolapati@gmail.com"
    }
    forget_response = user_client.post('/api/reset',json=email_data, headers={"Content-Type": "application/json"})
    token= forget_response.json['token']
    reset_password_data={
        "newpassword": "Kbv6&*rhb",
        "confirmpassword": "Kbv6*rhb"
    }
    reset_response=user_client.put(f'/api/reset?token={token}',json=reset_password_data, headers={"Content-Type": "application/json"})
    assert reset_response.status_code == 401
  
