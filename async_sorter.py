import asyncio
import aiofiles
import aiofiles.os
import aiofiles.ospath
import argparse
import logging
from pathlib import Path
import sys


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


# --- Асинхронна ініціалізація шляхів ---
async def init_paths(source: str, output: str) -> tuple[Path, Path]:
    """Перевіряє шляхи та створює вихідну папку, якщо її немає."""
    source_path = Path(source)
    output_path = Path(output)

    # Перевірка існування вихідної папки
    if not await aiofiles.ospath.exists(source_path):
        logging.error(f"Вихідна папка '{source_path}' не існує або не є директорією.")
        sys.exit(1)

    # Створюємо вихідну папку, якщо її немає
    if not await aiofiles.ospath.exists(output_path):
        await aiofiles.os.mkdir(output_path)
        logging.info(f"Цільова папка '{output_path}' створена.")

    return source_path, output_path


# --- Головна асинхронна функція ---
async def main():
    args = parse_arguments()
    source_path, output_path = await init_paths(args.source, args.output)
    logging.info(f"Шляхи ініціалізовано: source={source_path}, output={output_path}")
    print("Step 3: Шляхи успішно ініціалізовано.")


if __name__ == "__main__":
    asyncio.run(main())
