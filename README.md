# ProjetoFinal-RAD

#Relatório: Efeito Estufa no Brasil – Projeto Estufatos

# 1. Título do Projeto 
Estufatos 

# 2. Introdução
  O Brasil, com seus vastos biomas e recursos naturais, desempenha um papel vital na regulação climática global. A Amazônia, por exemplo, é um dos principais sumidouros de carbono do planeta, contribuindo para a redução dos impactos das emissões de gases de efeito estufa (GEE). No entanto, o avanço da agropecuária, exploração madeireira e urbanização tem intensificado a degradação ambiental, resultando em um aumento expressivo das emissões de CO₂ e outros GEE. As consequências desse fenômeno afetam não apenas o clima nacional, mas também influenciam padrões climáticos globais.
  Além disso, fatores como queimadas, mudanças no uso do solo e atividades industriais estão entre os principais responsáveis pelo aumento das emissões de carbono no Brasil. Diante desse cenário preocupante, a necessidade de estratégias eficazes de mitigação e adaptação se torna crucial para minimizar os efeitos adversos da crise climática.
  O projeto Estufatos tem como propósito a criação de relatórios detalhados sobre o efeito estufa no Brasil, abordando períodos distintos e diferentes regiões. A análise desses documentos permitirá identificar padrões de emissão, avaliar impactos ambientais e fornece uma base sólida para a formulação de políticas públicas e ações empresariais voltadas para a sustentabilidade.

# 3. Justificativa
  O aumento das emissões de gases de efeito estufa no Brasil e no mundo tem gerado consequências alarmantes, como eventos climáticos extremos, elevação do nível do mar e perda de biodiversidade. A necessidade de medidas eficazes é urgente, e a implementação de tecnologias digitais é uma solução promissora para aprimorar o monitoramento e análise das emissões de carbono.
**Relevância do Projeto:**

●	Desenvolvimento de sistemas automatizados para a coleta e análise de dados climáticos.

●	Aplicabilidade tecnológica para a formulação de políticas públicas e ações empresariais sustentáveis.

●	Incentivo ao avanço científico para melhorar previsões e estratégias de combate às mudanças climáticas.

# 4. Objetivos
**Objetivos principais:**

●	Monitoramento de tendências climáticas: Comparação entre dados históricos e atuais para prever padrões de aquecimento e impactos ambientais.

●	Suporte à tomada de decisão: Facilitação do acesso a informações precisas para governos, empresas e comunidades científicas.

●	Transparência e prestação de contas: Fornecimento de dados concretos sobre a emissão de gases para aprimorar iniciativas de redução de carbono.

**Objetivos Específicos:**

●	Analisar dados de emissões de gases por atividade econômica, produto e tipo de gás.

●	Permitir ao usuário explorar visualmente dados interativos sobre emissões.

●	Desenvolver funcionalidades de cadastro e login para gerenciar o acesso à aplicação.

●	Incorporar mecanismos de CRUD (criar, ler, atualizar, deletar) para usuários e dados de emissões.

●	Integrar visualizações gráficas interativas por meio da biblioteca Plotly

# 5. Base de Dados
  Os dados foram obtidos de um dataset público disponibilizado no site basedosdados.org. O arquivo está formatado como SQL e possui as seguintes colunas: 

●	Id: Identificador único de cada linha (Primary Key).

●	Ano: Informa o ano da emissão.

●	Tipo_emissao: Define se o registro representa emissão, remoção ou compensação.

●	Gás: Tipo de gás de efeito estufa emitido (CO₂, CH₄, etc).

●	Produto: Produto ou processo final responsável pela emissão.

●	Atividade_economica: Setor econômico que gerou a emissão.

●	Emissão: Quantidade de gás emitido.

  Após o pré-processamento, foram removidas colunas redundantes e registros incompletos, resultando em uma base mais enxuta e eficiente para análise.

# 6. Tecnologias Utilizadas
  Este projeto foi construído utilizando uma stack de tecnologias Python focada no desenvolvimento de interfaces gráficas e manipulação de dados.

**Linguagem de Programação:**

●	Python: Linguagem principal utilizada para toda a lógica da aplicação, manipulação de dados e construção da interface gráfica.

**Frameworks e Bibliotecas:**

●	CustomTkinter (ctk): Uma extensão moderna e responsiva do Tkinter, utilizada para construir a interface gráfica de usuário (GUI) da aplicação, proporcionando um visual mais atraente e moderno.

●	Pillow (PIL): Biblioteca para processamento de imagens, utilizada para carregar e redimensionar imagens para a interface.

●	Plotly: Biblioteca poderosa para criação de gráficos interativos e visualizações de dados. Permite a criação de gráficos dinâmicos que podem ser explorados pelo usuário.

●	plotly.express: Módulo de alto nível para gráficos rápidos e expressivos.

●	plotly.graph_objects: Módulo de baixo nível para controle mais granular sobre os elementos do gráfico.

●	Pandas: Biblioteca fundamental para manipulação e análise de dados. Essencial para carregar os dados CSV, realizar filtros e agregar informações antes de visualizá-las.

●	CTkMessagebox: Componente CustomTkinter para exibir caixas de diálogo e mensagens informativas/de erro na aplicação.

●	SQLite3: Módulo embutido do Python para interagir com bancos de dados SQLite. Utilizado para armazenar e recuperar dados, como os parâmetros para geração de gráficos e, futuramente, informações de usuários.

**Ferramentas de Desenvolvimento:**

●	VSCode (Visual Studio Code): Editor de código-fonte utilizado para o desenvolvimento do projeto.

●	Git: Sistema de controle de versão distribuído, utilizado para gerenciar as alterações no código-fonte.

