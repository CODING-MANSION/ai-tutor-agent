# app/tools/constants.py

import json

# Using a simple dictionary as our data source. This could be a JSON file or a database.
PHYSICS_CONSTANTS = {
    "speed of light": {"value": 299792458, "unit": "m/s", "symbol": "c"},
    "gravitational constant": {"value": 6.67430e-11, "unit": "m^3 kg^-1 s^-2", "symbol": "G"},
    "planck constant": {"value": 6.62607015e-34, "unit": "J s", "symbol": "h"},
    "boltzmann constant": {"value": 1.380649e-23, "unit": "J/K", "symbol": "k_B"}
}

def lookup_physics_constant(constant_name: str) -> str:
    """
    Looks up the value, unit, and symbol of a physical constant.
    
    Args:
        constant_name (str): The name of the constant to look up. 
                             e.g., "speed of light", "planck constant"
                             
    Returns:
        str: A JSON string containing the constant's data or an error message.
    """
    # Normalize the input to be case-insensitive and handle minor variations
    normalized_name = constant_name.lower().strip()
    
    constant_data = PHYSICS_CONSTANTS.get(normalized_name)
    
    if constant_data:
        return json.dumps(constant_data)
    else:
        return json.dumps({"error": f"Constant '{constant_name}' not found."})

# Example of how the tool can be used:
if __name__ == '__main__':
    print(lookup_physics_constant("Speed of Light"))
    print(lookup_physics_constant("Avogadro's Number"))