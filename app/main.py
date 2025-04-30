import logging
from datetime import datetime, timezone

from make87_messages.core.header_pb2 import Header
from make87_messages.text.text_plain_pb2 import PlainText
from make87_messages.image.compressed.image_jpeg_pb2 import ImageJPEG
import make87
from ollama import chat, Client, ChatResponse, Message, Image


def main():
    make87.initialize()

    model_name = make87.get_config_value("MODEL_NAME", "moondream", str)
    logging.info(f"Downloading model {model_name}...")

    client = Client()
    client.pull(model=model_name, stream=False)
    logging.info(f"Model {model_name} downloaded.")

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
        name="IMG_CHAT", requester_message_type=ImageJPEG, provider_message_type=PlainText
    )

    def callback_img(message: ImageJPEG) -> PlainText:
        response: ChatResponse = chat(model=model_name, messages=[
            Message(
                role="user",
                images=[Image(value=message.data)],
            )
        ])
        return PlainText(
            header=make87.header_from_message(Header, message=message, append_entity_path="response"),
            body=response.message.content,
        )

    endpoint.provide(callback_img)

    make87.loop()


if __name__ == "__main__":
    main()
