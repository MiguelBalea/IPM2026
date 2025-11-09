import requests
from requests import RequestException
from typing import Any, Dict, List

# URL base por defecto; puedes cambiarla al instanciar Model(base_url="...")
SERVER_URL = "http://127.0.0.1:8000"

class ApiError(Exception):
    """Error al comunicarse con la API."""
    pass

class Model:
    def __init__(self, base_url: str = SERVER_URL, timeout: int = 5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def health_check(self) -> bool:
        """
        Comprueba si el servidor responde. Usa /docs porque FastAPI expone esa ruta por defecto.
        Devuelve True si recibe 200, False en caso contrario o si hay excepción de red.
        """
        try:
            resp = self.session.get(self._url("/docs"), timeout=self.timeout)
            return resp.status_code == 200
        except RequestException:
            return False

    def get_friends(self) -> List[Dict[str, Any]]:
        """GET /friends -> lista de amigos"""
        try:
            resp = self.session.get(self._url("/friends"), timeout=self.timeout)
        except RequestException as e:
            raise ApiError(f"Error de conexión al obtener friends: {e}") from e

        if resp.status_code == 200:
            try:
                return resp.json()
            except ValueError:
                raise ApiError("Respuesta no JSON al obtener friends")
        else:
            raise ApiError(f"GET /friends -> HTTP {resp.status_code}: {resp.text}")

    def add_friend(self, name: str) -> Dict[str, Any]:
        """POST /friends { name } -> friend creado"""
        payload = {"name": name}
        try:
            resp = self.session.post(self._url("/friends"), json=payload, timeout=self.timeout)
        except RequestException as e:
            raise ApiError(f"Error de conexión al crear friend: {e}") from e

        if resp.status_code == 201:
            try:
                return resp.json()
            except ValueError:
                raise ApiError("Respuesta no JSON al crear friend")
        elif resp.status_code == 409:
            raise ApiError("El friend ya existe (409)")
        else:
            raise ApiError(f"POST /friends -> HTTP {resp.status_code}: {resp.text}")

    def get_expenses(self) -> List[Dict[str, Any]]:
        """GET /expenses -> lista de gastos"""
        try:
            resp = self.session.get(self._url("/expenses"), timeout=self.timeout)
        except RequestException as e:
            raise ApiError(f"Error de conexión al obtener expenses: {e}") from e

        if resp.status_code == 200:
            try:
                return resp.json()
            except ValueError:
                raise ApiError("Respuesta no JSON al obtener expenses")
        else:
            raise ApiError(f"GET /expenses -> HTTP {resp.status_code}: {resp.text}")

    def add_expense(self, description: str, date: str, amount: float) -> Dict[str, Any]:
        """POST /expenses -> crea un gasto"""
        payload = {"description": description, "date": date, "amount": amount}
        try:
            resp = self.session.post(self._url("/expenses"), json=payload, timeout=self.timeout)
        except RequestException as e:
            raise ApiError(f"Error de conexión al crear expense: {e}") from e

        if resp.status_code in (200, 201):
            try:
                return resp.json()
            except ValueError:
                raise ApiError("Respuesta no JSON al crear expense")
        else:
            raise ApiError(f"POST /expenses -> HTTP {resp.status_code}: {resp.text}")

    def close(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass