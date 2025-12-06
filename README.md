# 🧹 Limpeza Inteligente do Windows

Sistema completo de limpeza e otimização do Windows com duas interfaces: **CLI interativa** e **GUI moderna**.

## 📦 Versões Disponíveis

### 🎨 Versão GUI - Interface Gráfica Moderna (Recomendada)
- Interface gráfica moderna com tema escuro
- Checkboxes visuais para cada opção
- Barra de progresso em tempo real
- Log colorido de execução
- Arquivo executável único (.exe)
- **Executa automaticamente como Administrador**
- Não requer Python instalado

### ⌨️ Versão CLI - Interface de Terminal Interativa
- Interface de texto colorida no terminal
- Navegação com teclado (W/S/números)
- Menu interativo com cores
- Barra de progresso
- Requer Python 3.6+

## 🚀 Instalação

### Versão GUI (Executável)

1. Baixe o executável `LimpezaWindows.exe` (~10 MB):
   - **Direto do repositório:** [LimpezaWindows.exe](LimpezaWindows.exe)
   - **Ou clone o repositório:** `git clone git@github.com:pcarvalho-dev/limpar-windows.git`
2. Clique duplo no executável
3. Aceite as permissões de Administrador (UAC)
4. Pronto! Use a interface gráfica

### Versão CLI (Python)

1. Clone o repositório:
```bash
git clone git@github.com:pcarvalho-dev/limpar-windows.git
cd limpar-windows
```

2. Instale as dependências:
```bash
pip install colorama tqdm
```

3. Execute:
```bash
# Windows
python limpar_windows.py

# Ou use o batch
executar_limpeza.bat
```

## 📋 O Que é Limpo

O sistema oferece **11 opções de limpeza**:

1. ✅ **Arquivos Temporários do Windows** - Limpa TEMP, TMP e pastas temporárias
2. ✅ **Prefetch do Windows** - Remove arquivos .pf de pré-carregamento
3. ✅ **Cache de Navegadores** - Chrome, Edge, Firefox, Opera, Brave (mantém senhas e sessões)
4. ✅ **Cache do Windows Update** - Remove downloads antigos
5. ✅ **Lixeira** - Esvazia completamente
6. ✅ **Cache do Node.js/npm** - Limpa cache global (não afeta projetos)
7. ⚪ **Docker - Apenas Não Utilizados** - Remove containers/imagens órfãos (opcional)
8. ⚠️ **Docker - REMOVER TUDO** - Remove TODOS containers, imagens e volumes (opcional, perigoso)
9. ✅ **Logs Antigos do Windows** - Remove logs com mais de 30 dias
10. ✅ **Cache de Miniaturas** - Limpa cache de ícones e thumbnails
11. ⚪ **Limpeza de Disco do Windows** - Executa cleanmgr (opcional)

### 🔒 Segurança Garantida

- ❌ **NÃO** remove senhas de navegadores
- ❌ **NÃO** remove sessões (você continua logado)
- ❌ **NÃO** remove histórico de navegação
- ❌ **NÃO** remove favoritos/bookmarks
- ❌ **NÃO** remove programas instalados
- ❌ **NÃO** remove jogos ou saves
- ❌ **NÃO** remove documentos pessoais
- ❌ **NÃO** remove node_modules dos projetos
- ✅ Remove **APENAS** cache e arquivos temporários

## 💡 Uso

### Versão GUI

```
1. Execute LimpezaWindows.exe
2. Aceite as permissões de Administrador
3. Selecione as opções desejadas (ou clique "Marcar Tudo")
4. Clique em "🚀 INICIAR LIMPEZA"
5. Aguarde a conclusão
```

### Versão CLI

```
1. Execute executar_limpeza.bat (Windows) ou python limpar_windows.py
2. Use W/S ou números para navegar
3. Digite números (1-11) para marcar/desmarcar
4. Pressione ENTER para confirmar
5. Digite 'A' para marcar tudo ou 'D' para desmarcar tudo
```

## 📊 Estatísticas

### Execução Como Administrador vs Normal

| Modo | Tarefas Funcionando | Espaço Liberado |
|------|---------------------|-----------------|
| **Como Admin** | 11/11 (100%) | ~8-10 GB |
| **Usuário Normal** | 5/11 (45%) | ~2-3 GB |

**⚡ Recomendação:** Sempre execute como Administrador para máxima eficiência!

## 🎨 Screenshots

### Interface GUI

![Interface Gráfica](docs/screenshot-gui.png)

- Tema escuro moderno
- Checkboxes visuais
- Log colorido em tempo real
- Barra de progresso

### Interface CLI

![Interface CLI](docs/screenshot-cli.png)

- Menu interativo colorido
- Navegação por teclado
- Barra de progresso
- Estatísticas em tempo real

## 🔧 Compilar Executável

Para compilar o executável GUI você mesmo:

```bash
# Instale PyInstaller
pip install pyinstaller

# Compile com manifest de admin
pyinstaller --onefile --windowed --name="LimpezaWindows" --manifest="admin.manifest" --uac-admin limpar_windows_gui.py

# O executável estará em dist/LimpezaWindows.exe
```

## 📁 Estrutura do Projeto

```
limpar-windows/
├── limpar_windows.py          # Versão CLI
├── limpar_windows_gui.py      # Versão GUI
├── executar_limpeza.bat       # Script batch para CLI
├── admin.manifest             # Manifest para execução como admin
├── README.md                  # Este arquivo
├── README_LIMPEZA.txt         # Manual detalhado CLI
├── README_GUI.txt             # Manual detalhado GUI
└── LEIA-ME_PRIMEIRO.txt       # Guia de escolha de versão
```

## ⚙️ Requisitos

### Versão GUI (Executável)
- Windows 7 ou superior
- Nenhuma dependência (tudo embutido)

### Versão CLI (Python)
- Windows 7 ou superior
- Python 3.6+
- Bibliotecas: `colorama`, `tqdm`

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## ⚠️ Aviso

Este software é fornecido "como está", sem garantias de qualquer tipo. Use por sua própria conta e risco. Sempre faça backup dos seus dados importantes antes de executar ferramentas de limpeza.

## 💡 Dicas

- Execute mensalmente para manter o PC otimizado
- Feche navegadores antes de executar
- Reinicie o PC após a limpeza para melhores resultados
- Docker opção 7 é segura para uso regular
- Docker opção 8 remove TUDO - use apenas se souber o que está fazendo

## 🐛 Problemas Conhecidos

### "Windows protegeu seu PC"
- Normal! O executável não tem assinatura digital
- Clique "Mais informações" → "Executar assim mesmo"
- Totalmente seguro - código aberto disponível

### "Erro de permissão"
- Execute como Administrador
- A versão GUI já faz isso automaticamente

## 📞 Suporte

Para reportar bugs ou sugerir melhorias, abra uma [issue](../../issues).

---

**Desenvolvido com ❤️ para manter seu Windows limpo e rápido!**
