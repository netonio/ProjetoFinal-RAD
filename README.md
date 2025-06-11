# ProjetoFinal-RAD

Estufatos: Análise e Visualização de Emissões de Gases do Efeito Estufa (GEE)
1. Introdução
O Estufatos é uma aplicação de desktop desenvolvida para fornecer informações claras e acessíveis sobre o Efeito Estufa e as emissões de Gases do Efeito Estufa (GEE), com foco especial em dados relevantes para o Brasil. Em um cenário global de crescentes preocupações climáticas, a disponibilidade de dados compreensíveis sobre as emissões é crucial para a conscientização e a tomada de decisões informadas.

O projeto visa resolver o problema da complexidade e dispersão de informações sobre GEEs, oferecendo uma interface intuitiva para visualizar dados históricos e compreender os impactos ambientais. O desenvolvimento rápido de aplicações (RAD) foi essencial para construir esta ferramenta de forma eficiente, permitindo a entrega de uma solução funcional em um curto período, respondendo à urgência do tema.

2. Justificativa
A motivação para o desenvolvimento do Estufatos surgiu da crescente necessidade de democratizar o acesso a dados ambientais e educar o público sobre o aquecimento global. Observamos uma lacuna em ferramentas que unam informações textuais claras com visualizações de dados sobre emissões de GEE de forma interativa e fácil de usar.

O projeto é altamente relevante, pois aborda um dos maiores desafios da atualidade: as mudanças climáticas. Há uma demanda real por ferramentas que auxiliem na compreensão das causas e efeitos dessas mudanças, tanto para estudantes quanto para o público em geral. A aplicabilidade prática reside na sua capacidade de servir como uma ferramenta educacional e de consulta rápida para qualquer pessoa interessada em entender melhor o panorama das emissões e seus impactos.

3. Objetivos
3.1. Objetivo Geral
Desenvolver uma aplicação de desktop interativa e responsiva para apresentar informações sobre o Efeito Estufa e visualizar dados históricos de emissões de Gases do Efeito Estufa (GEE), com foco no contexto brasileiro.

3.2. Objetivos Específicos
Fornecer informações educativas: Apresentar conceitos fundamentais sobre o efeito estufa, seu funcionamento e os principais gases envolvidos.
Visualizar dados de emissões: Implementar funcionalidades para exibir gráficos de emissões de GEE ao longo do tempo, permitindo a seleção de diferentes tipos de gases e metodologias de cálculo.
Garantir responsividade: Assegurar que a interface da aplicação se adapte a diferentes tamanhos de janela, mantendo a usabilidade.
Desenvolver uma interface intuitiva: Criar uma experiência de usuário simples e direta, facilitando a navegação e a compreensão das informações.
Gerenciar dados de usuário (futuro): Implementar uma seção para gerenciamento de usuários, prevendo futuras funcionalidades de personalização ou contribuição.
4. Base de Dados
O projeto utiliza dados sobre emissões de Gases do Efeito Estufa (GEE) provenientes do Sistema de Estimativas de Emissões de Gases de Efeito Estufa (SEEG), iniciativa do Observatório do Clima.

Origem dos Dados: Os dados foram obtidos de um dataset público do SEEG, que compila informações detalhadas sobre as emissões de GEE do Brasil por diferentes setores e gases ao longo dos anos.
Formato dos Dados: Os dados brutos foram baixados em formato CSV (Comma Separated Values), que é um formato tabular amplamente utilizado e fácil de processar.
Principais Colunas e Significado:
Ano: O ano da estimativa de emissão.
Gás: O tipo de GEE (ex: "CO2 (t)", "HFC-125 (t)", "CH4 (t)", "N2O (t)", etc.).
Metodologia/Unidade: Colunas como "CO2e (t) GWP-AR2", "CO2e (t) GWP-AR4", "CO2e (t) GWP-AR5", "CO2e (t) GTP-AR2", "CO2e (t) GTP-AR4", "CO2e (t) GTP-AR5", que indicam a quantidade equivalente de dióxido de carbono (CO2e) com base em diferentes Potenciais de Aquecimento Global (GWP) e Potenciais de Temperatura Global (GTP), e suas respectivas edições dos Relatórios de Avaliação (AR) do IPCC. As colunas como "CO2 (t)", "HFC-125 (t)", etc., representam a emissão do gás em toneladas.
Setores e Fontes: Detalhes sobre a origem da emissão (ex: "Energia", "Agropecuária", "Mudança de Uso da Terra e Florestas").
Outras colunas relevantes que podem ser utilizadas para filtragem e segmentação dos dados.
Pré-processamentos Realizados:
Filtragem de Colunas: Seleção apenas das colunas relevantes para a análise e visualização na aplicação.
Tratamento de Dados Ausentes: Identificação e tratamento (ex: preenchimento ou remoção) de valores nulos, se existirem.
Conversão de Tipos: Garantia de que as colunas numéricas estejam no formato correto para cálculos e plotagem.
Padronização de Nomes: Renomear colunas para facilitar a manipulação e apresentação na interface.
5. Tecnologias Utilizadas
Este projeto foi construído utilizando uma stack de tecnologias Python focada no desenvolvimento de interfaces gráficas e manipulação de dados.

