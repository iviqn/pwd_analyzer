# Библиотека PasswordAnalyzer
Библиотека на Python для комплексного анализа и генерации паролей с применением алгоритмов оценки безопасности.
# Установка
*1 способ*: Установка через pip с GitHub
```
pip install git+https://github.com/iviqn/password_analyzer.git 
```

*2 способ*: Установка как локальный пакет
```
cd /path/to/password_analyzer  # Переходим в директорию проекта
```
```
pip install . # устанавливаем
```
# Использование
*Импортирование библиотеки*
```
from password_analyzer import PasswordAnalyzer
```
*Базовый анализ*
```
# Комплексный анализ пароля
result = analyzer.all_analyze("Il0v35|)oqd")
print(f"Оценка: {result['rating']}/10")
print(f"Уровень безопасности: {result['level']}")
print("Рекомендации:", result['recs'])

# Генерация нового пароля
new_password = analyzer.gen_all(12)
print(f"Сгенерированный пароль: {new_password}")
```
