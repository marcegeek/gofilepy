import io

from requests import Response
from urllib3 import HTTPResponse


class ResponseIO:
    def __init__(self, resp: Response) -> None:
        self._resp = resp
        self._file: HTTPResponse | io.BytesIO
        if not self._resp.raw.closed:
            self._file = self._resp.raw
        else:
            # if raw object is closed assume stream=False and create a BytesIO buffer with the content
            self._file = io.BytesIO(self._resp.content)

    @property
    def status_code(self) -> int:
        return self._resp.status_code

    def read(self, amount: int | None = None) -> bytes:
        if isinstance(self._file, HTTPResponse):
            return self._file.read(amount, decode_content=True)
        else:
            return self._file.read(amount)

    def close(self) -> None:
        # close response to close the raw object if necessary and release the connection
        self._resp.close()
        if isinstance(self._file, io.BytesIO):
            # close the BytesIO buffer if created
            self._file.close()

    @property
    def closed(self) -> bool:
        return self._file.closed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # don't supress exceptions
        return False
