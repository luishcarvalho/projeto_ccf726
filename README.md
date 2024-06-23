# Projeto de Engenharia de Aprendizado de Máquina (CCF 726): Customização de Modelo para Contratos Inteligentes em *Blockchain*
Este repositório contém o código e os recursos relacionados ao projeto da disciplina CCF726 - Engenharia de Aprendizado de Máquina com foco na customização de um modelo de Inteligência Artificial generativa para lidar com contratos inteligentes de *blockchain* escritos em *Solidity*. A documentação do projeto encontra-se disponível no [repositório](https://github.com/luishcarvalho/projeto_ccf726/blob/main/Especifica%C3%A7%C3%B5es%20do%20Projeto.pdf).

## Objetivo do Projeto
O projeto tem como objetivo desenvolver e implementar um modelo de IA Generativa capaz de interpretar e interagir com contratos inteligentes de *blockchains* escritos em *Solidity*, uma linguagem de programação comum para contratos na *blockchain* *Ethereum*. Inicialmente o objetivo era treinar o modelo para analisar e compreender os padrões e requisitos presentes nos contratos, permitindo uma automação na detecção de vulnerabilidades presentes nos mesmos. Por fim, esse modelo deve ser implementado em uma nuvem AWS de modo que fique disponível e possa ser acessado remotamente.

## Dados Utilizados
Foi utilizado o conjunto de contratos auditados pela ferramenta Slither para treinamento do modelo. Este conjunto de dados contém o código-fonte dos contratos que foram juntamente de uma classificação de suas vulnerabilidades de acordo com a ferramenta. Os arquivos e mais informações sobre o conjunto de dados podem ser encontrados na plataforma [*Hugging Face*](https://huggingface.co/datasets/mwritescode/slither-audited-smart-contracts)[1].

> [Slither](https://github.com/crytic/slither) [6] é uma ferramenta de análise estática de contratos inteligentes escrita em Solidity. Desenvolvida para detectar vulnerabilidades, otimizar código e garantir a segurança em contratos inteligentes na blockchain Ethereum, o Slither é amplamente utilizado por desenvolvedores e auditores para identificar problemas comuns, como reentrância, estouros de inteiros e falhas de acesso, entre outros. Além de fornecer diagnósticos detalhados sobre o código analisado, ele também oferece sugestões de melhorias, contribuindo para o desenvolvimento de contratos mais seguros e eficientes.

Este dataset contém mais de 110 mil linhas (totalizando em tamanho cerca de 6,5Gb). A tabela abaixo apresenta as colunas e suas descrições. Para este projeto, foram utilizados somente os campos de código fonte e vulnerabilidade detectada usados como contexto e resposta respectivamente.


| **Coluna**  | **Descrição**                                                                                   |
|-------------|-------------------------------------------------------------------------------------------------|
| address     | Uma string representando o endereço de localização do contrato inteligente na main net Ethereum |
| source_code | Uma versão simplificada do código fonte do contrato inteligente no Solidity.                    |
| bytecode    | Uma string representando o bytecode do contrato inteligente                                     |
| slither     | Resultado da detecção da ferramenta                                                             |

A ideia inicial para este projeto seria analisar códigos contendo todas as vulnerabilidades presentes na ferramenta, entretanto, por limitações computacionais e de tempo, o dataset foi reajustado para conter cerca de 500 contratos com pelo menos a vulnerabilidade reentrância (*reentrancy*) e 500 seguros. A escolha dessa vulnerabilidade em específico se dá pelo fato de ser um ataque bastante comum e devastador quando executado corretamente. 

> A vulnerabilidade de reentrância é um tipo de ataque em contratos inteligentes onde um contrato malicioso pode fazer várias chamadas recursivas a um contrato alvo antes que a execução da função anterior seja concluída. Isso permite que o atacante retire fundos repetidamente, explorando a falta de atualização adequada do estado do contrato entre essas chamadas. Como exemplo, pode-se citar o [ataque ao The DAO em 2016](https://medium.com/@infinblock/the-dao-hack-and-reentrancy-attacks-b27bb84867f6) [5] , que resultou na perda de cerca de 60 milhões de dólares em Ether. Devido à sua gravidade e à facilidade com que pode ser explorada se o código não for cuidadosamente escrito e auditado, a reentrância é considerada uma das vulnerabilidades mais críticas na segurança de contratos inteligentes.

Vale ressaltar que todos os dados foram manejados em arquivos do tipo parquet tanto pela velocidade de leitura como tamanho final do conjunto de dados. Mesmo limitando o dataset a apenas 1000 linhas, foram necessárias várias adaptações para que fosse possível o treinamento do modelo. Dito isso, foram escolhidos somente os 1000 contratos com menor tamanho de código fonte além de retirada de comentários do código e new lines ('\n') numa tentativa de fazer possível o treinamento. 

## Modelo
Neste trabalho, o modelo Tiny LLaMA foi utilizado. Ele é uma versão reduzida do modelo de linguagem LLaMA (Large Language Model for AI) desenvolvido pela [Meta](https://llama.meta.com/) [2] e foi projetado para operar com menos recursos computacionais enquanto mantém uma alta capacidade de processamento de linguagem natural.  

A proposta é que, ao analisar um contrato, o Tiny LLaMA aprende a identificar padrões e anomalias que podem indicar a presença de falhas de segurança. Trabalhos como [3] e [4] utilizam o ChatGPT para detectar vulnerabilidades e também gerar relatórios sobre o contrato em si, porém, se trata de um modelo que apesar de apresentar bons resultados, não foi projetado para essa tarefa. A aplicação do Tiny LLaMA em específico, visa modelar um modelo de IA Generativa de pouco custo computacional mas que consiga melhorar a segurança e a confiabilidade de contratos inteligentes.

## Desenvolvimento
O trabalho foi desenvolvido tanto na plataforma colab do google quanto localmente por meio de notebooks Jupyter. Por conta do tamanho do dataset, a parte de pré processamento dos dados foi feita em grande parte localmente utilizando bibliotecas básicas como numpy, pandas etc. A parte de treinamento do modelo e ajuste de hiperparâmetros foi feita no google colab, rodando na GPU T4.

Se tratando do modelo em si, algumas alterações nos hiperparâmetros foram feitas para que a VRAM da GPU não estourasse antes mesmo do treinamento (como batch size e steps). Uma outra estratégia também foi aplicada, utilizando-se de checkpoints para continuar o treinamento. No caso deste trabalho, ao atingir cerca de 250 steps (aproximadamente 2 horas) o tempo de execução máximo para a GPU era atingido, então antes do tempo acabar, o último checkpoint de treino era salvo e continuado depois ou em outra conta.

No final, não foram obtidos resultados satisfatórios mesmo depois de tantas adaptações e mudanças não só no dataset como no modelo. Analisando o caso como um todo, uma das principais causas pode ter sido o dataset que, por ser muito grande, dificultou não só o manejo e processamento dos dados mas também o treinamento do modelo.

Para que pudesse funcionar na instância AWS, o modelo final foi então enviado para um repositório na plataforma HuggingFace e convertido para um arquivo GGUF (GPT-Generated Unified Format) para ser executado remotamente, via internet.

## Considerações Finais
Atualmente, os LLMs têm ganhado destaque devido tanto pela sua capacidade de processamento avançado quanto a automação de tarefas até a análise de grandes volumes de dados textuais. Modelos como o GPT-4, LLaMA e Copilot demonstram com clareza as oportunidades e as possibilidades da inteligência artificial. Aprofundar nesses temas, em minha opinião, é de suma importância considerando o rápido crescimento dessas tecnologias que estão sendo adaptadas e melhoradas cada dia mais. 

Implementar um modelo de LLM no contexto de contratos inteligentes em _blockchain_ apresentou um aprendizado valioso, tanto em termos de compreensão dos modelos quanto na adaptação às necessidades específicas de análise de segurança em contratos _Solidity_. Creio veementemente que o projeto me auxiliou bastante principalmente na minha pesquisa de mestrado. Durante o desenvolvimento, a configuração e otimização do modelo se mostrou um desafio visível, especialmente no que tange à limitação de recursos computacionais e ao manejo eficiente do dataset. A implementação na AWS trouxe suas próprias dificuldades também, tendo em vista que foi meu primeiro contato com essa tecnologia. Essas experiências mostraram as complexidade  associadas ao uso de LLMs  ao mesmo tempo que destacam a potencialidade de tais modelos em automatizar e aprimorar a detecção de vulnerabilidades em contratos inteligentes.

## Referências
[1] **Dataset Card for Slither Audited Smart Contracts -  Hugging Face**. Disponível em: <https://huggingface.co/datasets/mwritescode/slither-audited-smart-contracts>. Acesso em: 19 jun. 2024.

[2] **Llama**. Disponível em: <https://llama.meta.com>.

[3] CHEN, Chong et al. **When chatgpt meets smart contract vulnerability detection: How far are we?**. arXiv preprint arXiv:2309.05520, 2023.

[4] BOI, Biagio; ESPOSITO, Christian; LEE, Sokjoon. **VulnHunt-GPT: a Smart Contract vulnerabilities detector based on OpenAI chatGPT.** In: Proceedings of the 39th ACM/SIGAPP Symposium on Applied Computing. 2024. p. 1517-1524.

[5] INFINBLOCK, K. MARSONIA-.  **The DAO Hack and Reentrancy Attacks**. Disponível em: <https://medium.com/@infinblock/the-dao-hack-and-reentrancy-attacks-b27bb84867f6>. Acesso em: 23 jun. 2024.

[6] **Slither**. Disponível em: <https://github.com/crytic/slither>.