●	GitHub: Plataforma de hospedagem de código-fonte baseada em Git, utilizada para colaboração em equipe, versionamento e distribuição do projeto


# 7. Metodologia de Desenvolvimento 
  Desenvolvimento ágil, priorizamos a entrega de um produto mínimo viável (MVP) que já resolvesse o problema central de forma eficaz. A partir dessa base, novas funcionalidades e melhorias foram adicionadas em iterações subsequentes. Isso permitiu que tivéssemos uma versão funcional rapidamente e nos adaptássemos a feedbacks e novas ideias ao longo do processo.

# 8. Resultados e Funcionalidades 
  O Estufatos oferece uma interface amigável para explorar informações e dados sobre o efeito estufa.
**Funcionalidades Desenvolvidas:**

●	Menu lateral fixo: permite a navegação fácil entre as diferentes seções da aplicação

●	Tela Login: Tela inicial ao abrir a aplicação, traz a necessidade do usuário ter uma conta para acessar a aplicação 

●	Tela Cadastro: Função para caso o usuário não possua conta, permitindo o cadastramento no banco de dados

●	Página “início”: apresenta uma introdução ao efeito estufa, seu funcionamento e os impactos do aquecimento global. Detalha os principais gases do efeito estufa com explicações concisas. Inclui informações sobre picos de emissões no Brasil.

●	Página “Gráficos”: apresenta a visualização interativa de dados de emissões de GEE, onde o usuário pode selecionar intervalo temporal, gases e atividades econômicas para gerar gráficos dinâmicos com Plotly.

●	Página “Usuários”: apresenta o gerenciamento de usuários, permitindo adicionar, ver, editar (com pop-up) e excluir (CRUD) usuários no banco de dados.

●	Página “Dados”: apresenta o gerenciamento de informações do banco de dados principal, permitindo o usuário colaborar com os dados, ao adicionar, ver, editar (com pop-up) e excluir (CRUD) registros sobre emissões no banco de dados.

●	Design Responsivo: o layout do texto e imagens se adapta automaticamente ao redimensionamento da janela, garantindo uma boa experiência visual em diferentes tamanhos.

●	Rolagem de conteúdo: o conteúdo é exibido em um ScrollableFrame, permitindo que o usuário explore todas as informações sem sobrecarga visual.

**Prints das Telas**

![screenshot-paginalogin](https://github.com/user-attachments/assets/d9a41a36-b0fb-4a74-9a4c-3c5c404df231)

![screenshot-paginacadastro](https://github.com/user-attachments/assets/fd1e7bc8-5baf-42bb-83df-164c0c9d8545)

![screenshot-paginainicio](https://github.com/user-attachments/assets/1fb50352-ef49-4a26-8c0a-3d55ecfe2909)

![screenshot-paginagrafico](https://github.com/user-attachments/assets/6f634bfd-f799-4da3-83d2-2d900f3941f5)

![screenshot-paginausuarios](https://github.com/user-attachments/assets/3fec386d-cda2-4ba2-b680-e2f21170593c)

![screenshot-paginadados](https://github.com/user-attachments/assets/8d6dafb9-93c1-414b-91be-d7edac171e3a)

Capturas de tela estarão disponíveis na pasta /screenshots do repositório GitHub:

●	screenshot-paginalogin.png: Demonstração da tela de login

●	screenshot-paginacadastro.png: Demonstração da tela de cadastro

●	screenshot-paginainicio.png: Demonstração do menu lateral e da página inicial.

●	screenshot-paginagrafico.png: Demonstração da página gráficos

●	screenshot-paginausuarios.png: Demonstração da página usuários

●	screenshot-paginadados.png: Demonstração da página dados

# 9. Conclusão
  O desenvolvimento do projeto Estufatos trouxe conhecimentos fundamentais sobre o efeito estufa no Brasil e os desafios enfrentados na mitigação dos impactos climáticos. A implementação de tecnologias inteligentes possibilita um monitoramento mais preciso e um maior embasamento para políticas ambientais eficazes.

**O que foi aprendido?**

●	A influência do desmatamento e das emissões de gases na intensificação do efeito estufa.

●	A importância dos dados climáticos para decisões estratégicas.

●	O papel das tecnologias digitais no monitoramento e previsão de tendências ambientais.

**O que pode ser aprimorado?**

●	Expansão da base de dados para aumentar a precisão das análises.

●	Desenvolvimento de uma plataforma acessível ao público para engajamento social.

●	Automação avançada para otimização da coleta de informações climáticas.

●	Parcerias estratégicas com instituições de pesquisa e ONGs.

  O projeto Estufatos representa um avanço significativo no estudo e mitigação dos impactos do efeito estufa no Brasil. Com aperfeiçoamentos contínuos, poderá se tornar uma referência na geração de dados ambientais confiáveis e acessíveis.

# 10. Repositório Github
**Instruções de Uso**

**Pré-requisitos:**

● Python 3.10 ou superior

● Git instalado (opcional para clonar repositório)

**Instalação:**

● git clone https://github.com/netonio/ProjetoFinal-RAD.git

● cd seu-repositorio (crie uma pasta para armazenar os arquivos)

● pip install -r requirements.txt

**Execução:**

● python main.py

**Estrutura:**

● main.py: Arquivo principal para iniciar a aplicação

● db.py: Módulo responsável pelo banco de dados SQLite

● graficos.py: Geração de gráficos interativos com Plotly

● imagens/: Imagens utilizadas dentro do código

● screenshots/: Capturas de tela do sistema

● relatorio_estufatos.pdf: Arquivo do relatório final

● requirements.txt: Dependências da aplicação

**Relatório:**
[Relatório-Final.docx](https://github.com/user-attachments/files/20684105/Relatorio-Final.docx)
