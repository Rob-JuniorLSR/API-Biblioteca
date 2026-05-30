CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    ano_publicacao INTEGER NOT NULL,
    quantidade INTEGER NOT NULL
);

INSERT INTO livros (titulo, autor, genero, ano_publicacao, quantidade)
VALUES
('Dom Casmurro', 'Machado de Assis', 'Romance', 1899, 10),
('O Cortiço', 'Aluísio Azevedo', 'Romance', 1890, 8),
('Capitães da Areia', 'Jorge Amado', 'Drama', 1937, 12),
('Vidas Secas', 'Graciliano Ramos', 'Drama', 1938, 7),
('Iracema', 'José de Alencar', 'Romance', 1865, 5);