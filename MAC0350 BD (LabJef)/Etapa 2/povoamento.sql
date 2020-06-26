-- SCHEMA: public

-------------------- INSERÇÕES - POVOAMENTO DO BANCO -------------------
-- (Pode ser que um ou outro dado tenha sido modificado pra melhorar as consultas)
-- (Mas as inserções originais foram essas)
-- (Infelizmente, acabamos perdendo os inserts das tabelas PERTENCE e TUTELAMENTO)


------------------------------- USUÁRIOS --------------------------------
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (0, '33344455508', 'Denise Maria Avancini', 'Patologia', 'FMUSP', '19750514', 'denise_maria', 'denise0101', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (1, '33344466623', 'Raymundo Soares de Azevedo', 'Patologia', 'FMUSP', '19620226', 'raymundo_soares', 'raymundo0505', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (2, '33344477749', 'Wu Tu Hsing', 'Patologia', 'FMUSP', '19701125', 'wu_tu', 'hsing999', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (3, '33344488864', 'Suely Kazue Nagahashi', 'Neurologia', 'FMUSP', '19610911', 'suely_kazue', 'nagahashi123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (4, '33344499980', 'Eduardo Genaro Mutarelli', 'Neurologia', 'FMUSP', '19760301', 'eduardo_genaro', 'mutarelli456', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (5, '33344400010', 'Edna Maria de Albuquerque', 'Pediatria', 'FMUSP', '19650507', 'edna_maria', 'albuquerque789', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (6, '33355566667', 'Thelma Suely Okay', 'Pediatria', 'FMUSP', '19800922', 'thelma_suely', 'okayokay', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (7, '33355577782', 'Carlos Alberto Moreira Filho', 'Pediatria', 'FMUSP', '19680129', 'carlos_alberto', 'cazalbe15', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (8, '33355588806', 'Caio Henrique Freitas', 'Epidemiologia', 'FMUSP', '19910402', 'caio_henrique', 'freitas1991', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (9, '33355599913', 'Paulo Amorim Moreira', 'Epidemiologia', 'FMUSP', '19780125', 'paulo_amorim', 'moreira123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (10, '22255599961', 'Rosana Sayuri Sato', 'Saúde Pública', 'FSPUSP', '19830811', 'rosana_sayuri', 'sato456', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (11, '22244499928', 'Doralice Severo da Cruz', 'Saúde Pública', 'FSPUSP', '19940105', 'doralice_severo', 'cruz789', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (12, '22266699903', 'Fernão Dias de Lima', 'Saúde Pública', 'FSPUSP', '19681215', 'fernao_dias', 'limalima10', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (13, '22277799939', 'Eunice Aparecida Galati', 'Saúde Pública', 'FSPUSP', '19781231', 'eunice_aparecida', 'galati123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (14, '22288899972', 'Agnaldo Edson do Nascimento', 'Saúde Pública', 'FSPUSP', '19880211', 'agnaldo_edson', 'nascimento88', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (15, '33366600098', 'Edimilson Ramos Migowski', 'Pediatria', 'FMUFRJ', '19700606', 'edimilson_ramos', 'migowski789', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (16, '33377766634', 'Elaine Sobral da Costa', 'Pediatria', 'FMUFRJ', '19701022', 'elaine_sobral', 'costa1970', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (17, '33388877793', 'Marcia Gonçalves Ribeiro', 'Pediatria', 'FMUFRJ', '19901129', 'marcia_goncalves', 'ribeiro123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (18, '33366611103', 'Dalila Poli de Carvalho', 'Patologia', 'FMUFRJ', '19921122', 'dalila_poli', 'carvalho10', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (19, '33377711147', 'José Carlos Pando Esperança', 'Patologia', 'FMUFRJ', '19680210', 'jose_pando', 'esperanca123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (20, '33399911114', 'Valeria Ferreira Romano', 'Patologia', 'FMUFRJ', '19770303', 'maria_conceicao', 'zacharias456', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (21, '22299911162', 'Iranaia Assunção Miranda', 'Virologia', 'IMUFRJ', '19810514', 'iranaia_assuncao', 'miranda123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (22, '22299922288', 'Juliana Reis Cortinez', 'Virologia', 'IMUFRJ', '19911214', 'juliana_reis', 'cortinez246', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (23, '22299933301', 'Davis Ferreira', 'Virologia', 'IMUFRJ', '19741101', 'davis_ferreira', 'ferreira74', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (24, '22299944419', 'Ana Marcia de Sá Guimarães', 'Virologia', 'ICBUSP', '19660726', 'ana_marcia', 'guimaraes123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (25, '22299955534', 'Beny Spira', 'Virologia', 'ICBUSP', '19711027', 'beny_spira', 'spyrapira', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (26, '22299966650', 'Nísia Trindade Lima', 'Virologia', 'FIOCRUZ', '19690401', 'nisia_trindade', 'lima789', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (27, '22299977775', 'Maria Rachel de Gomensoro', 'Virologia', 'FIOCRUZ', '19901029', 'maria_rachel', 'gomensoro246', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (28, '22299988890', 'Magali Romero Sá', 'Patologia', 'FIOCRUZ', '19770730', 'magali_roma', 'sasasa3', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (29, '22288844485', 'Gilberto Hochman', 'Patologia', 'FIOCRUZ', '19711130', 'gilberto_hochman', 'hockmano10', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (30, '22288866616', 'Flavio Coelho Edler', 'Saúde Pública', 'FIOCRUZ', '19711228', 'flavio_coelho', 'edler123', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (31, '44455566619', 'Rogerio Marcos Fernandes', 'Virologia', 'FIOCRUZ', '19880811', 'rogerio_marcos', 'rogerinho1010', NULL);
INSERT INTO usuario (id_usuario, cpf, nome, area_de_pesquisa, instituicao, data_de_nascimento, login, senha, id_tutor)
VALUES (32, '44455577734', 'Pedro Gigeck Freire', 'Patologia', 'FIOCRUZ', '19751021', 'pedro_gigeck', 'trabalhonota10', NULL);

------------------------------- PACIENTE -------------------------------
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (0, '12345678909', 'Leila Almeida Cavalcanti', 'Avenida São José, 200. São Paulo-SP', '19980131');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (1, '12345679972', 'Yasmin Rodrigues Lima', 'Rua João Soriani, 17. Londrina-PR', '19810214');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (2, '12345698926', 'Kaike Barbosa Almeida', 'Rua Antônio Dias de Menezes Filho, 257. Contagem-MG', '19721122');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (3, '12345978961', 'Gabriela Martins Barros', 'Avenida Cidade de Pelotas, 123. Rio Grande-RS', '19680720');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (4, '12349678989', 'João Paulo Martins', 'Avenida Santo Antonio, Salvador-BA', '19910715');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (5, '12345678739', 'Rafael Araujo Lima', 'Rua Vinte e Três, 40. Mogi das Cruzes-SP', '19660322');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (6, '12345677929', 'Ana Fernandes Barbosa', 'Rua Paulo Torne, 83. Manaus-AM', '19810214');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (7, '12345688963', 'Rogerio Pereira Alencar', 'Rua Machado de Assis, 257. Contagem-MG', '19721122');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (8, '12345778954', 'Leila Torres Rocha', 'Avenida Ipiranga, 2100. Olinda-PE', '19930317');
INSERT INTO paciente (id_paciente, cpf, nome, endereco, nascimento)
VALUES (9, '12347678990', 'Kauã Silva Porto', 'Rua dos Alarmistas, 34. Curitiba-Pr', '19851222');

------------------------------ SERVIÇO ----------------------------
INSERT INTO servico (id_servico, nome, classe)
VALUES (0, 'Visualiza Exame', 'visualização');
INSERT INTO servico (id_servico, nome, classe)
VALUES (1, 'Insere Exame', 'inserção');
INSERT INTO servico (id_servico, nome, classe)
VALUES (2, 'Altera Exame', 'alteração');
INSERT INTO servico (id_servico, nome, classe)
VALUES (3, 'Remove Exame', 'remoção');

-------------------- EXAME ---------------------
INSERT INTO exame (id_exame, tipo, virus) VALUES (0, 'PCR', 'H1N1');
INSERT INTO exame (id_exame, tipo, virus) VALUES (1, 'PCR', 'Influenza');
INSERT INTO exame (id_exame, tipo, virus) VALUES (2, 'PCR', 'COVID19');
INSERT INTO exame (id_exame, tipo, virus) VALUES (3, 'PCR', 'SARSCOV2');
INSERT INTO exame (id_exame, tipo, virus) VALUES (4, 'anticorpos', 'H1N1');
INSERT INTO exame (id_exame, tipo, virus) VALUES (5, 'anticorpos', 'Influenza');
INSERT INTO exame (id_exame, tipo, virus) VALUES (6, 'anticorpos', 'COVID19');
INSERT INTO exame (id_exame, tipo, virus) VALUES (7, 'anticorpos', 'SARSCOV2');

-------------------- PERFIL ---------------------
INSERT INTO perfil (id_perfil, codigo, tipo)
VALUES (0, '0', 'pesquisador');
INSERT INTO perfil (id_perfil, codigo, tipo)
VALUES (1, '1', 'aluno');
INSERT INTO perfil (id_perfil, codigo, tipo)
VALUES (2, '2', 'funcionario');
INSERT INTO perfil (id_perfil, codigo, tipo)
VALUES (3, '3', 'administrador');
INSERT INTO perfil (id_perfil, codigo, tipo)
VALUES (4, '4', 'usuário comum');
INSERT INTO perfil (id_perfil, codigo, tipo)
VALUES (5, '5', 'eventuais');

----------------------- POSSUI (USUARIO x PERFIL) -------------------------------
INSERT INTO possui (id_usuario, id_perfil) VALUES (0, 0);
INSERT INTO possui (id_usuario, id_perfil) VALUES (1, 0);
INSERT INTO possui (id_usuario, id_perfil) VALUES (2, 0);
INSERT INTO possui (id_usuario, id_perfil) VALUES (3, 0);
INSERT INTO possui (id_usuario, id_perfil) VALUES (4, 0);
INSERT INTO possui (id_usuario, id_perfil) VALUES (5, 0);
INSERT INTO possui (id_usuario, id_perfil) VALUES (6, 0);
INSERT INTO possui (id_usuario, id_perfil) VALUES (7, 1);
INSERT INTO possui (id_usuario, id_perfil) VALUES (9, 1);
INSERT INTO possui (id_usuario, id_perfil) VALUES (10, 1);
INSERT INTO possui (id_usuario, id_perfil) VALUES (11, 1);
INSERT INTO possui (id_usuario, id_perfil) VALUES (12, 2);
INSERT INTO possui (id_usuario, id_perfil) VALUES (13, 2);
INSERT INTO possui (id_usuario, id_perfil) VALUES (14, 3);
INSERT INTO possui (id_usuario, id_perfil) VALUES (15, 3);
INSERT INTO possui (id_usuario, id_perfil) VALUES (16, 4);

--------------------- GERENCIA (SERVIÇO x EXAME) -------------------------
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 0);
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 1);
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 2);
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 3);
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 4);
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 5);
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 6);
INSERT INTO gerencia (id_servico, id_exame) VALUES (0, 7);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 0);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 1);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 2);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 3);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 4);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 5);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 6);
INSERT INTO gerencia (id_servico, id_exame) VALUES (1, 7);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 0);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 1);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 2);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 3);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 4);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 5);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 6);
INSERT INTO gerencia (id_servico, id_exame) VALUES (2, 7);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 0);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 1);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 2);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 3);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 4);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 5);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 6);
INSERT INTO gerencia (id_servico, id_exame) VALUES (3, 7);

