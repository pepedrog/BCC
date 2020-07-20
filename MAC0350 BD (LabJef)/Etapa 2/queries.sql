-- 4.1 Liste  todos  os  exames  realizados, com  seus  respectivos  tipos, --
-- bem  como os seus pacientes com suas respectivas datas de solicitação e execução. --
select paciente.nome as nome_do_paciente, 
realiza.id_exame, 
realiza.data_de_solicitacao, 
realiza.data_de_realizacao,
exame.tipo
from paciente, realiza, exame
where paciente.id_paciente = realiza.id_paciente and exame.id_exame = realiza.id_exame;

-- 4.2 Liste os 5 exames realizados com maior eficiência --
select id_exame, (data_de_realizacao - data_de_solicitacao) as eficiencia
from realiza order by eficiencia limit 5;

-- 4.3 Liste os serviços que podem ser utilizados pelos usuarios --
select distinct usuario.id_usuario, servico.nome as serviço
from usuario, possui, servico, pertence, tutelamento
where -- Serviços que vem do perfil --
(usuario.id_usuario = possui.id_usuario and 
pertence.id_perfil = possui.id_perfil and
servico.id_servico = pertence.id_servico) 
or -- Serviços que vem do tutelamento --
(usuario.id_usuario = tutelamento.id_usuario_tutelado and
servico.id_servico = tutelamento.id_servico);

-- 4.4 Liste os serviços que podem ser utilizados por usuários tutelados --
-- Igual a 4.3, restringindo para usuários tutelados --
select distinct usuario.id_usuario, servico.nome as serviço
from usuario, possui, servico, pertence, tutelamento
where usuario.id_usuario = tutelamento.id_usuario_tutelado and
-- Serviços que vem do perfil --
((usuario.id_usuario = possui.id_usuario and 
pertence.id_perfil = possui.id_perfil and
servico.id_servico = pertence.id_servico) 
or -- Serviços que vem do tutelamento --
servico.id_servico = tutelamento.id_servico);

-- 4.5 Liste  em  ordem  crescente  o  total  de  serviços  utilizados --
-- agrupados pelos tipos de serviços disponíveis e pelo perfil dos usuários. --

-- Em resumo, o 'realizou' nos da um usuário 'u' e um servico 's'
-- então fazemos uma tupla pra cada perfil de 'u' que dá acesso ao serviço 's'
-- Por fim, unimos com os serviços de tutelamento
select rel.classe, rel.tipo, count(rel.id_servico) as quant
from 
(select servico.classe, perf.tipo, r.id_servico 
 from realizou r, perfil perf, servico, possui, pertence
 where
	(r.id_servico = servico.id_servico and
	 possui.id_usuario = r.id_usuario and
	 possui.id_perfil = perf.id_perfil and
	 pertence.id_perfil = perf.id_perfil and
	 pertence.id_servico = r.id_servico)
  -- Agora juntamos com os serviços realizados por perfils tutelados
  UNION ALL
  select servico.classe, perfil.tipo, r.id_servico
  from realizou r, perfil, servico, tutelamento tut
  where 
	 r.id_servico = tut.id_servico and r.id_servico = servico.id_servico and
	 r.id_usuario = tut.id_usuario_tutelado and tut.id_perfil = perfil.id_perfil) as rel
group by rel.classe, rel.tipo order by quant;