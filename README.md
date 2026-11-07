# mcLauncher

MVP de launcher/gerenciador para Minecraft Bedrock no Windows 10/11.

## Criar o EXE
1. Instale Python 3.10 ou superior no Windows e marque "Add Python to PATH".
2. Extraia este projeto.
3. Execute `build.bat`.
4. O executável será criado em `dist\mcLauncher.exe`.

## Recursos
- Importa e organiza arquivos `.mcaddon`, `.mcpack` e `.zip`.
- Abre `.mcaddon` e `.mcpack` com o Minecraft para a importação oficial.
- Guarda perfil offline local com nome personalizado.
- Detecta a pasta de dados Bedrock quando acessível.
- Cria/exclui perfis do próprio gerenciador.
- Inicia Minecraft e reinicia o launcher.

## Limitações importantes
- O app não inclui cópias do Minecraft nem baixa versões antigas. Instale o jogo e atualizações pela Microsoft Store/Xbox; a disponibilidade de versões antigas depende dos canais oficiais.
- O perfil offline é apenas um nome local. Não substitui autenticação Microsoft/Xbox e não permite multiplayer online, Realms ou servidores que exigem autenticação.
- O login Microsoft é feito no próprio Minecraft oficial; o app não coleta senha, token ou cookies.
- Excluir um arquivo da lista remove a cópia guardada pelo mcLauncher, não um pacote já importado para dentro do Minecraft. Para remover um pacote importado, use as configurações de armazenamento do Minecraft.
- O gerenciamento de perfis nesta versão ainda não cria instalações independentes do executável Bedrock.

## Segurança
Não insira sua senha Microsoft em aplicativos de terceiros. Use somente a janela de autenticação oficial da Microsoft/Minecraft.


## Compilar automaticamente no Windows usando GitHub Actions
1. Crie um repositório no GitHub e envie todos os arquivos desta pasta para ele.
2. Abra a aba **Actions** do repositório.
3. Selecione **Build mcLauncher for Windows** e clique em **Run workflow** (ou faça push na branch `main`/`master`).
4. Quando terminar, abra a execução concluída e baixe o artefato **mcLauncher-Windows**.
5. Dentro do ZIP baixado estará `mcLauncher.exe`.

A compilação roda em um runner Windows do GitHub Actions; não precisa instalar Python no PC que vai executar o launcher.