----------------------- AMOSTRAS ------------------------
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (0, 6, 0, 'lancetador', 'sangue');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (0, 2, 1, 'swab', 'muco nasal');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (1, 7, 2, 'lancetador', 'sangue');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (1, 6, 3, 'lancetador', 'sangue');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (2, 0, 4, 'swab', 'muco nasal');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (2, 4, 5, 'lancetador', 'sangue');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (3, 1, 6, 'swab', 'muco nasal');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (3, 5, 7, 'lancetador', 'sangue');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (4, 1, 8, 'swab', 'muco nasal');
INSERT INTO amostra (id_paciente, id_exame, codigo_amostra, metodo_de_coleta, material)
VALUES (4, 2, 9, 'lancetador', 'sangue');

----------------------- REALIZA ------------------------
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (0, 6, 0, '20200412 10:00:00', '20200415 12:00:30');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (0, 6, 1, '20200401 14:30:00', '20200402 18:40:30');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (1, 6, 4, '20200521 16:45:30', '20200521 19:22:00');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (1, 6, 5, '20200524 09:05:00', '20200529 10:50:00');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (2, 6, 6, '20200510 09:10:00', '20200510 16:05:00');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (2, 6, 7, '20200507 17:30:00', '20200510 07:10:00');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (3, 1, 8, '20200424 12:40:00','20200510 10:55:30');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (3, 5, 9, '20200410 10:00:00', '20200424 18:00:00');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (4, 1, 2, '20200330 07:20:30', '20200330 09:05:00');
INSERT INTO realiza (id_paciente, id_exame, codigo_amostra, data_de_solicitacao, data_de_realizacao)
VALUES (4, 2, 0, '20200325 11:10:00', '20200327 11:00:00');

------------------ TUTELADOS -----------------
UPDATE usuario
SET is_tutor = 2
WHERE id_usuario = 28;
UPDATE usuario
SET is_tutor = 3
WHERE id_usuario = 21;
UPDATE usuario
SET is_tutor = 31
WHERE id_usuario = 25;
UPDATE usuario
SET is_tutor = 12
WHERE id_usuario = 9;
UPDATE usuario
SET is_tutor = 32
WHERE id_usuario = 19;

------------------ REALIZOU ---------------
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (3, 0, 1, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (27, 0, 2, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (15, 0, 3, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (12, 1, 4, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (14, 1, 5, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (22, 1, 0, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (26, 2, 7, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (25, 2, 6, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (31, 3, 2, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, is_exame, data_realizacao)
VALUES (32, 3, 7, CURRENT_TIMESTAMP);
INSERT INTO realizou (id_usuario, id_servico, id_exame, data_realizacao)
VALUES (3, 1, 5, CURRENT_TIMESTAMP);
-- Tutelado
INSERT INTO realizou (id_usuario, id_servico, id_exame, data_realizacao)
VALUES (9, 1, 5, CURRENT_TIMESTAMP);