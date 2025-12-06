═══════════════════════════════════════════════════════════════════════════
  LIMPEZA INTELIGENTE DO WINDOWS - VERSÃO 2.0 CLI INTERATIVA
═══════════════════════════════════════════════════════════════════════════

🎨 NOVA INTERFACE CLI INTERATIVA
---------------------------------
  ✓ Menu visual com cores
  ✓ Navegação com teclado
  ✓ Marcar/desmarcar itens individualmente
  ✓ Barra de progresso em tempo real
  ✓ Estatísticas de espaço liberado

📋 O QUE O SCRIPT LIMPA
------------------------
  1. ✓ Arquivos Temporários do Windows
  2. ✓ Prefetch do Windows
  3. ✓ Cache de Navegadores (mantém senhas e sessões)
  4. ✓ Cache do Windows Update
  5. ✓ Lixeira
  6. ✓ Cache do Node.js/npm
  7. ⚪ Cache do Docker - Apenas Não Utilizados (desabilitado por padrão)
  8. ⚠️ Docker - REMOVER TUDO (desabilitado por padrão)
  9. ✓ Logs Antigos do Windows (>30 dias)
 10. ✓ Cache de Miniaturas
 11. ⚪ Limpeza de Disco Windows (desabilitado por padrão)

🚀 COMO USAR
------------

OPÇÃO 1 - ÁREA DE TRABALHO (Mais Fácil):
  1. Clique duplo em: "Limpeza Windows.bat" (na área de trabalho)
  2. Aceite as permissões de administrador
  3. Use o menu interativo para escolher o que limpar
  4. Pressione ENTER para confirmar

OPÇÃO 2 - PASTA DO USUÁRIO:
  1. Clique duplo em: "executar_limpeza.bat"
  2. Siga as instruções na tela

OPÇÃO 3 - LINHA DE COMANDO:
  PowerShell como Administrador:
    python C:\Users\pablo\limpar_windows.py

🎮 CONTROLES DO MENU INTERATIVO
--------------------------------
  [1-11]  → Digite o número para marcar/desmarcar item
  [W/K]   → Navegar para cima
  [S/J]   → Navegar para baixo
  [ESPAÇO]→ Marcar/desmarcar item selecionado
  [A]     → Marcar TUDO
  [D]     → Desmarcar TUDO
  [ENTER] → Confirmar seleção e continuar
  [Q]     → Sair

📊 RECURSOS DA INTERFACE
------------------------
  ✓ Cores para facilitar visualização
  ✓ Descrição de cada item de limpeza
  ✓ Checkbox visual [✓] ou [ ]
  ✓ Indicador de seleção atual (→)
  ✓ Barra de progresso animada
  ✓ Contador de espaço liberado por tarefa
  ✓ Total de espaço liberado ao final
  ✓ Tempo de execução

🔒 SEGURANÇA GARANTIDA
----------------------
  ❌ NÃO remove senhas de navegadores
  ❌ NÃO remove sessões (você continua logado)
  ❌ NÃO remove histórico de navegação
  ❌ NÃO remove favoritos/bookmarks
  ❌ NÃO remove programas instalados
  ❌ NÃO remove jogos ou saves
  ❌ NÃO remove documentos pessoais
  ❌ NÃO remove node_modules dos projetos
  ✅ Remove APENAS cache e arquivos temporários

⚡ DETALHES DAS OPÇÕES
----------------------

1. Arquivos Temporários do Windows
   - Limpa: %TEMP%, %TMP%, C:\Windows\Temp
   - Seguro: SIM | Liberação média: 500MB-5GB

2. Prefetch do Windows
   - Limpa: Arquivos .pf de pré-carregamento
   - Seguro: SIM | Liberação média: 50-200MB

3. Cache de Navegadores
   - Limpa: Apenas cache de imagens/scripts
   - MANTÉM: Senhas, cookies, sessões, histórico
   - Navegadores: Chrome, Edge, Firefox, Opera, Brave
   - Seguro: SIM | Liberação média: 500MB-3GB

4. Cache do Windows Update
   - Limpa: Downloads antigos do Windows Update
   - Seguro: SIM | Liberação média: 100MB-2GB

5. Lixeira
   - Esvazia completamente a lixeira
   - Seguro: SIM (revise antes!) | Liberação: varia

6. Cache do Node.js/npm
   - Limpa: Cache global do npm
   - NÃO afeta: node_modules dos seus projetos
   - Seguro: SIM | Liberação média: 100MB-1GB

7. Cache do Docker - Apenas Não Utilizados (DESABILITADO POR PADRÃO)
   - Remove: Containers parados, imagens órfãs, volumes não usados
   - MANTÉM: Containers em execução e imagens em uso
   - Seguro: SIM | Liberação média: 1GB-10GB

8. Docker - REMOVER TUDO ⚠️ (DESABILITADO POR PADRÃO)
   - Remove: TODOS containers (até os em execução)
   - Remove: TODAS imagens (todas mesmo!)
   - Remove: TODOS volumes e build cache
   - ⚠️ ATENÇÃO: Use apenas se quiser resetar o Docker completamente
   - Liberação média: 5GB-50GB+ (pode ser MUITO!)

