import tkinter as tk
import json
import random

# Загрузка цитаты из файла
def load_quotes():
    
   try:
       with open("quotes.json", "r", encoding="utf-8") as file:
           return json.load(file)
       
   except (FileNotFoundError, json.JSONDecodeError):
       return []
  
   
# Сохранение цитаты в файл   
def save_quotes(quote_list):
    with open("quotes.json", "w", encoding="utf-8") as file:
           json.dump(quote_list, file, ensure_ascii=False, indent=4)
    
# Обновляем список задач в интерфейсе с учётом фильтра
def update_listbox():
   quote_listbox.delete(0, tk.END)
   selected_type = filter_var.get()
   if selected_type == "Все":
       filtered_quotes = quotes
   else:
       filtered_quotes = [quote for quote in quotes if quote.get("type", "работа") == selected_type]
   
   for quote in filtered_quotes:
       quote_listbox.insert(tk.END, f"{quote['type']} [{quote['author']}] <<{quote['quote']}>>")
       
# Добавление новой цитаты
def add_quote():
   type = entry_type.get().strip()
   author = entry_author.get().strip()
   quote = entry_quote.get().strip()
   
   if(quote!="" and type!="" and author!=""):
       quotes.append({"type": type, "author": author,"quote":quote})
       entry_type.delete(0,tk.END)    
       entry_author.delete(0,tk.END) 
       entry_quote.delete(0,tk.END)         
       update_listbox()
       save_quotes(quotes)
   else:
       error_label.config(text="Ошибка: введите все данные", fg="red")

random_quotes=[]

# Обновление списка цитат
def update_history_listbox():
   history_listbox.delete(0, tk.END)
   for quote in random_quotes:
       history_listbox.insert(tk.END, f"{quote['type']} [{quote['author']}] <<{quote['quote']}>>")

# Выбор случайной цитаты
def random_quote():
    num=random.randint(0, len(quotes)-1)
    selected_quote = quotes[num]
    current_quote_label["text"]=f"{selected_quote['quote']} [{selected_quote['author']}]"
    random_quotes.append(selected_quote)
    update_history_listbox()
    save_history()
    
   

# Сохраняем историю в JSON
def save_history():
    try:
        with open("history.json", "w", encoding="utf-8") as file:
            json.dump(random_quotes, file, ensure_ascii=False, indent=4)
    except:
        pass

# Загружаем историю из файла
def load_history():
    try:
        with open("history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Применяем фильтр при изменении выбора
def apply_filter(*args):
   update_listbox()

# Создание графического интерфейса
window= tk.Tk()
window.title("Цитаты")
window.geometry("600x700")

# Загружаем сохранённую историю
random_quotes = load_history()

# Вывод цитат
quote_listbox=tk.Listbox(window,height=8,width=50,selectmode=tk.SINGLE)
quote_listbox.pack(pady=10)

quotes = load_quotes()

# Блок фильтрации
filter_frame = tk.Frame(window)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT, padx=5)

filter_var = tk.StringVar(value="Все")
filter_var.trace('w', apply_filter)

types = ["Все", "учеба", "спорт", "работа"]
for t in types:
    tk.Radiobutton(filter_frame, text=t, variable=filter_var, value=t).pack(side=tk.LEFT, padx=5)

# 
type_frame = tk.Frame(window)
type_frame.pack(pady=5)

# Поле для типа цитаты
tk.Label(window, text="Тема цитаты:").pack(pady=(10,0))
entry_type = tk.Entry(window, font="Arial 12", width=40)
entry_type.pack(pady=5)

# Поле для автора цитаты
tk.Label(window, text="Автор цитаты:").pack(pady=(10,0))
entry_author = tk.Entry(window, font="Arial 12", width=40)
entry_author.pack(pady=5)

# Поле для текста цитаты
tk.Label(window, text="Текст цитаты:").pack(pady=(10,0))
entry_quote = tk.Entry(window, font="Arial 12", width=40)
entry_quote.pack(pady=5)

# Кнопка добавления цитаты
but_add = tk.Button(window, text="Добавить цитату", bg="green", fg="white", command=add_quote)
but_add.pack(pady=10)

# Кнопка  генерации
current_quote_label=tk.Label(window,text="Нажмите кнопку для генерации", font="Arial 12", fg="blue", wraplength=500)
current_quote_label.pack(pady=10)

but_random=tk.Button(window,text="выбрать случайную цитату",bg="lightblue",fg="white", command=random_quote)
but_random.pack(pady=5)

# Метка для ошибок
error_label=tk.Label(window, text="", font="Arial 10", fg="red")
error_label.pack(pady=5)

# Блок истории
tk.Label(window, text="История цитат, выбранных случайно:", font="Arial 10 bold").pack(pady=5)
history_listbox=tk.Listbox(window,height=8,width=50)
history_listbox.pack(pady=5)
update_history_listbox()

update_listbox() 

window.mainloop()