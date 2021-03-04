import pytest
from pydantic.dataclasses import dataclass
from quart import Quart

from quart_schema import QuartSchema, validate_request, validate_response


@dataclass
class Data:
    snake_case: str


@pytest.mark.asyncio
async def test_request_casing() -> None:
    app = Quart(__name__)
    QuartSchema(app, convert_casing=True)

    @app.route("/", methods=["POST"])
    @validate_request(Data)  # type: ignore
    async def index(data: Data) -> str:
        return repr(data)

    test_client = app.test_client()
    response = await test_client.post("/", json={"snakeCase": "Hello"})
    assert await response.get_data(raw=False) == "Data(snake_case='Hello')"


@pytest.mark.asyncio
async def test_response_casing() -> None:
    app = Quart(__name__)
    QuartSchema(app, convert_casing=True)

    @app.route("/", methods=["GET"])
    @validate_response(Data)  # type: ignore
    async def index() -> Data:
        return Data(snake_case="Hello")

    test_client = app.test_client()
    response = await test_client.get("/")
    assert await response.get_data(raw=False) == '{"snakeCase":"Hello"}'