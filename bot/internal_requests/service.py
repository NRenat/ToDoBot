from config import INTERNAL_API_URL
from httpx import AsyncClient, Response
from urllib.parse import urljoin


class APIService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None

    async def create_user(self, tg_id):
        data = {"telegram_id": tg_id}
        response = await self._post_request('users/', data)
        return response

    async def close_task(self, task_id):
        data = {
            'completed': True
        }
        response = await self._patch_request(f'tasks/{task_id}/', data)
        return response

    async def get_task_details(self, task_id: str):
        response = await self._get_request(f'tasks/?id={task_id}')
        return response.json()[0]

    async def get_tasks(self, telegram_id: str):
        response = await self._get_request(
            f'tasks/?author={telegram_id}&completed=False')
        return response.json()

    async def create_task(self, task: dict):
        response = await self._post_request('tasks/', task)
        return response.json()

    async def _get_request(self, url: str) -> Response:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        async with AsyncClient() as client:
            response = await client.get(
                urljoin(base=self.base_url, url=url), headers=headers
            )
            return response

    async def _post_request(self, url: str, data: dict) -> Response:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        async with AsyncClient() as client:
            response = await client.post(
                urljoin(base=self.base_url, url=url), json=data, headers=headers
            )
            return response

    async def _patch_request(self, url: str, data: dict) -> Response:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        async with AsyncClient() as client:
            response = await client.patch(
                urljoin(base=self.base_url, url=url), json=data, headers=headers
            )
            return response

    async def _delete_request(self, url: str) -> Response:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        async with AsyncClient() as client:
            response = await client.delete(
                urljoin(base=self.base_url, url=url), headers=headers
            )
        return response

    async def authenticate(self, username: str, password: str):
        data = {"username": username, "password": password}
        response = await self._post_request('token/', data)
        tokens = response.json()
        self.token = tokens.get('access')
        return tokens


api_service = APIService(base_url=INTERNAL_API_URL)
