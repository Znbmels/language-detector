#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import re
from bs4 import BeautifulSoup
import time

def clean_text(text):
    """Очистка текста от лишних символов и форматирования"""
    # Удаляем HTML теги
    text = re.sub(r'<[^>]+>', '', text)
    # Удаляем лишние пробелы и переносы строк
    text = re.sub(r'\s+', ' ', text)
    # Удаляем специальные символы, оставляя только буквы, цифры и знаки препинания
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\"\']+', '', text, flags=re.UNICODE)
    return text.strip()

def has_kazakh_chars(text):
    """Проверяет, содержит ли текст казахские буквы"""
    kazakh_chars = set('әқңөұүі')
    return any(char in text.lower() for char in kazakh_chars)

def get_wikipedia_articles():
    """Получает статьи с казахской Википедии"""
    articles = []
    
    # Список популярных статей на казахском языке
    article_titles = [
        "Қазақстан",
        "Алматы", 
        "Нұр-Сұлтан",
        "Абай_Құнанбайұлы",
        "Мұхтар_Әуезов",
        "Қазақ_тілі",
        "Қазақ_әдебиеті",
        "Балқаш_көлі",
        "Арал_теңізі",
        "Каспий_теңізі",
        "Тянь-Шань",
        "Алтай_тауы",
        "Қазақ_хандығы",
        "Назарбаев_Нұрсұлтан",
        "Тоқаев_Қасым-Жомарт",
        "Қазақстан_тарихы",
        "Қазақ_мәдениеті",
        "Қазақ_музыкасы",
        "Домбыра",
        "Наурыз"
    ]
    
    for title in article_titles:
        try:
            url = f"https://kk.wikipedia.org/wiki/{title}"
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Находим основной контент статьи
                content_div = soup.find('div', {'id': 'mw-content-text'})
                if content_div:
                    # Удаляем навигационные блоки, таблицы и другие элементы
                    for element in content_div.find_all(['table', 'div', 'span'], 
                                                       class_=['navbox', 'infobox', 'toc', 'references']):
                        element.decompose()
                    
                    # Извлекаем текст из параграфов
                    paragraphs = content_div.find_all('p')
                    text = ' '.join([p.get_text() for p in paragraphs])
                    
                    # Очищаем текст
                    cleaned_text = clean_text(text)
                    
                    # Проверяем, что текст содержит казахские символы и достаточно длинный
                    if has_kazakh_chars(cleaned_text) and len(cleaned_text) > 500:
                        articles.append(cleaned_text)
                        print(f"Собрана статья: {title} ({len(cleaned_text)} символов)")
                    
            time.sleep(1)  # Пауза между запросами
            
        except Exception as e:
            print(f"Ошибка при получении статьи {title}: {e}")
            continue
    
    return articles

def create_sample_texts():
    """Создает образцы казахских текстов"""
    sample_texts = [
        """
        Қазақстан Республикасы — Орталық Азия мен Шығыс Еуропада орналасқан мемлекет. 
        Астанасы — Нұр-Сұлтан қаласы. Ең ірі қаласы — Алматы. Қазақстан аумағы бойынша 
        әлемдегі тоғызыншы ірі ел. Халқы 19 миллионнан астам адам. Мемлекеттік тілі — қазақ тілі, 
        ресми тіл — орыс тілі. Қазақстан көп ұлтты мемлекет болып табылады.
        """,
        
        """
        Абай Құнанбайұлы — қазақтың ұлы ақыны, ағартушысы, композиторы, философы және аудармашысы. 
        Ол қазақ әдебиетінің классигі болып саналады. Абайдың шығармалары қазақ халқының рухани 
        мұрасының бір бөлігі. Оның "Қара сөздері" қазақ философиясының маңызды дереккөзі болып табылады. 
        Абай қазақ жазба әдебиетінің негізін қалаушылардың бірі.
        """,
        
        """
        Қазақ тілі — түркі тілдер тобына жататын тіл. Қазақстан Республикасының мемлекеттік тілі. 
        Қазақ тілінде сөйлейтін адамдар саны 12 миллионнан астам. Қазақ тілі кириллица әрпімен жазылады, 
        бірақ латын әрпіне көшу жоспарланып отыр. Қазақ тілінің өзіндік ерекшеліктері бар: 
        дауысты дыбыстардың үйлесімі, септік жүйесі, етістіктің күрделі түрлену жүйесі.
        """,
        
        """
        Алматы — Қазақстанның ең ірі қаласы және бұрынғы астанасы. Қала Іле Алатауының етегінде орналасқан. 
        Алматы Қазақстанның мәдени, ғылыми және экономикалық орталығы болып табылады. Қалада көптеген 
        университеттер, театрлар, мұражайлар орналасқан. Алматы "Алма-Ата" деп те аталады, 
        бұл "алма атасы" дегенді білдіреді.
        """,
        
        """
        Наурыз — қазақтардың ұлттық мерекесі, жаңа жыл мерекесі. Наурыз 22 наурызда тойланады. 
        Бұл мереке көктемнің келуін, табиғаттың жаңаруын білдіреді. Наурыз күні қазақтар наурыз көже 
        дайындайды, бұл жеті түрлі дәннен жасалған тағам. Наурыз мерекесі барлық Орталық Азия 
        халықтарында тойланады.
        """
    ]
    
    return [clean_text(text) for text in sample_texts]

def main():
    """Основная функция для сбора казахских текстов"""
    output_dir = "langdetect/datasets/train/kk"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Начинаем сбор казахских текстов...")
    
    # Сначала создаем образцы текстов
    sample_texts = create_sample_texts()
    
    # Пытаемся получить статьи с Википедии
    try:
        wiki_articles = get_wikipedia_articles()
        all_texts = sample_texts + wiki_articles
    except Exception as e:
        print(f"Ошибка при получении статей с Википедии: {e}")
        print("Используем только образцы текстов")
        all_texts = sample_texts
    
    # Сохраняем тексты в файлы
    total_size = 0
    for i, text in enumerate(all_texts, 1):
        filename = os.path.join(output_dir, f"{i}-kk.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            
            file_size = len(text.encode('utf-8'))
            total_size += file_size
            print(f"Сохранен файл: {filename} ({file_size} байт)")
            
        except Exception as e:
            print(f"Ошибка при сохранении файла {filename}: {e}")
    
    print(f"\nВсего собрано: {len(all_texts)} файлов")
    print(f"Общий размер: {total_size} байт ({total_size/1024:.1f} KB)")
    
    if total_size < 100000:  # 100KB
        print("ВНИМАНИЕ: Размер корпуса меньше рекомендуемого (100KB)")
        print("Рекомендуется добавить больше текстов для лучшего качества определения языка")

if __name__ == "__main__":
    main()
