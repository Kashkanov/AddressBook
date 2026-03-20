from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def reset_db():
    yield
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()

@pytest.fixture(autouse=True)
def override_db():
    def get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)

def test_create_address_complete(client):
    samp_address = {
        "label": "Test",
        "houseNo": "301",
        "street": "Gen. Luna Street",
        "barangay": "Intramuros",
        "city": "Manila",
        "region": "NCR",
        "country": "Philippines",
        "latitude": 14.5896,
        "longitude": 120.9747
    }

    res = client.post("/address/", json=samp_address)
    assert res.status_code == 201
    assert res.json()["label"] == "Test"
    
def test_create_address_empty(client):
    res = client.post("/address/", json={})
    assert res.status_code == 422

def test_create_address_invalid_lat_and_long(client):
    samp_address = {
        "label": "Home",
        "houseNo": "12",
        "street": "Maple",
        "barangay": "San Isidro",
        "city": "Quezon City",
        "region": "NCR",
        "country": "Philippines",
        "latitude": 200,
        "longitude": -200
    }
    
    res = client.post("/address/", json=samp_address)
    assert res.status_code == 422
    
def test_get_addresses_pagination(client):
    addresses = [
        {
            "label": "Home",
            "houseNo": "18",
            "street": "Gen. Luna Street",
            "barangay": "Poblacion",
            "city": "Cavite City",
            "region": "Calabarzon",
            "country": "Philippines",
            "latitude": 14.4790,
            "longitude": 120.8500
        },
        {
            "label": "Work",
            "houseNo": "56",
            "street": "J.P. Rizal Street",
            "barangay": "Barangay 1",
            "city": "Tagbilaran",
            "region": "Central Visayas",
            "country": "Philippines",
            "latitude": 9.6500,
            "longitude": 123.8500
        },
        {
            "label": "Friend_House",
            "houseNo": "22A",
            "street": "Dr. P. Burgos Street",
            "barangay": "San Antonio",
            "city": "Iligan City",
            "region": "Northern Mindanao",
            "country": "Philippines",
            "latitude": 8.2286,
            "longitude": 124.2451
        },
        {
            "label": "Home",
            "houseNo": "77",
            "street": "Mabini Avenue",
            "barangay": "San Isidro",
            "city": "Batangas City",
            "region": "Calabarzon",
            "country": "Philippines",
            "latitude": 13.7563,
            "longitude": 121.0584
        },
        {
            "label": "Work",
            "houseNo": "101",
            "street": "Quezon Avenue",
            "barangay": "Bambang",
            "city": "Baguio",
            "region": "CAR",
            "country": "Philippines",
            "latitude": 16.4023,
            "longitude": 120.5960
        },
        {
            "label": "Friend House",
            "houseNo": "33B",
            "street": "Osmeña Boulevard",
            "barangay": "San Roque",
            "city": "Cebu City",
            "region": "Central Visayas",
            "country": "Philippines",
            "latitude": 10.3157,
            "longitude": 123.8854
        }
    ]
    
    for address in addresses:
        client.post("/address/", json=address)
    
    res = client.get("/address/?skip=2&pageSize=2")
    data = res.json()
    
    assert isinstance(data, list)

    labels = [item["label"] for item in data]

    print(data)
    
    expected_labels = {"Friend_House", "Home"}
    assert expected_labels.issubset(labels) 
    
def test_get_address_exists(client):
    address = {
        "label": "Vacation Home",
        "houseNo": "14",
        "street": "Coral Way",
        "barangay": "Balabag",
        "city": "Malay",
        "region": "Western Visayas",
        "country": "Philippines",
        "latitude": 11.9674,
        "longitude": 121.9248
    }
    
    add = client.post("/address/", json=address)
    added_addr = add.json()
    
    res = client.get(f"/address/{added_addr['id']}")
    data= res.json()
    data.pop("id", None)
    
    assert address == data
    
def test_get_address_DNE(client):
    randID = 599

    res = client.get(f"/address/{randID}")
    
    if res.status_code != 404:
        data = res.json()
        client.delete(f"/address/{data['id']}")
        res = client.get(f"/address/{randID}")
    
    assert res.status_code == 404

def test_update_address(client):
    address = {
        "label": "Vacation House",
        "houseNo": "12",
        "street": "Seaside Boulevard",
        "barangay": "San Juan",
        "city": "Puerto Galera",
        "region": "MIMAROPA",
        "country": "Philippines",
        "latitude": 13.4600,
        "longitude": 120.9500
    }
    
    add = client.post("/address/", json=address)
    added_addr = add.json()
    
    updates = {
        "city": "El Nido",
        "latitude": 13.46142,
        "longitude": 122.0032
    }
    
    res = client.put(f"/address/{added_addr['id']}", json=updates)
    data = res.json()
    
    assert all(data[k] == v for k, v in updates.items())
    
def test_update_address_invalid_fields(client):
    address = {
        "label": "Work",
        "houseNo": "8B",
        "street": "Mabini Street",
        "barangay": "Poblacion",
        "city": "El Nido",
        "region": "MIMAROPA",
        "country": "Philippines",
        "latitude": 11.1952,
        "longitude": 119.4021
    }
    
    add = client.post("/address/", json=address)
    added_addr = add.json()
    
    updates = {   
        "latitude": 200,
        "longitude": -200
    }
    
    res = client.put(f"/address/{added_addr['id']}", json=updates)
    assert res.status_code == 422
    
def test_delete_address(client):
    address = {
        "label": "Home",
        "houseNo": "25",
        "street": "Rizal Avenue",
        "barangay": "Barangay 2",
        "city": "Coron",
        "region": "MIMAROPA",
        "country": "Philippines",
        "latitude": 12.1667,
        "longitude": 120.2000
    }
    
    add = client.post("/address/", json=address)
    added_addr = add.json()
    
    res = client.delete(f"/address/{added_addr['id']}")
    assert res.status_code == 204
    
def test_get_nearby_addresses(client):
    ref = {
        "latitude": 14.5995,
        "longitude": 120.9842,
        "distance": 5
    }
    
    nearby_address = {
        "label": "Nearby Place",
        "houseNo": "10",
        "street": "Taft Avenue",
        "barangay": "Malate",
        "city": "Manila",
        "region": "NCR",
        "country": "Philippines",
        "latitude": 14.5700,
        "longitude": 120.9910
    }
    nearby = client.post("/address/", json=nearby_address)
    
    OOR_address = {
        "label": "Far Place",
        "houseNo": "200",
        "street": "Aguinaldo Highway",
        "barangay": "Aniban",
        "city": "Bacoor",
        "region": "Calabarzon",
        "country": "Philippines",
        "latitude": 14.4120,
        "longitude": 120.9730
    }
    OOR = client.post("/address/", json=OOR_address)
    
    res = client.post("address/nearby/", json=ref)
    data = res.json()
    
    print(f"data is {data}")
    
    assert nearby.json() in data
    assert OOR.json() not in data
    
    
    