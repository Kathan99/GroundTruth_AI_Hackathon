import json
import math
from typing import Dict, List, Optional

class ContextManager:
    def __init__(self, users_path="data/users.json", stores_path="data/stores.json"):
        with open(users_path, "r") as f:
            self.users = {u["user_id"]: u for u in json.load(f)}
        
        with open(stores_path, "r") as f:
            self.stores = json.load(f)

    def get_user(self, user_id: str) -> Optional[Dict]:
        return self.users.get(user_id)

    def get_nearest_store(self, lat: float, lon: float) -> Dict:
        """
        Finds the nearest store using Haversine formula.
        """
        nearest_store = None
        min_dist = float("inf")

        for store in self.stores:
            s_lat = store["location"]["latitude"]
            s_lon = store["location"]["longitude"]
            
            dist = math.sqrt((lat - s_lat)**2 + (lon - s_lon)**2)
            
            if dist < min_dist:
                min_dist = dist
                nearest_store = store
        
        return nearest_store

    def format_context(self, user_id: str, current_lat: float, current_lon: float) -> str:
        """
        Builds the context string for the LLM.
        """
        user = self.get_user(user_id)
        if not user:
            return "User not found."

        store = self.get_nearest_store(current_lat, current_lon)
        
        context = []
        
        context.append(f"User: {user['name']}")
        context.append(f"Preferences: {user['preferences']['size']} {user['preferences']['favorite_drink']} "
                       f"({user['preferences']['milk']} Milk, {user['preferences']['sugar']})")
        context.append(f"Loyalty Points: {user['loyalty_points']}")
        
        if user['past_orders']:
            last_order = user['past_orders'][0]
            context.append(f"Last Order: {last_order['item']} on {last_order['date']}")
        
        if store:
            context.append(f"Nearest Store: {store['name']} (Open: {store['hours']['open']}-{store['hours']['close']})")
            
            if store['offers']:
                offers = ", ".join([f"{o['code']} ({o['description']})" for o in store['offers']])
                context.append(f"Active Offers: {offers}")
            else:
                context.append("Active Offers: None")
                
            unavailable = [k for k, v in store['stock'].items() if not v]
            if unavailable:
                context.append(f"Out of Stock: {', '.join(unavailable)}")
        
        return "\n".join(context)

if __name__ == "__main__":
    cm = ContextManager()
    user_id = list(cm.users.keys())[0]
    user = cm.get_user(user_id)
    
    lat = user['location']['latitude']
    lon = user['location']['longitude']
    
    print(f"Context for {user_id} at {lat}, {lon}:")
    print("-" * 20)
    print(cm.format_context(user_id, lat, lon))
