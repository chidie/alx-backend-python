def build_thread(message):
    return {
        "id": message.id,
        "sender": message.sender.email,
        "body": message.message_body,
        "timestamp": message.timestamp,
        "replies": [build_thread(reply) for reply in message.replies.all()]
    }
