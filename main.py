import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conexão com banco
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='SuaSenhaAqui',
    database='escola'
)
cursor = conn.cursor()

# Cores
cor_fundo = "#e8f5e9"   # Verde bem claro
cor_botao = "#43a047"   # Verde médio
cor_texto = "#1b5e20"   # Verde escuro

# Funções
def cadastrar_aluno():
    nome = entry_nome.get()
    idade = entry_idade.get()
    curso = entry_curso.get()

    if nome and idade and curso:
        sql = "INSERT INTO alunos (nome, idade, curso) VALUES (%s, %s, %s)"
        valores = (nome, idade, curso)
        cursor.execute(sql, valores)
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno cadastrado!")
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_curso.delete(0, tk.END)
        listar_alunos()
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def deletar_aluno():
    selecionado = tree.focus()
    if selecionado:
        valores = tree.item(selecionado, 'values')
        id_aluno = valores[0]
        sql = "DELETE FROM alunos WHERE id = %s"
        cursor.execute(sql, (id_aluno,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno deletado!")
        listar_alunos()
    else:
        messagebox.showwarning("Atenção", "Selecione um aluno para deletar.")

def listar_alunos():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    for aluno in alunos:
        tree.insert("", "end", values=aluno)

# Janela principal
janela = tk.Tk()
janela.title("Sistema de Cadastro de Alunos")
janela.geometry("900x600")
janela.configure(bg=cor_fundo)

# Fonte Roboto
font_padrao = ("Roboto", 12)

# Frame Cadastro
frame_cadastro = tk.Frame(janela, bg=cor_fundo)
frame_cadastro.pack(pady=10)

tk.Label(frame_cadastro, text="Nome:", font=font_padrao, bg=cor_fundo, fg=cor_texto).grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_cadastro, font=font_padrao, width=30)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Idade:", font=font_padrao, bg=cor_fundo, fg=cor_texto).grid(row=1, column=0, padx=5, pady=5)
entry_idade = tk.Entry(frame_cadastro, font=font_padrao, width=30)
entry_idade.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Curso:", font=font_padrao, bg=cor_fundo, fg=cor_texto).grid(row=2, column=0, padx=5, pady=5)
entry_curso = tk.Entry(frame_cadastro, font=font_padrao, width=30)
entry_curso.grid(row=2, column=1, padx=5, pady=5)

btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar Aluno", command=cadastrar_aluno, bg=cor_botao, fg="white", font=font_padrao, width=25)
btn_cadastrar.grid(row=3, column=0, columnspan=2, pady=10)

# Frame Lista
frame_lista = tk.Frame(janela, bg=cor_fundo)
frame_lista.pack(pady=20, fill=tk.BOTH, expand=True)

cols = ("ID", "Nome", "Idade", "Curso")
tree = ttk.Treeview(frame_lista, columns=cols, show="headings", height=15)
for col in cols:
    tree.heading(col, text=col)
    tree.column("ID", width=50, anchor=tk.CENTER)
    tree.column("Nome", width=250, anchor=tk.W)
    tree.column("Idade", width=100, anchor=tk.CENTER)
    tree.column("Curso", width=200, anchor=tk.W)

tree.pack(fill=tk.BOTH, expand=True)

# Scrollbar para tabela
scroll_y = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
tree.configure(yscroll=scroll_y.set)
scroll_y.pack(side="right", fill="y")

btn_deletar = tk.Button(janela, text="Deletar Aluno Selecionado", command=deletar_aluno, bg=cor_botao, fg="white", font=font_padrao, width=30)
btn_deletar.pack(pady=10)

# Estilo da tabela
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=cor_fundo, foreground=cor_texto, fieldbackground=cor_fundo, font=font_padrao)
style.configure("Treeview.Heading", font=("Roboto", 13, "bold"), foreground=cor_texto)

listar_alunos()

# Rodar janela
janela.mainloop()

# Fechar conexão
cursor.close()
conn.close()
