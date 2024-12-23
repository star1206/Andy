import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, filedialog
import json

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My To-Do List")

        self.tasks = []
        self.load_tasks()

        self.task_label = tk.Label(root, text="할 일 목록")
        self.task_label.pack(pady=10)

        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(pady=10)

        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack(pady=5)

        self.add_button = tk.Button(root, text="할 일 추가", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="할 일 완료", width=20, command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="할 일 삭제", width=20, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="할 일 수정", width=20, command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.priority_button = tk.Button(root, text="우선순위 설정", width=20, command=self.set_priority)
        self.priority_button.pack(pady=5)

        self.save_button = tk.Button(root, text="텍스트 파일로 저장", width=20, command=self.save_to_text_file)
        self.save_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="종료", width=20, command=root.quit)
        self.quit_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append({"task": task, "done": False, "priority": 1})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("입력 오류", "할 일을 입력하세요.")
    
    def complete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["done"] = True
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("선택 오류", "완료할 할 일을 선택하세요.")
    
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("선택 오류", "삭제할 할 일을 선택하세요.")
    
    def edit_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            new_task = self.task_entry.get()
            if new_task:
                self.tasks[selected_index]["task"] = new_task
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("입력 오류", "새로운 할 일을 입력하세요.")
        except IndexError:
            messagebox.showwarning("선택 오류", "수정할 할 일을 선택하세요.")

    def set_priority(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            new_priority = simpledialog.askinteger("우선순위 설정", "새로운 우선순위 (1 ~ 5):")
            if new_priority and 1 <= new_priority <= 5:
                self.tasks[selected_index]["priority"] = new_priority
                self.update_task_listbox()
            else:
                messagebox.showwarning("입력 오류", "우선순위는 1에서 5까지의 값이어야 합니다.")
        except IndexError:
            messagebox.showwarning("선택 오류", "우선순위를 설정할 할 일을 선택하세요.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        # 우선순위에 따라 정렬
        sorted_tasks = sorted(self.tasks, key=lambda x: x["priority"])
        for task in sorted_tasks:
            status = "완료" if task["done"] else "진행 중"
            self.task_listbox.insert(tk.END, f"{task['task']} - {status} - 우선순위: {task['priority']}")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def save_to_text_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for task in self.tasks:
                    status = "완료" if task["done"] else "진행 중"
                    file.write(f"{task['task']} - {status} - 우선순위: {task['priority']}\n")
            messagebox.showinfo("저장 완료", f"할 일 목록이 {file_path}로 저장되었습니다.")

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    
    # 종료 시 파일에 저장
    root.protocol("WM_DELETE_WINDOW", app.save_tasks)
    
    root.mainloop()

if __name__ == "__main__":
    main()