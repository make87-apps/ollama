import json
import logging
import os
from datetime import datetime, timezone

from make87_messages.core.empty_pb2 import Empty
from make87_messages.core.header_pb2 import Header
from make87_messages.image.compressed.image_jpeg_with_string_pb2 import ImageJPEGWithString
from make87_messages.text.text_plain_pb2 import PlainText
from make87_messages.image.compressed.image_jpeg_pb2 import ImageJPEG
import make87
from ollama import chat, Client, ChatResponse, Message, Image

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

def main():
    make87.initialize()

    model_name = make87.get_config_value("MODEL_NAME", "moondream", str)
    logger.info(f"Using model {model_name}")
    vpn_ip = os.environ.get("VPN_IP", None)
    if vpn_ip is None:
        raise Exception("No VPN IP found")
    port_config = os.environ.get("PORT_CONFIG", None)
    if port_config is None:
        raise Exception("No port config found")
    vpn_server_url = None
    if port_config is not None:
        # search for OLLAMA and get public port
        port_config = json.loads(port_config)
        for port_config in port_config:
            if port_config["name"] == "OLLAMA":
                port = port_config["published_port"]
                vpn_server_url = f"http://{vpn_ip}:{port}"
                break

    vpn_url_endpoint = make87.get_provider(
        name="VPN_SERVER_URL", requester_message_type=Empty, provider_message_type=PlainText
    )
    def callback_vpn_url(message: Empty) -> PlainText:
        return PlainText(
            header=make87.header_from_message(Header, message=message, append_entity_path="response"),
            body=vpn_server_url,
        )

    vpn_url_endpoint.provide(callback_vpn_url)

    local_url_endpoint = make87.get_provider(
        name="LOCAL_SERVER_URL", requester_message_type=Empty, provider_message_type=PlainText
    )
    def callback_local_url(message: Empty) -> PlainText:
        local_address = f"http://{make87.DEPLOYED_APPLICATION_NAME}:11434"

        return PlainText(
            header=make87.header_from_message(Header, message=message, append_entity_path="response"),
            body=local_address,
        )

    local_url_endpoint.provide(callback_local_url)

    model_name_endpoint = make87.get_provider(
        name="MODEL_NAME", requester_message_type=Empty, provider_message_type=PlainText
    )
    def callback_model_name(message: Empty) -> PlainText:
        return PlainText(
            header=make87.header_from_message(Header, message=message, append_entity_path="response"),
            body=model_name,
        )
    model_name_endpoint.provide(callback_model_name)
    logger.info("Setup vpn and model name endpoints")

    logger.info(f"Downloading model {model_name}...")
    client = Client()
    client.pull(model=model_name, stream=False)
    logger.info(f"Model {model_name} downloaded.")

    endpoint = make87.get_provider(
        name="CHAT", requester_message_type=PlainText, provider_message_type=PlainText
    )

    def callback(message: PlainText) -> PlainText:
        response: ChatResponse = chat(model=model_name, messages=[
            Message(
                role="user",
                content=message.body,
            )
        ])
        return PlainText(
            header=make87.header_from_message(Header, message=message, append_entity_path="response"),
            body=response.message.content,
        )

    endpoint.provide(callback)

    endpoint = make87.get_provider(
        name="IMG_CHAT", requester_message_type=ImageJPEGWithString, provider_message_type=PlainText
    )

    def callback_img(message: ImageJPEGWithString) -> PlainText:
        response: ChatResponse = chat(model=model_name, messages=[
            Message(
                role="user",
                images=[Image(value=message.data)],
                content=message.text,
            )
        ])
        return PlainText(
            header=make87.header_from_message(Header, message=message, append_entity_path="response"),
            body=response.message.content,
        )

    endpoint.provide(callback_img)

    logger.info("Setup chat endpoints")
    logger.info("Ollama is ready.")

    make87.loop()


if __name__ == "__main__":
    main()
