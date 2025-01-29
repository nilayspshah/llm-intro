import openai
import logging
import configparser

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

# Function to initialize the OpenAI API client
def initialize_openai(api_key):
    openai.api_key = api_key
    logger.info('OpenAI API client initialized.')

# Function to create a chat completion using OpenAI API
def create_chat_completion_hallucination_math(model='gpt-3.5-turbo', max_tokens=100):
    try:
        logger.info('Creating chat completion with model: %s', model)
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant"},
                {"role": "user", "content": "What is 123,456 × 789,012 "}
            ],
            max_tokens=max_tokens,
            temperature=1
        )
        logger.info('Chat completion created successfully.')
        logger.info('response: %s', response)
        return response.choices[0].message
    except Exception as e:
        logger.error('Error creating chat completion: %s', e)


# Main function to demonstrate the usage of the OpenAI API
def main():
    api_key = get_api_key()
    initialize_openai(api_key)
    completion = create_chat_completion_hallucination_math()
    if completion:
        logger.info('Completion received: %s', completion)
    else:
        logger.error('Failed to receive a completion.')

if __name__ == "__main__":
    main()