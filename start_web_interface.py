#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Простой запуск веб-интерфейса для определения казахского языка
"""

import sys
import os
import subprocess

def check_dependencies():
    """Проверяет зависимости"""
    try:
        import flask
        print("✅ Flask установлен")
        return True
    except ImportError:
        print("❌ Flask не установлен")
        return False

def install_flask():
    """Устанавливает Flask"""
    print("📦 Устанавливаем Flask...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("✅ Flask установлен успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка установки Flask: {e}")
        return False

def main():
    """Главная функция"""
    print("🚀 Запуск веб-интерфейса для определения казахского языка")
    print("=" * 60)
    
    # Проверяем зависимости
    if not check_dependencies():
        if not install_flask():
            print("❌ Не удалось установить Flask")
            return
    
    # Проверяем наличие необходимых файлов
    required_files = [
        'web_interface.py',
        'templates/index.html',
        'enhanced_reels_detector.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Файл {file} не найден")
            return
        else:
            print(f"✅ {file} найден")
    
    print("\n🌐 Запускаем веб-сервер...")
    print("📝 Откройте браузер и перейдите по адресу: http://localhost:5000")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("-" * 60)
    
    try:
        # Запускаем веб-интерфейс
        from web_interface import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Веб-интерфейс остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
