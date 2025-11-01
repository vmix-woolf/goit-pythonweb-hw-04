import asyncio
import aiofiles
import aiofiles.os
import aiofiles.ospath
import argparse
import logging
from pathlib import Path
import sys
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
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
    """Рекурсивно обходить усі файли у вихідній папці."""
    tasks = []

    # Викликаємо os.scandir у окремому потоці
    entries = await asyncio.to_thread(lambda: list(os.scandir(source)))

    for entry in entries:
        if entry.is_dir():
            sub_source = source / entry.name
            await read_folder(sub_source, output)
        else:
            logging.info(f"Знайдено файл: {entry.name}")

    if tasks:
        await asyncio.gather(*tasks)


async def main():
    args = parse_arguments()
    source_path, output_path = await init_paths(args.source, args.output)
    await read_folder(source_path, output_path)
    print("Step 4: Читання вихідної папки завершено.")


if __name__ == "__main__":
    asyncio.run(main())
