# Модель TF‑IDF для MyLangDetect

Файл модели `tfidf_langid.joblib` по умолчанию не хранится в репозитории.

Варианты использования:

1) Укажите путь к модели через переменную окружения:

   ```bash
   export MYLANGDETECT_MODEL_PATH=/absolute/path/to/tfidf_langid.joblib
   ```

2) Скопируйте файл в эту папку (не рекомендуется для публичного Git из‑за размера):

   ```
   mylangdetect/model/tfidf_langid.joblib
   ```

3) Используйте Git LFS для хранения больших файлов (если доступно):

   ```bash
   git lfs install
   git lfs track "mylangdetect/model/*.joblib"
   ```

Код автоматически ищет модель сначала здесь, затем по пути из `MYLANGDETECT_MODEL_PATH`.

