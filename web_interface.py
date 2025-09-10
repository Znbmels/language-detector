#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Веб-интерфейс для тестирования определения казахского языка
"""

import sys
import os
import json
from datetime import datetime

# Добавляем путь к нашей системе
sys.path.append('langdetect')

try:
    from enhanced_reels_detector import EnhancedReelsDetector
    import langdetect as ld
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    sys.exit(1)

# Импорты для веб-интерфейса
try:
    from flask import Flask, render_template, request, jsonify
except ImportError:
    print("Flask не установлен. Устанавливаем...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Глобальная переменная для детектора
detector = None

def init_detector():
    """Инициализация детектора"""
    global detector
    try:
        detector = EnhancedReelsDetector()
        return True
    except Exception as e:
        print(f"Ошибка инициализации детектора: {e}")
        return False

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_language():
    """API для определения языка"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Текст не может быть пустым'
            })
        
        if not detector:
            return jsonify({
                'success': False,
                'error': 'Детектор не инициализирован'
            })
        
        # Определяем язык
        result = detector.detect_language(text)
        
        # Анализируем тип текста
        text_analysis = analyze_text_type(text)
        
        # Подготавливаем результат
        response = {
            'success': True,
            'text': text,
            'detection': {
                'language': result['language'],
                'language_name': result['language_name'],
                'confidence': round(result['confidence'] * 100, 1),
                'method': result['method'],
                'status': result['status']
            },
            'analysis': text_analysis,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Добавляем альтернативные результаты если есть
        if 'all_results' in result and result['all_results']:
            response['detection']['alternatives'] = [
                {
                    'language': lang,
                    'confidence': round(conf * 100, 1)
                }
                for lang, conf in result['all_results'][:3]
            ]
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def analyze_text_type(text):
    """Анализирует тип текста"""
    analysis = {
        'has_cyrillic_kazakh': False,
        'has_latin_kazakh': False,
        'has_mixed_languages': False,
        'text_length': len(text),
        'word_count': len(text.split()),
        'kazakh_words_found': [],
        'special_chars': []
    }
    
    # Проверяем казахские кириллические символы
    kazakh_cyrillic_chars = set('әқңөұүі')
    found_cyrillic = [char for char in text.lower() if char in kazakh_cyrillic_chars]
    if found_cyrillic:
        analysis['has_cyrillic_kazakh'] = True
        analysis['special_chars'] = list(set(found_cyrillic))
    
    # Проверяем латинские казахские слова
    kazakh_latin_words = {
        'qazaq', 'qazaqstan', 'almaty', 'abay', 'nauryz', 'men', 'sen', 'ol',
        'biz', 'siz', 'olar', 'bolyp', 'zhane', 'menin', 'senin', 'onyng',
        'bizding', 'sizding', 'olardyn', 'tili', 'tiller', 'memeleket', 'qala',
        'khalq', 'el', 'adam', 'zhyl', 'kuni', 'mereke', 'koktem', 'tabighat',
        'super', 'balamyn', 'otanym', 'iri', 'aqyny', 'merekesi', 'keluin'
    }
    
    words = text.lower().split()
    found_latin_words = [word for word in words if word in kazakh_latin_words]
    if found_latin_words:
        analysis['has_latin_kazakh'] = True
        analysis['kazakh_words_found'] = found_latin_words
    
    # Проверяем смешанные языки
    has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in text)
    has_latin = any('a' <= char.lower() <= 'z' for char in text)
    has_kazakh_cyrillic = analysis['has_cyrillic_kazakh']
    has_kazakh_latin = analysis['has_latin_kazakh']
    
    if (has_cyrillic and has_latin) or (has_kazakh_cyrillic and has_kazakh_latin):
        analysis['has_mixed_languages'] = True
    
    return analysis

@app.route('/stats')
def get_stats():
    """Получение статистики"""
    try:
        # Здесь можно добавить логику для подсчета статистики
        # Пока возвращаем базовую информацию
        stats = {
            'supported_languages': 24,
            'kazakh_support': True,
            'latin_kazakh_support': True,
            'detector_status': 'active' if detector else 'inactive'
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 Запуск веб-интерфейса для определения казахского языка...")
    
    # Инициализируем детектор
    if init_detector():
        print("✅ Детектор инициализирован")
    else:
        print("❌ Ошибка инициализации детектора")
        sys.exit(1)
    
    print("🌐 Веб-интерфейс доступен по адресу: http://localhost:8080")
    print("📝 Вставьте текст на казахском языке и нажмите 'Проверить'")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
