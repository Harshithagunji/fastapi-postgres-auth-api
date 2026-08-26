import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, get_db
from main import app

# using sqlite for testing so, will not mess up with postgresql data

SQLALCHEMY_DATABASE_URL='sqlite:///./test.db'

engine= create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}
)
TestingSessionLocal=sessionmaker(autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db=TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db]=override_get_db

current_username=f'user_{uuid.uuid4().hex[:6]}'

client= TestClient(app)

def test_register_user():
    response=client.post(
        '/register',
        params={'username':current_username,'password':'testpassword'}
    )
    assert response.status_code==201
    data=response.json()
    assert data['message']=='User registered successfully'
    

# getting the access token after registration
def test_login_user():
    response=client.post(
        '/token',
        data={'username':current_username,'password':'testpassword'}
    )
    assert response.status_code==200
    data=response.json()
    print('LOGIN RESPONSE DATA:',data)
    assert 'access_token' in data
    assert data['token_type']=='bearer'

    headers={'Authorization': f'Bearer {data['access_token']}'}

    #testing book CRUD

    # create book
    book_data={
        'title':'FastAPI Handbook',
        'author':'Developer',
        'description':'Testing CRUD',
        'year':2026
    }
    create_res=client.post('/books', json=book_data, headers=headers)
    assert create_res.status_code in[200,201]
    book_id=create_res.json()['id']

   # Read Book
    get_res=client.get(f'/books/{book_id}', headers=headers)
    assert get_res.status_code==200
    assert get_res.json()['title']=='FastAPI Handbook'

   # update Book

    update_data={
        'title':'FastAPI Handbook Updated',
        'author':'Developer',
        'description':'Updated description',
        'year':2026
    }
    update_res=client.put(f'/books/{book_id}',json=update_data, headers=headers)
    assert update_res.status_code==200
    assert update_res.json()['title'] == 'FastAPI Handbook Updated'

    #Delete Book
    delete_res= client.delete(f'/books/{book_id}',headers=headers)
    assert delete_res.status_code==200

    #Deletion verification
    verify_res= client.get(f'/books/{book_id}',headers=headers)
    assert verify_res.status_code==404