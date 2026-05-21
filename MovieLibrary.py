import json
import os
from tkinter import *
from tkinter import ttk, messagebox

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x600")
        

        self.movies = []
        self.data_file = "movies.json"
        

        self.load_movies()

        self.create_widgets()

        self.refresh_table()
    
    def create_widgets(self):
    
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(N, W, E, S))
        
  
        add_frame = ttk.LabelFrame(main_frame, text="Добавить фильм", padding="10")
        add_frame.grid(row=0, column=0, columnspan=2, sticky=(W, E), pady=(0, 10))

        ttk.Label(add_frame, text="Название:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.title_entry = ttk.Entry(add_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Жанр:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
        self.genre_entry = ttk.Entry(add_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Год выпуска:").grid(row=2, column=0, sticky=W, padx=5, pady=2)
        self.year_entry = ttk.Entry(add_frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Рейтинг (0-10):").grid(row=3, column=0, sticky=W, padx=5, pady=2)
        self.rating_entry = ttk.Entry(add_frame, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=2)
        

        ttk.Button(add_frame, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)
        
  
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(W, E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.filter_genre_entry = ttk.Entry(filter_frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Год:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
        self.filter_year_entry = ttk.Entry(filter_frame, width=20)
        self.filter_year_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).grid(row=3, column=0, columnspan=2)
        
      
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(N, S, E, W))
        

        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        

        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        
        self.tree.column("Название", width=200)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=100)
        self.tree.column("Рейтинг", width=100)
        

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        

        self.tree.grid(row=0, column=0, sticky=(N, S, E, W))
        scrollbar.grid(row=0, column=1, sticky=(N, S))
        

        ttk.Button(table_frame, text="Удалить выбранный фильм", command=self.delete_movie).grid(row=1, column=0, columnspan=2, pady=5)
        

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
    
    def validate_input(self, title, genre, year, rating):
        """Проверка корректности ввода"""
        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return False
        
        try:
            year_int = int(year)
            if year_int < 1888 or year_int > 2030:  # Первый фильм снят в 1888
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2030")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return False
        
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return False
        
        return True
    
    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        if not self.validate_input(title, genre, year, rating):
            return
        
        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }
        
        self.movies.append(movie)
        self.save_movies()
        self.refresh_table()
        

        self.title_entry.delete(0, END)
        self.genre_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.rating_entry.delete(0, END)
        
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите фильм для удаления")
            return
        

        item = self.tree.item(selected[0])
        values = item["values"]
        

        for i, movie in enumerate(self.movies):
            if (movie["title"] == values[0] and 
                movie["genre"] == values[1] and 
                movie["year"] == values[2] and 
                movie["rating"] == values[3]):
                del self.movies[i]
                break
        
        self.save_movies()
        self.refresh_table()
        messagebox.showinfo("Успех", "Фильм удалён")
    
    def apply_filter(self):
        """Применение фильтра"""
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()
        
        filtered_movies = self.movies.copy()
        
        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]
        
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m["year"] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год для фильтрации должен быть числом")
                return
        
        self.refresh_table(filtered_movies)
    
    def reset_filter(self):
        """Сброс фильтра"""
        self.filter_genre_entry.delete(0, END)
        self.filter_year_entry.delete(0, END)
        self.refresh_table()
    
    def refresh_table(self, movies=None):
        """Обновление таблицы"""
 
        for item in self.tree.get_children():
            self.tree.delete(item)
        

        if movies is None:
            movies = self.movies
        

        for movie in movies:
            self.tree.insert("", END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))
    
    def save_movies(self):
        """Сохранение данных в JSON"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)
    
    def load_movies(self):
        """Загрузка данных из JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.movies = []

if __name__ == "__main__":
    root = Tk()
    app = MovieLibrary(root)
    root.mainloop()