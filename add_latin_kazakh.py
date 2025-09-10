#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Добавление латинского казахского в корпус
"""

import os

def create_latin_kazakh_texts():
    """Создает тексты на латинском казахском"""
    
    latin_texts = [
        # Транслитерация существующих текстов
        "Qazaqstan Respublikasy Ortalyq Aziya men Shygys Evropada ornalasqan memleket. Astanasy - Nur-Sultan qalasy. En iri qalasy - Almaty. Qazaqstan aumagy boiynsha alemdegi togyzynshy iri el. Khalqy 19 millionnan astam adam. Memlekettik tili - qazaq tili, resmi til - orys tili. Qazaqstan kop ultty memleket bolyp tabylady.",
        
        "Abay Qunanbaiuly qazaqtyn uly aqyny, agartushysy, kompozitory, filosofy zhane audarmashysy. Ol qazaq adebietinin klassigi bolyp sanalady. Abaidyn shygarmalary qazaq khalqynyn rukhany murasynyn bir boligi. Onyn 'Qara sozderi' qazaq filosofiasynyn mazdy derekkozhi bolyp tabylady. Abay qazaq zhazba adebietinin negizin qalaushylardyn biri.",
        
        "Qazaq tili turki tiller tobyna zhatatyn til. Qazaqstan Respublikasynyn memlekettik tili. Qazaq tilinde soileitin adamdar sany 12 millionnan astam. Qazaq tili kirillitsa arpimen zhazylady, biraq latyn arpine koshu zhosparylyp otyr. Qazaq tilinin ozindik erekshelikteri bar: dauysty dybystardyn uilesimi, septik zhuiesi, etistiktyn kurdele turlenu zhuiesi.",
        
        "Almaty - Qazaqstannyn en iri qalasy zhane burynghy astanasy. Qala Ile Alatauynyn eteginde ornalasqan. Almaty Qazaqstannyn madeni, gylymi zhane ekonomikalyq ortalygy bolyp tabylady. Qalada koptegen universitetter, teatrlar, muzeylar ornalasqan. Almaty 'Alma-Ata' dep te atalady, bul 'alma atasy' degendi bildiredi.",
        
        "Nauryz - qazaqtardyn ulttyq merekesi, zhana zhyl merekesi. Nauryz 22 nauryzda toilnady. Bul mereke koktemnnin keluin, tabighattyn zhanaruyn bildiredi. Nauryz kuni qazaqtar nauryz koje daindady, bul zheti turli dannen zhasyalghan tagam. Nauryz merekesi barlyq Ortalyq Aziya khalqtarynda toilnady.",
        
        # Дополнительные тексты
        "Men super balamyn! Men qazaq tili uiretin bala. Menin atym Zhanar. Men Almatyda tuilganmin. Menin otam zhane anam qazaq. Biz qazaq tilinde soileimiz.",
        
        "Qazaqstan - menin Otanym! Bul menin tugan zherim. Menin qazaq eli menin zhuregimde. Men qazaqtyn balasymyn. Men qazaq tili menin ana tilim.",
        
        "Almaty - menin tugan qalam. Bul qala ote suyikti. Almatyda koptegen parkter bar. Almatyda Tyan-Shan taulary bar. Almaty - Qazaqstannyn madeni ortalygy.",
        
        "Abay Qunanbaiuly - qazaqtyn uly aqyny. Ol qazaq adebietinin klassigi. Abaidyn shygarmalary ote suyikti. Abay qazaq filosofiasynyn negizshisi. Abay - qazaqtyn uly adamdar.",
        
        "Qazaq tili - menin ana tilim. Men qazaq tilinde soileimin. Qazaq tili turki tiller tobyna zhatady. Qazaq tili ote suyikti til. Men qazaq tilin uiretinmin."
    ]
    
    return latin_texts

def main():
    """Добавляет латинские тексты в корпус"""
    
    output_dir = "langdetect/datasets/train/kk"
    
    if not os.path.exists(output_dir):
        print(f"Ошибка: Папка {output_dir} не существует")
        return
    
    print("Создание латинских казахских текстов...")
    latin_texts = create_latin_kazakh_texts()
    
    # Находим следующий номер файла
    existing_files = [f for f in os.listdir(output_dir) if f.endswith('-kk.txt')]
    next_number = len(existing_files) + 1
    
    print(f"Существующих файлов: {len(existing_files)}")
    print(f"Добавляем {len(latin_texts)} латинских файлов...")
    
    total_size = 0
    for i, text in enumerate(latin_texts):
        filename = os.path.join(output_dir, f"{next_number + i}-kk-latin.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            
            file_size = len(text.encode('utf-8'))
            total_size += file_size
            print(f"Сохранен: {filename} ({file_size} байт)")
            
        except Exception as e:
            print(f"Ошибка при сохранении {filename}: {e}")
    
    print(f"\nДобавлено: {len(latin_texts)} файлов")
    print(f"Общий размер: {total_size} байт ({total_size/1024:.1f} KB)")
    print("Теперь нужно пересоздать профили!")

if __name__ == "__main__":
    main()
