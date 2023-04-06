from routes import app,db
import json
from models import TA
from werkzeug.security import generate_password_hash, check_password_hash
import pytest
import jwt

@pytest.fixture
def client():
    client = app.test_client()
    return client

def test_add_ta():
    with app.test_client() as client:
        # Define the test data
        data = {
            'native_english_speaker': 'true',
            'course_instructor': 'John Doe',
            'course': 'CSC101',
            'semester': 'regular',
            'class_size': '50',
            'performance_score': '85',
            'email': 'jane@example.com',
            'password': 'password123'
        }
        print('data',data)
        # Send a POST request with the test data to the /Add route
        response = client.post('/Add', json=data)
        # Check that the response status code is 200 (OK)
        assert response.status_code == 200
        # Parse the response JSON data
        ta_data = json.loads(response.data)
        # Check that the TA object was added to the database
        ta = db.session.query(TA).filter_by(email=data['email']).first()
        assert ta is not None
        # Check that the TA object was serialized correctly in the response data
        assert ta_data['native_english_speaker'] == data['native_english_speaker']
        assert ta_data['course_instructor'] == data['course_instructor']
        assert ta_data['course'] == data['course']
        assert ta_data['semester'] == data['semester']
        assert ta_data['class_size'] == data['class_size']
        assert ta_data['performance_score'] == data['performance_score']
        assert ta_data['email'] == data['email']
        assert check_password_hash(ta_data['password'], data['password'])   
        

def test_log_data():
    with app.test_client() as client:
        # Create a new TA user for testing
        ta = TA(native_english_speaker=True,
            course_instructor='John Doe',
            course='CSC101',
            semester='regular',
            class_size=50,
            performance_score=85,
            email='jane@example.com',
            password='password123')
        
        app.config['SECRET_KEY'] = 'mysecretkey'
       
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        # Add the TA user to the database
        with app.app_context():
            db.create_all()
            db.session.add(ta)
            db.session.commit()
            
        data = {
            'email': 'jane@example.com',
            'password': 'password123'
        }
        # Send a POST request with the test data to the /login route
        response = client.post('/login', data=data)
        
        # Check that the response status code is 201 (Created)
        assert response.status_code == 201
        # Parse the response JSON data
        response_data = json.loads(response.data)
        # Check that the response contains a token
        assert 'token' in response_data


   



def test_retrieve_function(client):
    # create a test token for the current_user
    token = jwt.encode({'id': 184}, app.config['SECRET_KEY'], algorithm='HS256')
    headers = {'x-access-token': token}
    
    # send a GET request to the endpoint with the test token
    response = client.get('/retrieve/242', headers=headers)
    print('response',response.data)
    # assert that the response is successful (HTTP status code 200)
    assert response.status_code == 200
    
    # assert that the response contains the expected data
    expected_data = {
        "class_size": "10",
        "course": "statistics",
        "course_instructor": "Kiii",
        "email": "jack@gmail.com",
        "id": 242,
        "native_english_speaker": "False",
        "password": "pbkdf2:sha256:260000$9tHgiW2rR0ZbkHwM$422c05b01d13aaa4b4cb933f03d69027ffdb0d5b292fb91d75ee3e51e7a00359",
        "performance_score": "12",
        "semester": "regular"

    }
    assert json.loads(response.data) == expected_data
    


# @pytest.fixture
def test_delete_student():
    with app.app_context():
        with app.test_client() as client:
            token = jwt.encode({'id': 185}, app.config['SECRET_KEY'], algorithm='HS256')
            headers = {'x-access-token': token}
            # Create a new TA user for testing
            ta = TA(
                 class_size =  "50",
                course = "Maths",
                course_instructor = "Ram",
                email= "ram@gmail.com",
                native_english_speaker =  "True",
                password =  "pbkdf2:sha256:260000$867FBREB2Kdsa1rn$159439b55918aa6e5b52ba01fc47fbecfa9c8d3a15de6e8f4e3dc5efb0cea87c",
                performance_score =  "1055",
                semester =  "summer"
            )
            db.session.add(ta)
            db.session.commit()
            # Send a DELETE request with the token to the /delete route
            response = client.delete(f'/delete/{ta.id}', headers=headers)
            print('response',response.data)

            # Check that the response status code is 200 (OK)
            assert response.status_code == 200

            # Check that the TA user was deleted from the database
            deleted_ta = db.session.query(TA).filter_by(email='jane@example.com').first()
            # assert deleted_ta is None

            # Check that the response message is "Deleted successfully"
            response_data = json.loads(response.data)
            print('response',response_data)
            assert response_data == 'Deleted succesfully'
            







