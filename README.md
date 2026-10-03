Web XPL Bot



Bot desenvolvido em Python para Telegram, com funcionalidades básicas de reconhecimento e coleta de informações relacionadas a segurança de APIs e aplicações web.



Funcionalidades



O bot possui os seguintes comandos:



/start — inicia o bot e apresenta as opções disponíveis.

/help — mostra a ajuda e os comandos disponíveis.

/nmap <host> — realiza uma varredura básica de portas e serviços utilizando o Nmap.

/gau <domínio> — realiza coleta passiva de URLs relacionadas ao domínio.

/crt <domínio> — consulta informações de Certificate Transparency para identificar subdomínios.

/ipinfo <IP> — consulta informações públicas relacionadas a um endereço IP utilizando o IPinfo.

Tecnologias utilizadas

Python

python-telegram-bot

Telegram Bot API

Nmap

URLScan

Certificate Transparency (CT Logs)

IPinfo

python-dotenv

Requisitos



Para executar o projeto, é necessário ter instalado:



Python 3.x

Nmap

Git

Uma conta/bot do Telegram

Instalação



Clone o repositório:



git clone https://github.com/danilo-intetech/web-xpl-bot.git



Entre na pasta do projeto:



cd web-xpl-bot



Crie um ambiente virtual:



py -m venv venv



Ative o ambiente virtual no Windows com Git Bash:



source venv/Scripts/activate



Instale as dependências:



py -m pip install python-telegram-bot python-dotenv

Configuração do token



O token do Telegram deve ser armazenado em um arquivo .env.



Crie o arquivo:



.env



E adicione:



TELEGRAM\_BOT\_TOKEN=SEU\_TOKEN\_AQUI



O arquivo .env não deve ser enviado para o GitHub.



O projeto utiliza .gitignore para impedir que informações sensíveis, o ambiente virtual e arquivos temporários sejam versionados.



Execução



Com o ambiente virtual ativado, execute:



py bot.py



Se estiver tudo configurado corretamente, será exibida uma mensagem indicando que o bot foi iniciado.



Depois, abra o bot no Telegram e utilize os comandos disponíveis.



Exemplos

Nmap

/nmap localhost



Realiza uma varredura básica no host informado.



Coleta de URLs

/gau example.com



Realiza uma consulta passiva por URLs relacionadas ao domínio.



Certificate Transparency

/crt google.com



Consulta registros públicos de Certificate Transparency para identificar possíveis subdomínios.



IPinfo

/ipinfo 8.8.8.8



Consulta informações públicas sobre o endereço IP informado.



Segurança



Este projeto foi desenvolvido para fins acadêmicos e de aprendizado em segurança de aplicações web e APIs.



As funcionalidades devem ser utilizadas somente em sistemas, hosts e domínios para os quais o usuário tenha autorização.



O token do Telegram não deve ser compartilhado publicamente ou enviado para o repositório.



Estrutura do projeto

web-xpl-bot/

│

├── bot.py

├── .gitignore

├── README.md

├── .env

└── venv/



Os arquivos .env e venv/ são mantidos apenas localmente e não são enviados ao GitHub.



Autor



Projeto acadêmico — Web XPL Bot.



Repositório:



https://github.com/danilo-intetech/web-xpl-bot

