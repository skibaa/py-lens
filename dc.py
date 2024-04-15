from dataclasses import dataclass

@dataclass(frozen=True)
class Exchange:
    name: str
    location: str

# Example usage
nyse = Exchange(name="New York Stock Exchange", location="New York, USA")

# Attempting to modify the instance will raise an error
try:
    nyse.name = "NASDAQ"
except AttributeError as e:
    print(e)  # Prints an error message because the dataclass is frozen

# Using replace to create a modified instance
from dataclasses import replace
nyse_updated = replace(nyse, name="NASDAQ")
print(nyse_updated)
