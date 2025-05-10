# GTKinter - GTK+ обёртка в стиле Tkinter

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![GTK](https://img.shields.io/badge/GTK-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

GTKinter - это обёртка над PyGTK, которая предоставляет API, похожий на стандартный Tkinter, но с использованием GTK+ 3.0.

## Особенности

- Знакомый Tkinter-подобный синтаксис
- Поддержка большинства базовых виджетов Tkinter
- Использование возможностей GTK+ (стили, темы, аппаратное ускорение)
- Кроссплатформенность (Linux, Windows, macOS)
- Поддержка современных фич GTK (прозрачность, анимации и др.)

## Установка

Требования:
- Python 3.6+
- PyGObject (для GTK 3.0)

Установка зависимостей:
```bash
# Для Linux (Debian/Ubuntu)
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Для Windows/macOS
pip install PyGObject
