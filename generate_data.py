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

def generate_stores(num_stores_per_city=5):
    stores = []
    
    # Real coordinates for major hubs
    hubs = {
        "Mumbai": [
            {"name": "Bandra West", "lat": 19.0607, "lon": 72.8362},
            {"name": "Andheri West", "lat": 19.1136, "lon": 72.8697},
            {"name": "Colaba", "lat": 18.9067, "lon": 72.8147},
            {"name": "Powai", "lat": 19.1176, "lon": 72.9060},
            {"name": "Juhu", "lat": 19.1075, "lon": 72.8263}
        ],
        "Delhi NCR": [
            {"name": "Connaught Place", "lat": 28.6315, "lon": 77.2167},
            {"name": "Hauz Khas", "lat": 28.5494, "lon": 77.2001},
            {"name": "Cyber Hub (Gurgaon)", "lat": 28.4950, "lon": 77.0895},
            {"name": "Sector 29 (Gurgaon)", "lat": 28.4695, "lon": 77.0637},
            {"name": "Noida Sector 18", "lat": 28.5708, "lon": 77.3271}
        ],
        "Bangalore": [
            {"name": "Indiranagar", "lat": 12.9716, "lon": 77.6412},
            {"name": "Koramangala", "lat": 12.9352, "lon": 77.6245},
            {"name": "MG Road", "lat": 12.9766, "lon": 77.5993},
            {"name": "Whitefield", "lat": 12.9698, "lon": 77.7500}
        ]
    }
    
    store_id_counter = 1
    
    for city, locations in hubs.items():
        for loc in locations:
            # Create a store at this exact hub location (or slightly offset)
            store = {
                "store_id": f"store_{store_id_counter}",
                "name": f"Velvet Brew - {loc['name']}",
                "location": {
                    "latitude": loc["lat"],
                    "longitude": loc["lon"],
                    "address": f"{loc['name']}, {city}, India"
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
                    {"code": "BREW20", "description": "20% off Hot Beverages", "valid_until": "2025-12-31"}
                ] if random.random() > 0.3 else []
            }
            stores.append(store)
            store_id_counter += 1
            
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
