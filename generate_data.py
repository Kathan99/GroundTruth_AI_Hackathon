import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_IN')

def generate_users(num_users=50):
    users = []
    for i in range(num_users):
        phone = f"+91-{random.randint(60000, 99999)}-{random.randint(10000, 99999)}"
        
        user = {
            "user_id": f"USR-{i+1:03d}",
            "name": fake.name(),
            "phone_number": phone,
            "preferences": {
                "favorite_drink": random.choice(["Masala Chai", "Filter Coffee", "Cappuccino", "Ginger Tea", "Lassi"]),
                "size": random.choice(["Small", "Medium", "Large"]),
                "milk": random.choice(["Whole", "Oat", "Almond", "Soy"]),
                "sugar": random.choice(["None", "1 tsp", "2 tsp"])
            },
            "loyalty_points": random.randint(0, 500),
            "location": {
                "latitude": 19.0760 + random.uniform(-0.1, 0.1),
                "longitude": 72.8777 + random.uniform(-0.1, 0.1)
            },
            "past_orders": []
        }

        if random.random() < 0.7:
            num_orders = random.randint(1, 5)
            for j in range(num_orders):
                user["past_orders"].append({
                    "order_id": f"ORD-{i+1:03d}-{j+1:03d}",
                    "item": random.choice(["Masala Chai", "Samosa", "Vada Pav", "Filter Coffee", "Bun Maska"]),
                    "date": fake.date_this_year().isoformat(),
                    "amount": round(random.uniform(50.0, 300.0), 2)
                })
        
        users.append(user)
    return users

def generate_stores(num_stores=5):
    stores = []
    base_lat = 19.0760
    base_lon = 72.8777
    
    for i in range(num_stores):
        store = {
            "store_id": f"store_{i+1}",
            "name": f"Chai Point - {fake.street_name()}",
            "location": {
                "latitude": base_lat + random.uniform(-0.05, 0.05),
                "longitude": base_lon + random.uniform(-0.05, 0.05),
                "address": fake.address().replace("\n", ", ")
            },
            "hours": {
                "open": "08:00",
                "close": "22:00"
            },
            "stock": {
                "Masala Chai": True,
                "Filter Coffee": True,
                "Samosa": True,
                "Vada Pav": random.choice([True, False]),
                "Bun Maska": True,
                "Ginger Tea": True
            },
            "offers": [
                {"code": "CHAI20", "description": "20% off Masala Chai", "valid_until": "2025-12-31"}
            ] if random.random() > 0.5 else []
        }
        stores.append(store)
    return stores

if __name__ == "__main__":
    users = generate_users(50)
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=2)
    print(f"Generated {len(users)} users in data/users.json")

    stores = generate_stores(5)
    with open("data/stores.json", "w") as f:
        json.dump(stores, f, indent=2)
    print(f"Generated {len(stores)} stores in data/stores.json")
