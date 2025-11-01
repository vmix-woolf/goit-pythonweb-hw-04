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

    args = parser.parse_args()

    # перевірка існування вихідної папки
    source_path = Path(args.source)
    if not source_path.exists() or not source_path.is_dir():
        logging.error(f"Вихідна папка '{source_path}' не існує або не є директорією.")
        sys.exit(1)

    return args


# --- Точка входу ---
if __name__ == "__main__":
    args = parse_arguments()
    logging.info(f"Отримано аргументи: source={args.source}, output={args.output}")
    print("Step 2: Аргументи успішно оброблено.")

