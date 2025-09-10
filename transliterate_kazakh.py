#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Транслитерация казахского языка: кириллица ↔ латиница
"""

def cyrillic_to_latin(text):
    """Конвертирует кириллический казахский в латинский"""
    
    # Словарь транслитерации
    translit_dict = {
        'а': 'a', 'ә': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ғ': 'g',
        'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'қ': 'q', 'л': 'l', 'м': 'm', 'н': 'n',
        'ң': 'n', 'о': 'o', 'ө': 'o', 'п': 'p', 'р': 'r', 'с': 's',
        'т': 't', 'у': 'u', 'ұ': 'u', 'ү': 'u', 'ф': 'f', 'х': 'h',
        'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y',
        'і': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        
        # Заглавные буквы
        'А': 'A', 'Ә': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Ғ': 'G',
        'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Қ': 'Q', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'Ң': 'N', 'О': 'O', 'Ө': 'O', 'П': 'P', 'Р': 'R', 'С': 'S',
        'Т': 'T', 'У': 'U', 'Ұ': 'U', 'Ү': 'U', 'Ф': 'F', 'Х': 'H',
        'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y',
        'І': 'I', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    
    result = ""
    for char in text:
        if char in translit_dict:
            result += translit_dict[char]
        else:
            result += char
    
    return result

def latin_to_cyrillic(text):
    """Конвертирует латинский казахский в кириллический"""
    
    # Словарь обратной транслитерации
    reverse_dict = {
        'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е',
        'zh': 'ж', 'z': 'з', 'i': 'и', 'y': 'й', 'k': 'к', 'q': 'қ',
        'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р',
        's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'ts': 'ц',
        'ch': 'ч', 'sh': 'ш', 'shch': 'щ', 'yo': 'ё', 'yu': 'ю', 'ya': 'я',
        
        # Заглавные буквы
        'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е',
        'Zh': 'Ж', 'Z': 'З', 'I': 'И', 'Y': 'Й', 'K': 'К', 'Q': 'Қ',
        'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р',
        'S': 'С', 'T': 'Т', 'U': 'У', 'F': 'Ф', 'H': 'Х', 'Ts': 'Ц',
        'Ch': 'Ч', 'Sh': 'Ш', 'Shch': 'Щ', 'Yo': 'Ё', 'Yu': 'Ю', 'Ya': 'Я'
    }
    
    # Сначала обрабатываем многосимвольные комбинации
    result = text
    for latin, cyrillic in reverse_dict.items():
        if len(latin) > 1:
            result = result.replace(latin, cyrillic)
    
    # Затем одиночные символы
    for char in result:
        if char in reverse_dict:
            result = result.replace(char, reverse_dict[char])
    
    return result

def test_transliteration():
    """Тестирует транслитерацию"""
    
    print("🔄 ТЕСТ ТРАНСЛИТЕРАЦИИ")
    print("=" * 40)
    
    test_cases = [
        "Қазақстан - менің Отаным!",
        "Абай Құнанбайұлы қазақтың ұлы ақыны",
        "Алматы - Қазақстанның ең ірі қаласы",
        "Наурыз мерекесі көктемнің келуін білдіреді",
        "мен супер баламын"
    ]
    
    for text in test_cases:
        latin = cyrillic_to_latin(text)
        back_to_cyrillic = latin_to_cyrillic(latin)
        
        print(f"\nИсходный: {text}")
        print(f"Латинский: {latin}")
        print(f"Обратно: {back_to_cyrillic}")
        print(f"Совпадает: {'✅' if text == back_to_cyrillic else '❌'}")

if __name__ == "__main__":
    test_transliteration()
