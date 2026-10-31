-- Catálogos fixos: barreiras, adaptações, itens de questionário, tipos de erro, habilidades
INSERT INTO barreira VALUES
('P1','Decodificação e fluência de leitura','Lê devagar ou com erros; entende melhor ouvindo'),
('P2','Linguagem e compreensão','Dificuldade com enunciados longos, sintaxe complexa e linguagem figurada'),
('P3','Atenção e memória de trabalho','Perde o fio em tarefas longas; desempenho oscila na sessão'),
('P4','Previsibilidade, sensorial e comunicação social','Mudanças inesperadas e estímulos excessivos desorganizam'),
('P5','Senso numérico e matemática','Fatos básicos não automatizados; dificuldade com quantidades'),
('P6','Motor e grafomotor','Dificuldade em escrever, arrastar e acertar alvos pequenos'),
('P7','Ritmo e abstração','Precisa de mais repetições e exemplos concretos'),
('P8','Altas habilidades','Domina rápido; precisa de desafio e aceleração');

INSERT INTO adaptacao (codigo,nome,barreira_codigo,descricao,fonte_evidencia,parametros_padrao) VALUES
('AUDIO_ENUNCIADO','Enunciado em áudio','P1','Botão de ouvir o enunciado e as alternativas','Wood et al. 2018, d=0,35','{"auto_play":false}'),
('ESPACAMENTO_LETRAS','Espaçamento extra entre letras','P1','Letter-spacing ampliado','Zorzi et al. 2012, +20% velocidade','{"letter_spacing_em":0.12}'),
('ENUNCIADO_SIMPLES','Enunciado simplificado e literal','P2','Usa enunciado_simplificado do item','Filderman et al. 2021, g=0,59','{}'),
('GLOSSARIO_VISUAL','Glossário com imagem','P2','Palavras-chave com imagem ao tocar','Norbury et al. 2016 (barreiras)','{}'),
('UMA_INSTRUCAO','Uma instrução por vez','P3','Tarefa em etapas, instrução sempre visível','Kofler et al. 2020','{}'),
('BLOCO_CURTO','Blocos curtos com pausa','P3','Bloco de N itens e pausa sugerida','Kofler et al. 2013 (variabilidade)','{"itens_por_bloco":5,"pausa_s":120}'),
('CONFIRMAR_ENVIO','Confirmar antes de enviar','P3','Evita resposta impulsiva','Baker et al. 2004 (respostas rápidas)','{}'),
('AGENDA_VISUAL','Agenda visual da sessão','P4','Mostra "primeiro, depois" no início','NCAEP 2020 (apoios visuais)','{}'),
('INTERFACE_CALMA','Interface calma','P4','Sem animação/som automáticos; layout fixo; sem ranking','NCAEP 2020','{"ranking":false,"sons":false}'),
('APOIO_VISUAL_MAT','Apoio visual em matemática','P5','Reta numérica e barras de fração','Benavides-Varela et al. 2020, 0,55','{}'),
('ALVOS_GRANDES','Alvos de toque de 44 px','P6','Botões grandes; tocar em vez de arrastar','WCAG 2.2 SC 2.5.5','{"alvo_px":44}'),
('SEM_CRONOMETRO','Sem limite de tempo','P6','Remove cronômetros','WCAG 2.2 SC 2.2.1','{}'),
('EXEMPLO_RESOLVIDO','Exemplo resolvido antes','P7','Mostra exemplo antes do item','Análise de tarefa (NCAEP)','{}'),
('REVISAO_FREQUENTE','Revisões mais frequentes','P7','Meia-vida inicial menor','Cepeda et al. 2008','{"meia_vida_inicial_dias":0.5}'),
('ACELERACAO','Pular conteúdo dominado','P8','Teste de entrada; pula se dominar','Wilson et al. 2019 (zona de desafio)','{"zona_alvo_min":0.75}');

INSERT INTO questionario_item VALUES
('Q_LEITURA_LENTA','Lê devagar ou troca/omite letras','P1',1.0),
('Q_ENTENDE_OUVINDO','Entende melhor quando alguém lê para ele','P1',1.0),
('Q_INSTRUCAO_LONGA','Não entende instruções longas','P2',1.0),
('Q_LITERAL','Interpreta expressões ao pé da letra','P2',0.8),
('Q_SE_PERDE','Se perde em tarefas com vários passos','P3',1.0),
('Q_DISTRAI','Se distrai facilmente / não termina tarefas','P3',1.0),
('Q_MUDANCA','Fica agitado com mudanças de rotina','P4',1.0),
('Q_SENSORIAL','Incomoda-se com barulho, luz ou movimento','P4',0.8),
('Q_CONTA_DEDOS','Conta nos dedos / não memoriza tabuada','P5',1.0),
('Q_LETRA','Letra ilegível ou muito lenta para escrever','P6',1.0),
('Q_REPETICOES','Precisa de muitas repetições e exemplos concretos','P7',1.0),
('Q_TEDIO','Termina muito antes e se entedia','P8',1.0);

INSERT INTO tipo_erro VALUES
('conceito','Não compreende o conceito (ex.: soma numeradores e denominadores)','Revisar o conceito com representação visual'),
('procedimento','Conhece o conceito mas erra a execução','Exemplo resolvido passo a passo'),
('leitura','Erro causado pela leitura do enunciado','Ativar áudio / enunciado simplificado'),
('fato_aritmetico','Erro em conta básica','Prática de fluência'),
('motor','Erro de interação (toque/arrasto)','Alvos maiores / trocar formato');

INSERT INTO habilidade (codigo,componente,ano_escolar,descricao,prerequisito_codigo) VALUES
('EF06MA07','Matemática',6,'Compreender, comparar e ordenar frações associadas às ideias de partes de inteiros e resultado de divisão',NULL),
('EF06MA10','Matemática',6,'Resolver e elaborar problemas que envolvam adição ou subtração com números racionais positivos na representação fracionária','EF06MA07');
