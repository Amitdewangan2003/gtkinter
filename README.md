# GTKinter

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![GTK](https://img.shields.io/badge/GTK-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

GTKinter - это обёртка над PyGTK, которая предоставляет API, похожий на стандартный Tkinter, но с использованием GTK+ 3.0.

## Особенности

- Tkinter-подобный синтаксис
- Поддержка большинства базовых виджетов Tkinter
- Использование возможностей GTK+
- Кроссплатформенность
- Поддержка современных фишек GTK
- Почти всегда Tkinter-совместим

## Установка

Требования:
- Python 3.6+
- PyGObject (для GTK 3.0)

**Установка зависимостей:**

```bash
# Для Linux (Debian/Ubuntu)
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Для Windows/macOS
pip install PyGObject
```

**Установка GTKinter:**

```bash
pip install gtkinter
```

## Пример работы

**Привет, мир:**

```python
from gtkinter import *

root = Tk()
root.title("Пример GTKinter")
root.geometry("300x200")

def on_click():
    label.config(text="Привет, мир!")

btn = Button(root, text="Нажми на меня!", command=on_click)
btn.pack(pady=10)

label = Label(root, font="Arial 24 bold italic", fg="red")
label.pack()

root.mainloop()
```

**Вывод текста с entry:**

```python
from gtkinter import *

def show_message():
    label["text"] = entry.get()

root = Tk()
root.title("Поле ввода Entry")
root.geometry("250x200")

entry = Entry()
entry.pack(anchor="nw", padx=6, pady=6)

btn = Button(text="Нажми на меня!", command=show_message)
btn.pack(anchor="nw", padx=6, pady=6)

label = Label(font="Arial 24 bold italic", fg="red")
label.pack(anchor="nw", padx=6, pady=6)

root.mainloop()
```
