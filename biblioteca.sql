CREATE TABLE autores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    ano_publicacao INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    autor_id INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES autores(id)
);

INSERT INTO autores (nome)
VALUES
('Machado de Assis'),
('Aluísio Azevedo'),
('Jorge Amado'),
('Graciliano Ramos'),
('José de Alencar');

INSERT INTO livros
(titulo, genero, ano_publicacao, quantidade, autor_id)
VALUES
('Dom Casmurro', 'Romance', 1899, 10, 1),
('O Cortiço', 'Romance', 1890, 8, 2),
('Capitães da Areia', 'Drama', 1937, 12, 3),
('Vidas Secas', 'Drama', 1938, 7, 4),
('Iracema', 'Romance', 1865, 5, 5);
