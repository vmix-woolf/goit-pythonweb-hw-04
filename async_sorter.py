import asyncio
import aiofiles
import aiofiles.os
import aiofiles.ospath
import argparse
import logging
from pathlib import Path
import sys
import os


log_file = Path(__file__).parent / "sorter.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logging.info("Логування ініціалізовано успішно.")


def parse_arguments():
    """Парсить аргументи командного рядка."""
    parser = argparse.ArgumentParser(
        description="Асинхронне сортування файлів за розширенням."
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Шлях до вихідної папки, яку потрібно відсортувати."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Шлях до цільової папки, куди будуть скопійовані файли."
    )
    return parser.parse_args()


async def init_paths(source: str, output: str) -> tuple[Path, Path]:
    """Перевіряє шляхи та створює вихідну папку, якщо її немає."""
    source_path = Path(source)
    output_path = Path(output)

    if not await aiofiles.ospath.exists(source_path):
        logging.error(f"Вихідна папка '{source_path}' не існує або не є директорією.")
        sys.exit(1)

    if not await aiofiles.ospath.exists(output_path):
        await aiofiles.os.mkdir(output_path)
        logging.info(f"Цільова папка '{output_path}' створена.")

    return source_path, output_path


# --- Асинхронна функція для обходу директорії ---
async def read_folder(source: Path, output: Path):
    tasks = []
    entries = await asyncio.to_thread(lambda: list(os.scandir(source)))

    for entry in entries:
        if entry.is_dir():
            sub_source = source / entry.name
            await read_folder(sub_source, output)
        else:
            file_path = source / entry.name
            tasks.append(asyncio.create_task(copy_file(file_path, output)))

    if tasks:
        await asyncio.gather(*tasks)

async def copy_file(file_path: Path, output_dir: Path):
    try:
        ext = file_path.suffix.lower().lstrip(".") or "no_ext"
        target_folder = output_dir / ext

        if not await aiofiles.ospath.exists(target_folder):
            await aiofiles.os.mkdir(target_folder)

        target_path = target_folder / file_path.name

        async with aiofiles.open(file_path, "rb") as src, aiofiles.open(target_path, "wb") as dst:
            while chunk := await src.read(1024 * 64):
                await dst.write(chunk)

        logging.info(f"Файл '{file_path.name}' скопійовано до '{target_folder}'.")
    except Exception as e:
        logging.error(f"Помилка копіювання файлу '{file_path}': {e}", exc_info=True)


async def main():
    args = parse_arguments()
    source_path, output_path = await init_paths(args.source, args.output)
    await read_folder(source_path, output_path)
    print("Step 5: Асинхронне копіювання файлів завершено.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
        sys.exit(0)
    except Exception as e:
        logging.exception(f"Непередбачена помилка виконання: {e}")
        sys.exit(1)