Linguagem de Programação:

Python: Linguagem principal utilizada para toda a lógica da aplicação, manipulação de dados e construção da interface gráfica.
Frameworks e Bibliotecas:

CustomTkinter (ctk): Uma extensão moderna e responsiva do Tkinter, utilizada para construir a interface gráfica de usuário (GUI) da aplicação, proporcionando um visual mais atraente e moderno.
Pillow (PIL): Biblioteca para processamento de imagens, utilizada para carregar e redimensionar imagens para a interface.
Plotly: Biblioteca poderosa para criação de gráficos interativos e visualizações de dados. Permite a criação de gráficos dinâmicos que podem ser explorados pelo usuário.
plotly.express: Módulo de alto nível para gráficos rápidos e expressivos.
plotly.graph_objects: Módulo de baixo nível para controle mais granular sobre os elementos do gráfico.
Pandas: Biblioteca fundamental para manipulação e análise de dados. Essencial para carregar os dados CSV, realizar filtros e agregar informações antes de visualizá-las.
CTkMessagebox: Componente CustomTkinter para exibir caixas de diálogo e mensagens informativas/de erro na aplicação.
SQLite3: Módulo embutido do Python para interagir com bancos de dados SQLite. Utilizado para armazenar e recuperar dados, como os parâmetros para geração de gráficos e, futuramente, informações de usuários.
Ferramentas de Desenvolvimento:

VSCode (Visual Studio Code): Editor de código-fonte utilizado para o desenvolvimento do projeto.
Git: Sistema de controle de versão distribuído, utilizado para gerenciar as alterações no código-fonte.
GitHub: Plataforma de hospedagem de código-fonte baseada em Git, utilizada para colaboração em equipe, versionamento e distribuição do projeto.
6. Metodologia de Desenvolvimento
O projeto foi conduzido com uma abordagem Ágil, focando na entrega iterativa de valor e na adaptação contínua.

Etapas de Desenvolvimento:

Concepção e Prototipagem: Iniciamos com a definição das funcionalidades principais e a criação de protótipos de baixa fidelidade para a interface, testando o fluxo de navegação e a experiência do usuário.
Desenvolvimento Iterativo: As funcionalidades foram implementadas em ciclos curtos, com foco em uma seção por vez (ex: "Página Inicial", "Página de Gráficos").
Testes e Validações: Após cada iteração, foram realizados testes manuais para garantir que as funcionalidades operassem conforme o esperado e que a interface se adaptasse aos redimensionamentos.
Refatoração: O código foi refatorado continuamente para melhorar a legibilidade, performance e manutenção.
Organização do Trabalho em Equipe:

A equipe utilizou o GitHub para colaboração, com branches separadas para novas funcionalidades e revisões de código.
Reuniões periódicas foram realizadas para discutir o progresso, alinhar as tarefas e resolver impedimentos.
A comunicação foi constante para garantir a integração harmoniosa das partes do código.
Abordagem Utilizada:

Desenvolvimento Ágil (com elementos de MVP - Minimum Viable Product): Priorizamos a entrega de um Produto Mínimo Viável (MVP) que já resolvesse o problema central de forma eficaz. A partir dessa base, novas funcionalidades e melhorias foram adicionadas em iterações subsequentes. Isso permitiu que tivéssemos uma versão funcional rapidamente e nos adaptássemos a feedbacks e novas ideias ao longo do processo.
7. Resultados e Funcionalidades
O Estufatos oferece uma interface amigável para explorar informações e dados sobre o efeito estufa.

Funcionalidades Desenvolvidas:
Menu Lateral Fixo: Permite a navegação fácil entre as diferentes seções da aplicação.
Página "Início":
Apresenta uma introdução ao Efeito Estufa, seu funcionamento e os impactos do aquecimento global.
Detalha os principais Gases do Efeito Estufa (GEE) com explicações concisas (CO2, HFC-125, HFC-134a, HFC-143a).
Inclui informações sobre picos de emissões no Brasil.
Design Responsivo: O layout do texto e das imagens se adapta automaticamente ao redimensionamento da janela, garantindo uma boa experiência visual em diferentes tamanhos.
Rolagem de Conteúdo: O conteúdo é exibido em um CTkScrollableFrame, permitindo que o usuário explore todas as informações sem sobrecarga visual.
Página "Gráficos" (Em Desenvolvimento):
Estrutura base para a futura implementação de visualizações interativas de dados de emissões de GEE, onde o usuário poderá selecionar gases, períodos e metodologias para gerar gráficos dinâmicos com Plotly.
Página "Usuários" (Em Desenvolvimento):
Estrutura base para futuras funcionalidades de gerenciamento de usuários, como login, registro e possíveis funcionalidades personalizadas ou de contribuição de dados.
Como as funcionalidades resolvem o problema:
A aplicação Estufatos resolve o problema da complexidade e dispersão de informações sobre o Efeito Estufa ao consolidar conhecimentos essenciais e preparar o terreno para visualizações de dados em uma única interface. A página "Início" já fornece uma base educacional robusta, tornando tópicos complexos acessíveis ao público. A estrutura responsiva e a navegação intuitiva garantem que a informação seja consumida confortavelmente em diferentes configurações de tela.

