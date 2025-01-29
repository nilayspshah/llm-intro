import configparser
import logging
from typing import List

from openai import OpenAI
from pydantic import BaseModel

class IndividualAnimalName(BaseModel):
    animal_name: str


# Define the output structure using Pydantic
class IdentifiedAnimalsResponse(BaseModel):
    individual_instruments: List[IndividualAnimalName]


# Setup logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)

# Read the configuration file to get API key
def get_api_key(config_file='config/config.ini'):
    config = configparser.RawConfigParser()
    config.read(config_file)
    return config['openai']['api_key']


def get_animals_from_text() -> IdentifiedAnimalsResponse:
    # Initialize OpenAI client
    client = OpenAI(
        api_key=get_api_key())

    # gpt-4o-mini-2024-07-18
    # gpt-4o-mini-2024-07-18
    # Call OpenAI API
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system",
             "content": "You are a wildlife expert with knowledge about animals"},
            {"role": "user",
             "content": "Identity list of creatures from the following text: In the heart of the Amazon rainforest, a jaguar prowled silently through the underbrush, its eyes keenly scanning for prey. Above, a colorful macaw screeched as it soared through the canopy, searching for ripe fruit. Nearby, a shy sloth moved ever so slowly, blending perfectly with the moss-covered trees. On the forest floor, a python slithered smoothly, its scales glistening in the dappled sunlight. In a clearing, a tapir nibbled on some lush vegetation, while a curious capuchin monkey chattered excitedly, swinging from branch to branch. The forest was alive with sounds, from the chirping of crickets to the distant call of a toucan. As dusk approached, the symphony of the rainforest grew louder, a reminder of the vibrant life teeming within its depths."}
        ],
        response_format=IdentifiedAnimalsResponse,
    )
    message = completion.choices[0].message
    if message.parsed:
        for i in message.parsed.individual_instruments:
            print(i)
        return message
    else:
        raise ValueError("Could not identify Companies")


# Example usage
if __name__ == "__main__":
    try:
        get_animals_from_text()
    except Exception as e:
        print(f"Error: {str(e)}")