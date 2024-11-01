import tkinter as tk
import random
import webbrowser
from questions import questions  # Certifique-se de que `questions.py` está corretamente importado

class ModernQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz - História de Apucarana")
        self.root.geometry("900x600")
        self.root.configure(bg="#1A1A40")

        self.score = 0
        self.question_index = 0
        self.total_questions = 20
        self.results_shown = False  # Controle para evitar duplicação

        # Selecionar aleatoriamente 20 das 100 perguntas
        self.selected_questions = random.sample(questions, self.total_questions)

        # Título da pergunta
        self.question_label = tk.Label(root, text="Question", wraplength=800, justify="center",
                                       font=("Helvetica", 18, "bold"), bg="#1A1A40", fg="white")
        self.question_label.pack(pady=20)

        # Opções estilizadas
        self.options_frame = tk.Frame(root, bg="#1A1A40")
        self.options_frame.pack(pady=20)

        self.options = []
        for i in range(4):
            button = tk.Button(self.options_frame, text=f"Option {i+1}", font=("Helvetica", 12),
                               bg="#26266F", fg="white", activebackground="#4CAF50", activeforeground="white",
                               relief="groove", borderwidth=2, highlightthickness=0, wraplength=200,
                               height=4, width=30)
            button.config(command=lambda b=i: self.check_answer(b))
            button.grid(row=i // 2, column=i % 2, padx=20, pady=10)
            self.options.append(button)

        # Barra de progresso usando Canvas
        self.progress_canvas = tk.Canvas(root, width=400, height=20, bg="#1A1A40", highlightthickness=0)
        self.progress_canvas.pack(pady=10)

        # Criar os retângulos da barra de progresso
        self.progress_rects = []
        for i in range(self.total_questions):
            rect = self.progress_canvas.create_rectangle(i * 20, 0, (i + 1) * 20, 20, fill="#555555", outline="")
            self.progress_rects.append(rect)

        # Mensagem de feedback
        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#1A1A40", fg="yellow")
        self.feedback_label.pack(pady=10)

        # Frame para o contador de perguntas e Score
        self.info_frame = tk.Frame(root, bg="#1A1A40")
        self.info_frame.pack(fill="x", side="bottom", pady=10)

        # Contador de perguntas (canto inferior esquerdo)
        self.question_counter_label = tk.Label(self.info_frame, text=f"Pergunta: 1/{self.total_questions}",
                                               font=("Helvetica", 12, "bold"), bg="#1A1A40", fg="white", anchor="w")
        self.question_counter_label.pack(side="left", padx=20)

        # Score (canto inferior direito)
        self.score_label = tk.Label(self.info_frame, text=f"Score: {self.score}", font=("Helvetica", 12, "bold"),
                                    bg="#1A1A40", fg="white", anchor="e")
        self.score_label.pack(side="right", padx=20)

        self.load_question()

    def load_question(self):
        if self.question_index < self.total_questions:
            q = self.selected_questions[self.question_index]
            self.question_label.config(text=q["question"])
            random.shuffle(q["options"])
            for i, option in enumerate(q["options"]):
                self.options[i].config(text=option, state="normal")
            self.feedback_label.config(text="")
            # Atualizar o contador de perguntas e o Score
            self.question_counter_label.config(text=f"Pergunta: {self.question_index + 1}/{self.total_questions}")
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.show_results()

    def check_answer(self, index):
        selected_answer = self.options[index].cget("text")
        correct_answer = self.selected_questions[self.question_index]["answer"]

        if selected_answer == correct_answer:
            self.score += 1
            self.feedback_label.config(text="Resposta correta!", fg="green")
            self.progress_canvas.itemconfig(self.progress_rects[self.question_index], fill="green")
        else:
            self.feedback_label.config(text=f"Errou! A resposta correta é: {correct_answer}", fg="red")
            self.progress_canvas.itemconfig(self.progress_rects[self.question_index], fill="red")

        self.question_index += 1
        self.root.after(2000, self.load_question)

    def show_results(self):
        if not self.results_shown:  # Verificar se os resultados já foram exibidos
            self.results_shown = True  # Marcar como exibido

            # Esconder os widgets atuais
            self.info_frame.pack_forget()
            self.question_label.pack_forget()
            self.options_frame.pack_forget()
            self.progress_canvas.pack_forget()
            self.feedback_label.pack_forget()

            # Mostrar a tela de resultados
            result_label = tk.Label(self.root, text=f"Você marcou {self.score} ponto(s)!", font=("Helvetica", 18, "bold"),
                                    bg="#1A1A40", fg="white")
            result_label.pack(pady=30)

            # Botão para abrir o link do livro
            view_book_button = tk.Button(self.root, text="Ver Livro", font=("Helvetica", 14), bg="#4CAF50", fg="white",
                                         command=self.open_web_link)
            view_book_button.pack(pady=10)

            # Botão Reiniciar
            restart_button = tk.Button(self.root, text="Reiniciar", font=("Helvetica", 14), bg="#4CAF50", fg="white",
                                       command=self.restart_quiz)
            restart_button.pack(pady=10)

            # Botão Fechar
            close_button = tk.Button(self.root, text="Fechar", font=("Helvetica", 14), bg="#f44336", fg="white",
                                     command=self.root.quit)
            close_button.pack(pady=10)

    def open_web_link(self):
        # Link para a página do livro
        web_link = "https://www.visiteapucarana.com.br/alma-e-historia-das-ruas-de-apucarana/"
        webbrowser.open(web_link)

    def restart_quiz(self):
        # Fechar a janela atual
        self.root.destroy()
        # Criar uma nova janela
        new_root = tk.Tk()
        ModernQuizApp(new_root)
        new_root.mainloop()

# Iniciar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernQuizApp(root)
    root.mainloop()
