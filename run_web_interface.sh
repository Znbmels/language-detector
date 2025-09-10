#!/bin/bash

echo "🚀 Запуск веб-интерфейса для определения казахского языка"
echo "=" * 60

# Проверяем наличие виртуального окружения
if [ ! -d "web_env" ]; then
    echo "📦 Создаем виртуальное окружение..."
    python3 -m venv web_env
fi

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source web_env/bin/activate

# Устанавливаем зависимости если нужно
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Устанавливаем Flask..."
    pip install flask
fi

# Проверяем наличие необходимых файлов
required_files=("web_interface.py" "templates/index.html" "enhanced_reels_detector.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Файл $file не найден!"
        exit 1
    fi
    echo "✅ $file найден"
done

echo ""
echo "🌐 Запускаем веб-интерфейс..."
echo "📝 Откройте браузер и перейдите по адресу: http://localhost:8080"
echo "🛑 Для остановки нажмите Ctrl+C"
echo "=" * 60

# Запускаем веб-интерфейс
python3 web_interface.py
