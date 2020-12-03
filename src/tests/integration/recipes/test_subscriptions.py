import pytest


@pytest.mark.asyncio
async def test_hello_world(websocket_communicator, execute_websocket_query):
    subscription = """
        subscription {
            hello
        }
    """

    await execute_websocket_query(subscription)

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {"data": {"hello": "hello world!"}, "errors": None}
