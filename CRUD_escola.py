import sqlite3

def conectar():
    return sqlite3.connect("sistema_escola.db")


# CRIAR TABELAS
# ==============================
def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT,
        cpf TEXT UNIQUE,
        telefone TEXT,
        email TEXT,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        carga_horaria INTEGER,
        valor REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS matriculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        curso_id INTEGER,
        data_matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Ativo',
        FOREIGN KEY (aluno_id) REFERENCES alunos(id),
        FOREIGN KEY (curso_id) REFERENCES cursos(id)
    )
    """)

    conn.commit()
    conn.close()


# ALUNOS
# ==============================

def inserir_aluno():
    nome = input("Nome: ")
    nascimento = input("Data de nascimento: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")
    email = input("Email: ")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO alunos (nome, data_nascimento, cpf, telefone, email)
    VALUES (?, ?, ?, ?, ?)
    """, (nome, nascimento, cpf, telefone, email))

    conn.commit()
    conn.close()
    print("Aluno cadastrado!")


def listar_alunos():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT * FROM alunos")
    dados = cur.fetchall()

    for a in dados:
        print(a)

    conn.close()


def atualizar_aluno():
    id_aluno = int(input("ID do aluno: "))

    novo_nome = input("Novo nome: ")
    novo_tel = input("Novo telefone: ")
    novo_email = input("Novo email: ")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    UPDATE alunos
    SET nome = ?, telefone = ?, email = ?
    WHERE id = ?
    """, (novo_nome, novo_tel, novo_email, id_aluno))

    if cur.rowcount == 0:
        print("Aluno não encontrado!")
    else:
        print("Aluno atualizado!")

    conn.commit()
    conn.close()


def excluir_aluno():
    id_aluno = int(input("ID do aluno: "))

    conn = conectar()
    cur = conn.cursor()

    cur.execute("DELETE FROM matriculas WHERE aluno_id = ?", (id_aluno,))
    cur.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))

    if cur.rowcount == 0:
        print("Aluno não encontrado!")
    else:
        print("Aluno excluído!")

    conn.commit()
    conn.close()


# CURSOS
# ==============================

def inserir_curso():
    nome = input("Nome do curso: ")
    carga = int(input("Carga horária: "))
    valor = float(input("Valor: "))

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO cursos (nome, carga_horaria, valor)
    VALUES (?, ?, ?)
    """, (nome, carga, valor))

    conn.commit()
    conn.close()
    print("Curso cadastrado!")


def listar_cursos():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT * FROM cursos")
    dados = cur.fetchall()

    for c in dados:
        print(c)

    conn.close()


def atualizar_curso():
    id_curso = int(input("ID do curso: "))

    novo_nome = input("Novo nome: ")
    nova_carga = int(input("Nova carga horária: "))
    novo_valor = float(input("Novo valor: "))

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    UPDATE cursos
    SET nome = ?, carga_horaria = ?, valor = ?
    WHERE id = ?
    """, (novo_nome, nova_carga, novo_valor, id_curso))

    if cur.rowcount == 0:
        print("Curso não encontrado!")
    else:
        print("Curso atualizado!")

    conn.commit()
    conn.close()


def excluir_curso():
    id_curso = int(input("ID do curso: "))

    conn = conectar()
    cur = conn.cursor()

    cur.execute("DELETE FROM matriculas WHERE curso_id = ?", (id_curso,))
    cur.execute("DELETE FROM cursos WHERE id = ?", (id_curso,))

    if cur.rowcount == 0:
        print("Curso não encontrado!")
    else:
        print("Curso excluído!")

    conn.commit()
    conn.close()


# MATRÍCULAS
# ==============================

def matricular_aluno():
    aluno_id = int(input("ID do aluno: "))
    curso_id = int(input("ID do curso: "))

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO matriculas (aluno_id, curso_id)
    VALUES (?, ?)
    """, (aluno_id, curso_id))

    conn.commit()
    conn.close()
    print("Matrícula realizada!")


def listar_matriculas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    SELECT m.id, a.nome, c.nome, m.status
    FROM matriculas m
    JOIN alunos a ON m.aluno_id = a.id
    JOIN cursos c ON m.curso_id = c.id
    """)

    dados = cur.fetchall()

    for m in dados:
        print(f"ID: {m[0]} | Aluno: {m[1]} | Curso: {m[2]} | Status: {m[3]}")

    conn.close()


def atualizar_matricula():
    id_matricula = int(input("ID da matrícula: "))
    novo_status = input("Novo status (Ativo/Cancelado): ")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    UPDATE matriculas
    SET status = ?
    WHERE id = ?
    """, (novo_status, id_matricula))

    if cur.rowcount == 0:
        print("Matrícula não encontrada!")
    else:
        print("Matrícula atualizada!")

    conn.commit()
    conn.close()


def excluir_matricula():
    id_matricula = int(input("ID da matrícula: "))

    conn = conectar()
    cur = conn.cursor()

    cur.execute("DELETE FROM matriculas WHERE id = ?", (id_matricula,))

    if cur.rowcount == 0:
        print("Matrícula não encontrada!")
    else:
        print("Matrícula excluída!")

    conn.commit()
    conn.close()


# MENU
# ==============================

def menu():
    criar_tabelas()

    while True:
        print("\n===== SISTEMA ESCOLAR =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Cadastrar curso")
        print("4 - Listar cursos")
        print("5 - Matricular aluno")
        print("6 - Listar matrículas")
        print("7 - Excluir aluno")
        print("8 - Excluir curso")
        print("9 - Excluir matrícula")
        print("10 - Atualizar aluno")
        print("11 - Atualizar curso")
        print("12 - Atualizar matrícula")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            inserir_aluno()
        elif op == "2":
            listar_alunos()
        elif op == "3":
            inserir_curso()
        elif op == "4":
            listar_cursos()
        elif op == "5":
            matricular_aluno()
        elif op == "6":
            listar_matriculas()
        elif op == "7":
            excluir_aluno()
        elif op == "8":
            excluir_curso()
        elif op == "9":
            excluir_matricula()
        elif op == "10":
            atualizar_aluno()
        elif op == "11":
            atualizar_curso()
        elif op == "12":
            atualizar_matricula()
        elif op == "0":
            break
        else:
            print("Opção inválida!")


menu()