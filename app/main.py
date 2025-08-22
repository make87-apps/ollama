import logging

import make87 as m87
from ollama import Client

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def main():
    config = m87.config.load_config_from_env()
    model_name = m87.config.get_config_value(config, "model_name", default=None)
    if model_name is not None:
        logger.info(f"Using model {model_name}")

        logger.info("Setup vpn and model name endpoints")

        logger.info(f"Downloading model {model_name}...")
        client = Client()
        client.pull(model=model_name, stream=False)
        logger.info(f"Model {model_name} downloaded.")

        logger.info("Ollama is ready.")
    else:
        logger.info(f"No model passed. Skipping download.")

    m87.run_forever()


if __name__ == "__main__":
    main()
