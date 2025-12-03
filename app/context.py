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

    def find_user_id(self, identifier: str) -> Optional[str]:
        """
        Finds a user ID by exact match, phone number, or extracting from text.
        """
        import re
        
        if identifier in self.users:
            return identifier
            
        for uid, user in self.users.items():
            if user.get("phone_number") == identifier:
                return uid

        id_match = re.search(r"USR-\d+", identifier, re.IGNORECASE)
        if id_match:
            extracted_id = id_match.group(0).upper()
            if extracted_id in self.users:
                return extracted_id
        
        phone_match = re.search(r"\+91-\d{5}-\d{5}", identifier)
        if phone_match:
            extracted_phone = phone_match.group(0)
            for uid, user in self.users.items():
                if user.get("phone_number") == extracted_phone:
                    return uid
                    
        return None

    def get_nearest_store(self, lat: float, lon: float) -> tuple[Dict, float]:
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
        
        return nearest_store, min_dist

    def find_stores_by_text(self, query: str) -> List[Dict]:
        """
        Finds stores by matching city or area names in the query.
        """
        if not query:
            return []
            
        query_lower = query.lower()
        matches = []
        for store in self.stores:
            try:
                name = store["name"].lower()
                address = store["location"]["address"].lower()
                address_parts = [p.strip().lower() for p in store["location"]["address"].split(",")]
                
                match_found = False
                
                for part in address_parts:
                    if part in query_lower and len(part) > 3: 
                        match_found = True
                        break
                
                if match_found or query_lower in name or query_lower in address:
                    matches.append(store)
            except Exception as e:
                print(f"Error matching store {store.get('store_id')}: {e}")
                continue
                
        return matches

    def format_context(self, user_id: str, current_lat: float, current_lon: float, query: str = "", include_location: bool = True) -> str:
        """
        Builds the context string for the LLM.
        """
        user = self.get_user(user_id)
        
        context = []
        
        if include_location:
            context.append(f"Current Location: Lat: {current_lat:.4f}, Lon: {current_lon:.4f}")
        
        if user:
            context.append(f"User: {user['name']}")
            context.append(f"Preferences: {user['preferences']['size']} {user['preferences']['favorite_drink']} "
                           f"({user['preferences']['milk']} Milk, {user['preferences']['sugar']})")
            context.append(f"Loyalty Points: {user['loyalty_points']}")
            if user['past_orders']:
                last_order = user['past_orders'][0]
                context.append(f"Last Order: {last_order['item']} on {last_order['date']}")
        else:
            context.append("User: Guest (No profile found)")

        if not include_location:
            return "\n".join(context)

        store, dist_deg = self.get_nearest_store(current_lat, current_lon)
        
        found_store = None
        dist_str = "Unknown distance"
        
        if store:
            dist_meters = int(dist_deg * 111000)
            if dist_meters <= 50000: 
                found_store = store
                dist_str = f"{dist_meters}m" if dist_meters < 1000 else f"{dist_meters/1000:.1f}km"
        
        if not found_store and query:
            text_matches = self.find_stores_by_text(query)
            if text_matches:
                found_store = text_matches[0] 
                dist_str = "Distance unknown (found by name)"

        if found_store:
            try:
                city = found_store["location"]["address"].split(",")[-2].strip()
                context.append(f"Inferred City: {city}")
            except:
                pass

            context.append(f"Nearest Store: {found_store['name']} ({dist_str} away)")
            context.append(f"Store Hours: {found_store['hours']['open']} - {found_store['hours']['close']}")
            
            if found_store['offers']:
                offers = ", ".join([f"{o['code']} ({o['description']})" for o in found_store['offers']])
                context.append(f"Active Offers: {offers}")
            else:
                context.append("Active Offers: None")
                
            unavailable = [k for k, v in found_store['stock'].items() if not v]
            if unavailable:
                context.append(f"Out of Stock: {', '.join(unavailable)}")
        else:
             context.append("Nearest Store: None nearby (closest is >50km away and no city mentioned)")
        
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
