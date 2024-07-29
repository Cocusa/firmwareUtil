Для сборки проекта используется команды:
ОТК - "pyinstaller --onefile --windowed main.py --name 111 --version-file ./version.rc", 
Обновление - "pyinstaller --onefile --windowed util_update.py --name 11"

Подготовка виртуальной среды и устновка зависимостей:
1. python -m venv firmware-util-venv
2. .\firmware-util-venv\Scripts\activate
3. pip install -r requirements.txt