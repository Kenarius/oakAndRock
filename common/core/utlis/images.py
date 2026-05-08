import asyncio
from functools import wraps

import httpx
import uuid
from fastapi import UploadFile

YANDEX_DISK_API_URL = "https://cloud-api.yandex.net/v1/disk/resources"
YANDEX_DISK_TOKEN = "y0__wgBEMC74K4DGNaxQSCb7ZmsF5lXxEAksQylgupNga9-G3wpeoTu"
headers = {"Authorization": f"OAuth {YANDEX_DISK_TOKEN}"}


def with_retry(max_retries=3, delay=1):
    """Декоратор для retry с backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except RuntimeError as e:
                    last_exc = e
                    if "InternalServerError" in str(e) and attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
                        continue
                    raise
            raise last_exc or RuntimeError("Max retries exceeded")
        return wrapper
    return decorator


@with_retry(max_retries=3, delay=1)
async def publish_file(disk_path: str):
    """Публикация с retry только для InternalServerError"""
    async with httpx.AsyncClient() as client:
        # Инициация
        init_resp = await client.put(f"{YANDEX_DISK_API_URL}/publish",
                                     headers=headers, params={"path": disk_path})
        if init_resp.status_code != 200:
            init_resp.raise_for_status()  # Поднимает точную ошибку

        href = init_resp.json()["href"]
        # Активация
        final_resp = await client.get(href, headers=headers)
        final_resp.raise_for_status()

        public_data = final_resp.json()
        if "public_url" not in public_data:
            raise RuntimeError(f"No public_url: {public_data}")

        return public_data

async def ensure_folder_exists(folder_path: str) -> None:
    """
    Проверяет существование папки, создаёт если нет (рекурсивно).
    folder_path: например "/app/blog"
    """
    params = {"path": folder_path, "fields": ""}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{YANDEX_DISK_API_URL}", headers=headers, params=params)

    if resp.status_code == 404:
        # Создаём папку (PUT создаёт рекурсивно)
        async with httpx.AsyncClient(timeout=30.0) as client:
            create_resp = await client.put(
                f"{YANDEX_DISK_API_URL}",
                headers=headers,
                params={"path": folder_path}
            )
            create_resp.raise_for_status()
    elif resp.status_code != 200:
        raise RuntimeError(f"Ошибка проверки папки {folder_path}: {resp.text}")


async def upload_file_to_disk(file: UploadFile, name: str, folder: str = "blog") -> str:
    folder_path = f"/app/{folder}"
    await ensure_folder_exists(folder_path)

    filename = f"{name}.{uuid.uuid4().hex[:8]}"
    disk_path = f"{folder_path}/{filename}"

    # Шаг 1-2: Upload (как раньше)
    params = {"path": disk_path, "overwrite": "true"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{YANDEX_DISK_API_URL}/upload", headers=headers, params=params)
        data = resp.json()
        if "href" not in data:
            raise RuntimeError(f"Upload URL failed: {data}")

        file.file.seek(0)
        upload_resp = await client.put(data["href"], content=await file.read())
        upload_resp.raise_for_status()

    # Шаг 3: Publish — двухэтапный процесс!
    public_data = await publish_file(disk_path)
    # После получения public_data с "public_url" и "public_key":
    public_key = public_data["public_key"]  # "6RWgHAgkTjbwRjS0..." из вашего лога

    # Шаг 4: Получить ПРЯМУЮ ссылку для <img src>
    async with httpx.AsyncClient(timeout=30.0) as client:
        download_resp = await client.get(
            "https://cloud-api.yandex.net/v1/disk/public/resources/download",
            headers=headers,  # Токен нужен!
            params={"public_key": public_key}
        )
        if download_resp.status_code != 200:
            raise RuntimeError(f"Direct link failed: {download_resp.text}")

        direct_data = download_resp.json()
        print(f"direct response: {direct_data}")
        if "href" not in direct_data:
            raise RuntimeError(f"No direct href: {direct_data}")

    direct_url = direct_data["href"]  # https://downloader.disk.yandex.ru/disk/...&media_type=image
    return direct_url