Prints das Telas (Exemplos a serem incluídos no GitHub/Repositório):
(Aqui você deve descrever onde estarão os screenshots no seu repositório GitHub. Por exemplo:)
Você pode encontrar capturas de tela das principais funcionalidades na pasta screenshots/ do repositório GitHub, incluindo:

screenshot_menu_inicio.png: Demonstração do menu lateral e da página inicial.
screenshot_pagina_inicio_scroll.png: Exemplo da página inicial com conteúdo rolado.
screenshot_responsividade.png: Mostra a adaptação do layout ao redimensionar a janela.
8. Conclusão
O desenvolvimento do projeto Estufatos foi uma jornada de aprendizado valiosa e demonstrou a eficácia do Python e do CustomTkinter para o desenvolvimento rápido de aplicações desktop.

O que foi aprendido?

Aprofundamos o conhecimento em CustomTkinter para criar interfaces modernas e responsivas.
Praticamos a organização de código em classes e módulos para uma aplicação maior.
Refinamos habilidades de manipulação de dados com Pandas e integração com SQLite (para a base de dados de configurações e futuras funcionalidades de usuários).
Compreendemos a importância do design responsivo em aplicações desktop e como implementá-lo.
Ganhamos experiência na integração de bibliotecas de visualização como Plotly em GUIs (mesmo que a parte de gráficos esteja em desenvolvimento, a infraestrutura já está pronta).
Fortalecemos a colaboração utilizando Git e GitHub de forma eficaz.
O que funcionou bem?

A arquitetura modular da aplicação, separando o menu da área de conteúdo, permitiu uma fácil adição de novas páginas.
A implementação da responsividade na Pagina_inicio por meio do método _update_responsive_layout e a recriação das seções funcionou de forma eficiente, adaptando o texto e as imagens ao tamanho da janela.
A integração da Pillow para o carregamento e redimensionamento de imagens se mostrou robusta.
A utilização de CTkScrollableFrame garantiu que todo o conteúdo da página inicial fosse acessível, independentemente da quantidade de texto.
O que poderia ser melhorado?

Implementação completa dos gráficos: A próxima etapa essencial é desenvolver as funcionalidades interativas da página "Gráficos", permitindo ao usuário selecionar e visualizar os dados de emissões de forma dinâmica.
Persistência de dados para configurações: Embora o SQLite esteja configurado, a persistência de configurações de usuário ou preferências de gráficos poderia ser explorada.
Refinamento da UI/UX: Embora funcional, a interface poderia se beneficiar de mais elementos visuais e de uma experiência de usuário ainda mais polida.
Tratamento de erros mais robusto: Expandir o tratamento de exceções para cobrir mais cenários, como falhas na leitura de dados ou problemas de conexão com o banco de dados.
9. Repositório GitHub
Acesse o código-fonte completo do projeto e todas as instruções de uso no repositório GitHub:

Link para o seu Repositório GitHub

(Lembre-se de substituir https://github.com/SEU_USUARIO/SEU_REPOSITORIO pelo link real do seu repositório no GitHub.)

Como usar o projeto:
Clone o repositório:

Bash

git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
Crie e ative um ambiente virtual (recomendado):

Bash

python -m venv venv
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
Instale as dependências:

Bash

pip install -r requirements.txt
(Certifique-se de que o arquivo requirements.txt com o conteúdo fornecido anteriormente esteja na raiz do seu projeto.)

Prepare os dados (se necessário):

Coloque os arquivos de imagem (efeito_estufa.png, funcionamento.png, grafico.png) no mesmo diretório do seu script principal (ou em uma subpasta e ajuste os caminhos no código).
Certifique-se de que seu banco de dados db.py esteja configurado e que o arquivo de dados CSV esteja acessível conforme esperado pelo módulo db.py e graficos.py.
Execute a aplicação:

Bash

python seu_script_principal.py
(Substitua seu_script_principal.py pelo nome do seu arquivo Python que inicia a aplicação, provavelmente o arquivo que contém a classe App e o bloco if _name_ == "_main_":)
