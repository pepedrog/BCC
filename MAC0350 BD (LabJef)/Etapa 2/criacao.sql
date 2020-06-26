CREATE TABLE usuario (
    id_usuario    INT NOT NULL PRIMARY KEY,
    cpf    CHAR(11) NOT NULL,
    nome    VARCHAR(255) NOT NULL,
    area_de_pesquisa    VARCHAR(255),
    instituicao    VARCHAR(255),
    data_de_nascimento    DATE,
    login    VARCHAR(255) NOT NULL,
    senha    VARCHAR(255) NOT NULL,
    id_tutor   INT references usuario(id_usuario),
	UNIQUE (cpf)
);

CREATE TABLE perfil (
    id_perfil    INT NOT NULL PRIMARY KEY,
    codigo    VARCHAR(255) NOT NULL,
    tipo    VARCHAR(255),
	UNIQUE (codigo)
);

--Relacionamento possui
CREATE TABLE possui (
    id_usuario    INT NOT NULL references usuario(id_usuario),
    id_perfil    INT NOT NULL references perfil(id_perfil), 
	UNIQUE (id_usuario, id_perfil)
);

CREATE TABLE servico (
    id_servico    INT NOT NULL PRIMARY KEY,
    nome    VARCHAR(255) NOT NULL,
    classe    VARCHAR(255) NOT NULL CHECK (classe IN ('visualização', 'inserção', 'alteração', 'remoção')),
	UNIQUE (nome, classe)
);

--Relacionamento pertence
CREATE TABLE pertence (
    id_servico    INT NOT NULL references servico(id_servico),
    id_perfil    INT NOT NULL references perfil(id_perfil),
	UNIQUE (id_servico, id_perfil)
);

--Relacionamento tutelamento
CREATE TABLE tutelamento (
    id_usuario_tutelado    INT NOT NULL references usuario(id_usuario),
    id_tutor    INT NOT NULL references usuario(id_usuario),
    id_servico    INT NOT NULL references servico(id_servico),
    id_perfil    INT NOT NULL references perfil(id_perfil),
    data_de_inicio    DATE NOT NULL,
    data_de_termino    DATE,
	UNIQUE (id_usuario_tutelado, id_tutor, id_servico, id_perfil)
);

CREATE TABLE paciente (
    id_paciente    INT NOT NULL PRIMARY KEY,
    cpf    VARCHAR(11) NOT NULL,
    nome    VARCHAR(255) NOT NULL,
    endereco    VARCHAR(255) NOT NULL,
    nascimento    DATE NOT NULL,
	UNIQUE (cpf)
);

CREATE TABLE exame (
    id_exame    INT NOT NULL PRIMARY KEY,
    tipo    VARCHAR(255) NOT NULL,
    virus    VARCHAR(255) NOT NULL,
	UNIQUE (tipo, virus)
);

--Relacionamento gerencia
CREATE TABLE gerencia (
    id_servico    INT NOT NULL references servico(id_servico),
    id_exame    INT NOT NULL references exame(id_exame),
	UNIQUE (id_servico, id_exame)
);

--Relacionamento realiza
CREATE TABLE realiza (
    id_paciente    INT NOT NULL references paciente(id_paciente),
    id_exame    INT NOT NULL references exame(id_exame),
    codigo_amostra    VARCHAR(255),
    data_de_solicitacao TIMESTAMP,
    data_de_realizacao TIMESTAMP,
	UNIQUE (id_paciente, id_exame, data_de_realizacao)
);

--Agregado amostra
CREATE TABLE amostra (
    id_paciente    INT NOT NULL references paciente(id_paciente),
    id_exame    INT NOT NULL references exame(id_exame),
    codigo_amostra    VARCHAR(255) NOT NULL,    
    metodo_de_coleta    VARCHAR(255) NOT NULL,
    material    VARCHAR(255) NOT NULL,
	UNIQUE (id_paciente, id_exame, codigo_amostra)
);

-- Relacionamento realizou (para o histórico de serviços)
CREATE TABLE realizou (
	id_paciente INT NOT NULL references paciente(id_paciente),
    id_servico  INT NOT NULL references servico(id_servico),
	id_exame    INT NOT NULL references exame(id_exame),
	data_realizacao TIMESTAMP NOT NULL,
	UNIQUE (id_paciente, id_servico, id_exame)
);

-- As permissões de acesso e modificação foram feitas com esse comando :)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "10284632";