9. Logs Antigos do Windows
   - Remove: Apenas logs com mais de 30 dias
   - Seguro: SIM | Liberação média: 50-500MB

10. Cache de Miniaturas
    - Limpa: Cache de ícones e thumbnails
    - Seguro: SIM | Liberação média: 50-300MB

11. Limpeza de Disco Windows (DESABILITADO POR PADRÃO)
    - Executa: Utilitário cleanmgr do Windows
    - Pode demorar e abrir janelas extras

⚠️ REQUISITOS
-------------
  • Python 3.6 ou superior
  • Bibliotecas: colorama, tqdm (instaladas automaticamente)
  • Windows 7 ou superior
  • Recomendado: Executar como Administrador

💡 DICAS E RECOMENDAÇÕES
------------------------
  • Feche navegadores antes de executar para melhores resultados
  • Docker opção 7: Seguro, remove apenas recursos não usados
  • Docker opção 8: PERIGOSO! Remove tudo, use apenas para resetar
  • Execute mensalmente para manter o PC otimizado
  • Após executar, reinicie o PC para melhores resultados
  • Se tiver pouco espaço, execute TUDO (exceto Docker opção 8)

⚠️ DIFERENÇA ENTRE AS OPÇÕES DO DOCKER
---------------------------------------
OPÇÃO 7 - Cache do Docker (Apenas Não Utilizados):
  ✓ Remove containers que você parou
  ✓ Remove imagens que não estão sendo usadas
  ✓ Remove volumes órfãos
  ✗ NÃO toca em containers rodando
  ✗ NÃO remove imagens que você está usando
  → SEGURO para usar regularmente

OPÇÃO 8 - Docker REMOVER TUDO ⚠️:
  ✓ Para e remove TODOS os containers
  ✓ Remove TODAS as imagens (até as que você usa)
  ✓ Remove TODOS os volumes (perde dados!)
  ✓ Limpa todo o build cache
  ⚠️ É como resetar o Docker do zero
  → Use apenas se quiser limpar TUDO mesmo

🐛 SOLUÇÃO DE PROBLEMAS
-----------------------

"Python não é reconhecido como comando"
  → Solução: Instale Python de python.org
  → Marque "Add Python to PATH" durante instalação

"Erro ao importar colorama ou tqdm"
  → Solução: Abra CMD/PowerShell e execute:
     pip install colorama tqdm

"Sem permissão para acessar..."
  → Solução: Execute como Administrador
  → Clique direito no .bat → Executar como administrador

"O script abre e fecha rápido"
  → Solução: Execute pelo CMD/PowerShell para ver erros
  → Ou clique direito no .bat → Editar

Cache de navegador não foi removido
  → Solução: Feche todos os navegadores antes de executar
  → Alguns navegadores bloqueiam acesso ao cache quando abertos

Docker: "Nenhum espaço liberado"
  → Normal: Você não tem containers/imagens não utilizados
  → Docker só remove recursos órfãos, não suas imagens ativas

📈 EXEMPLO DE USO
-----------------

1. Execute o script:
   ╔═══════════════════════════════════════════════════╗
   ║      LIMPEZA INTELIGENTE DO WINDOWS               ║
   ║          Versão 2.0 - CLI Interativa              ║
   ╚═══════════════════════════════════════════════════╝

2. Navegue pelo menu e selecione:
   → [✓] 1. Arquivos Temporários do Windows
     [✓] 2. Prefetch do Windows
     [✓] 3. Cache de Navegadores
     [ ] 7. Cache do Docker (Apenas Não Utilizados)  ← Desmarcado
     [ ] 8. Docker - REMOVER TUDO ⚠️  ← Desmarcado (perigoso!)

3. Pressione ENTER e confirme

4. Veja o progresso em tempo real:
   1. Arquivos Temporários do Windows...
   ████████████████████████ 100/100
   ✓ Liberado: 1.25 GB

5. Resultado final:
   ╔═══════════════════════════════════════════════════╗
   ║              LIMPEZA CONCLUÍDA!                   ║
   ╚═══════════════════════════════════════════════════╝

   Total liberado: 3.47 GB
   Tempo decorrido: 45.23 segundos

🔄 ATUALIZAÇÕES VERSÃO 2.0
--------------------------
  ✓ Interface CLI totalmente redesenhada
  ✓ Menu interativo com navegação por teclado
  ✓ Cores e visual melhorado
  ✓ Opções rápidas (Marcar/Desmarcar Tudo)
  ✓ Barra de progresso em tempo real
  ✓ Estatísticas detalhadas por tarefa
  ✓ Confirmação antes de executar
  ✓ Melhor tratamento de erros
  ✓ Arquivo .bat na área de trabalho

═══════════════════════════════════════════════════════════════════════════
  📧 Para suporte, verifique o código em: limpar_windows.py
  🌐 Este script é de código aberto e pode ser modificado livremente
═══════════════════════════════════════════════════════════════════════════
