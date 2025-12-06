#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Limpeza do Windows - Interface CLI Interativa
Limpa arquivos temporários, cache e lixo de diversos programas de forma segura
"""

import os
import shutil
import subprocess
import ctypes
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init
from tqdm import tqdm

# Inicializa colorama
init(autoreset=True)


class CleanupTask:
    """Classe para representar uma tarefa de limpeza"""
    def __init__(self, name, description, function, enabled=True):
        self.name = name
        self.description = description
        self.function = function
        self.enabled = enabled
        self.space_freed = 0


def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Imprime o cabeçalho do programa"""
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "╔" + "═" * 78 + "╗")
    print(Fore.CYAN + Style.BRIGHT + "║" + " " * 20 + "LIMPEZA INTELIGENTE DO WINDOWS" + " " * 28 + "║")
    print(Fore.CYAN + Style.BRIGHT + "║" + " " * 25 + "Versão 2.0 - CLI Interativa" + " " * 26 + "║")
    print(Fore.CYAN + Style.BRIGHT + "╚" + "═" * 78 + "╝")
    print()


def is_admin():
    """Verifica se o script está sendo executado como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_folder_size(path):
    """Calcula o tamanho total de uma pasta em bytes"""
    total = 0
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                try:
                    total += entry.stat().st_size
                except:
                    pass
            elif entry.is_dir(follow_symlinks=False):
                total += get_folder_size(entry.path)
    except:
        pass
    return total


def format_bytes(bytes_size):
    """Formata bytes em formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0


def safe_remove(path, pbar=None):
    """Remove arquivos/pastas de forma segura"""
    size_freed = 0
    try:
        if os.path.exists(path):
            size_before = get_folder_size(path)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            size_freed = size_before
            if pbar:
                pbar.update(1)
    except:
        pass
    return size_freed


def get_available_drives():
    """Detecta todos os drives disponíveis no sistema"""
    drives = []
    try:
        import string
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                try:
                    # Verifica se é um drive fixo (HD/SSD)
                    drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                    # DRIVE_FIXED = 3
                    if drive_type == 3:
                        total_bytes = ctypes.c_ulonglong(0)
                        free_bytes = ctypes.c_ulonglong(0)

                        if ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                            drive, None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes)
                        ):
                            total_gb = total_bytes.value / (1024**3)
                            free_gb = free_bytes.value / (1024**3)

                            drives.append({
                                'letter': letter,
                                'path': drive,
                                'total_gb': total_gb,
                                'free_gb': free_gb,
                                'label': f"{letter}: - {total_gb:.1f} GB ({free_gb:.1f} GB livre)"
                            })
                except:
                    pass
    except:
        drives.append({
            'letter': 'C',
            'path': 'C:\\',
            'total_gb': 0,
            'free_gb': 0,
            'label': 'C: - Drive do Sistema'
        })

    return drives


# ============================================================================
# FUNÇÕES DE LIMPEZA
# ============================================================================

def clean_temp_folders(pbar=None, selected_drives=None):
    """Limpa pastas temporárias do Windows"""
    total_freed = 0
    temp_paths = [
        os.environ.get('TEMP'),
        os.environ.get('TMP'),
        'C:\\Windows\\Temp',
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
    ]

    for temp_path in temp_paths:
        if temp_path and os.path.exists(temp_path):
            try:
                items = list(os.listdir(temp_path))
                for item in items:
                    item_path = os.path.join(temp_path, item)
                    total_freed += safe_remove(item_path, pbar)
            except:
                pass

    return total_freed


def clean_windows_prefetch(pbar=None):
    """Limpa arquivos prefetch do Windows"""
    total_freed = 0
    prefetch_path = 'C:\\Windows\\Prefetch'

    if os.path.exists(prefetch_path):
        try:
            items = [i for i in os.listdir(prefetch_path) if i.endswith('.pf')]
            for item in items:
                item_path = os.path.join(prefetch_path, item)
                total_freed += safe_remove(item_path, pbar)
        except:
            pass

    return total_freed


def clean_browser_cache(pbar=None):
    """Limpa cache dos navegadores"""
    total_freed = 0
    local_app_data = os.environ.get('LOCALAPPDATA', '')

    browser_caches = [
        # Chrome
        os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
        os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
        os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'GPUCache'),
        # Edge
        os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
        os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
        # Firefox
        os.path.join(local_app_data, 'Mozilla', 'Firefox', 'Profiles'),
        # Opera
        os.path.join(local_app_data, 'Opera Software', 'Opera Stable', 'Cache'),
        # Brave
        os.path.join(local_app_data, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Cache'),
    ]

    for cache_path in browser_caches:
        if 'Firefox' in cache_path and os.path.exists(cache_path):
            try:
                for profile in os.listdir(cache_path):
                    profile_cache = os.path.join(cache_path, profile, 'cache2')
                    if os.path.exists(profile_cache):
                        total_freed += safe_remove(profile_cache, pbar)
            except:
                pass
        elif os.path.exists(cache_path):
            total_freed += safe_remove(cache_path, pbar)

    return total_freed


def clean_windows_update_cache(pbar=None):
    """Limpa cache do Windows Update"""
    total_freed = 0
    update_cache = 'C:\\Windows\\SoftwareDistribution\\Download'

    if os.path.exists(update_cache):
        try:
            subprocess.run(['net', 'stop', 'wuauserv'],
                         capture_output=True, timeout=10)

            items = list(os.listdir(update_cache))
            for item in items:
                item_path = os.path.join(update_cache, item)
                total_freed += safe_remove(item_path, pbar)

            subprocess.run(['net', 'start', 'wuauserv'],
                         capture_output=True, timeout=10)
        except:
            pass

    return total_freed


def clean_recycle_bin(pbar=None):
    """Esvazia a lixeira"""
    recycle_bin = 'C:\\$Recycle.Bin'
    size_before = get_folder_size(recycle_bin) if os.path.exists(recycle_bin) else 0

    try:
        subprocess.run(['powershell.exe', '-Command',
                       'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'],
                      capture_output=True, timeout=30)
        if pbar:
            pbar.update(1)
    except:
        pass

    return size_before


def clean_node_cache(pbar=None):
    """Limpa cache do Node.js e npm"""
    total_freed = 0
    app_data = os.environ.get('APPDATA', '')
    local_app_data = os.environ.get('LOCALAPPDATA', '')

    node_caches = [
        os.path.join(app_data, 'npm-cache'),
        os.path.join(local_app_data, 'npm-cache'),
        os.path.join(app_data, 'npm'),
    ]

    try:
        subprocess.run(['npm', 'cache', 'clean', '--force'],
                      capture_output=True, timeout=30)
        if pbar:
            pbar.update(1)
    except:
        pass

    for cache_path in node_caches:
        if os.path.exists(cache_path):
            total_freed += safe_remove(cache_path, pbar)

    return total_freed


def clean_docker_cache(pbar=None):
    """Limpa cache e recursos não utilizados do Docker"""
    total_freed = 0

    try:
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, timeout=5)

        if result.returncode == 0:
            subprocess.run(['docker', 'container', 'prune', '-f'],
                         capture_output=True, timeout=60)
            if pbar:
                pbar.update(1)

            subprocess.run(['docker', 'image', 'prune', '-a', '-f'],
                         capture_output=True, timeout=60)
            if pbar:
                pbar.update(1)

            subprocess.run(['docker', 'volume', 'prune', '-f'],
                         capture_output=True, timeout=60)
            if pbar:
                pbar.update(1)

            subprocess.run(['docker', 'network', 'prune', '-f'],
                         capture_output=True, timeout=60)
            if pbar:
                pbar.update(1)

            subprocess.run(['docker', 'system', 'prune', '-a', '-f', '--volumes'],
                          capture_output=True, timeout=120)
            if pbar:
                pbar.update(1)
    except:
        pass

    return total_freed


def clean_docker_everything(pbar=None):
    """Remove TUDO do Docker: containers, imagens, volumes, networks e build cache"""
    total_freed = 0

    try:
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, timeout=5)

        if result.returncode == 0:
            # Para todos os containers em execução
            containers_result = subprocess.run(['docker', 'ps', '-aq'],
                                              capture_output=True, timeout=10, text=True)
            if containers_result.stdout.strip():
                container_ids = containers_result.stdout.strip().split('\n')
                subprocess.run(['docker', 'stop'] + container_ids,
                             capture_output=True, timeout=60)
            if pbar:
                pbar.update(10)

            # Remove TODOS os containers (parados e em execução)
            containers_result = subprocess.run(['docker', 'ps', '-aq'],
                                              capture_output=True, timeout=10, text=True)
            if containers_result.stdout.strip():
                container_ids = containers_result.stdout.strip().split('\n')
                subprocess.run(['docker', 'rm', '-f'] + container_ids,
                             capture_output=True, timeout=60)
            if pbar:
                pbar.update(20)

            # Remove TODAS as imagens
            images_result = subprocess.run(['docker', 'images', '-aq'],
                                          capture_output=True, timeout=10, text=True)
            if images_result.stdout.strip():
                image_ids = images_result.stdout.strip().split('\n')
                subprocess.run(['docker', 'rmi', '-f'] + image_ids,
                             capture_output=True, timeout=120)
            if pbar:
                pbar.update(30)

            # Remove TODOS os volumes
            volumes_result = subprocess.run(['docker', 'volume', 'ls', '-q'],
                                           capture_output=True, timeout=10, text=True)
            if volumes_result.stdout.strip():
                volume_ids = volumes_result.stdout.strip().split('\n')
                subprocess.run(['docker', 'volume', 'rm'] + volume_ids,
                             capture_output=True, timeout=60)
            if pbar:
                pbar.update(20)

            # Remove TODAS as redes (exceto as padrão)
            subprocess.run(['docker', 'network', 'prune', '-f'],
                         capture_output=True, timeout=60)
            if pbar:
                pbar.update(10)

            # Remove build cache
            subprocess.run(['docker', 'builder', 'prune', '-a', '-f'],
                         capture_output=True, timeout=60)
            if pbar:
                pbar.update(10)

    except:
        pass

    return total_freed


def clean_windows_logs(pbar=None):
    """Limpa logs antigos do Windows"""
    total_freed = 0
    log_paths = [
        'C:\\Windows\\Logs',
        'C:\\Windows\\Panther',
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'WebCache'),
    ]

    for log_path in log_paths:
        if os.path.exists(log_path):
            try:
                items = list(os.listdir(log_path))
                for item in items:
                    item_path = os.path.join(log_path, item)
                    if os.path.isfile(item_path):
                        try:
                            mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
                            if datetime.now() - mtime > timedelta(days=30):
                                total_freed += safe_remove(item_path, pbar)
                        except:
                            pass
            except:
                pass

    return total_freed


def clean_thumbnail_cache(pbar=None):
    """Limpa cache de miniaturas"""
    total_freed = 0
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    thumbnail_cache = os.path.join(local_app_data, 'Microsoft', 'Windows', 'Explorer')

    if os.path.exists(thumbnail_cache):
        try:
            items = [i for i in os.listdir(thumbnail_cache)
                    if 'thumbcache' in i.lower() or i.startswith('iconcache')]
            for item in items:
                item_path = os.path.join(thumbnail_cache, item)
                total_freed += safe_remove(item_path, pbar)
        except:
            pass

    return total_freed


def run_disk_cleanup(pbar=None):
    """Executa a limpeza de disco do Windows"""
    try:
        subprocess.run(['cleanmgr', '/sagerun:1'],
                      capture_output=True, timeout=300)
        if pbar:
            pbar.update(1)
    except:
        pass
    return 0


# ============================================================================
# INTERFACE CLI
# ============================================================================

def display_menu(tasks, selected_index):
    """Exibe o menu interativo"""
    print_header()

    if not is_admin():
        print(Fore.YELLOW + "⚠  ATENÇÃO: Execute como Administrador para melhores resultados!")
        print()

    print(Fore.WHITE + Style.BRIGHT + "Selecione os itens para limpar:")
    print(Fore.WHITE + Style.DIM + "Use ↑↓ para navegar, ESPAÇO para marcar/desmarcar, ENTER para continuar")
    print()

    for i, task in enumerate(tasks):
        prefix = "→ " if i == selected_index else "  "
        checkbox = "[✓]" if task.enabled else "[ ]"

        if i == selected_index:
            print(Fore.CYAN + Style.BRIGHT + f"{prefix}{checkbox} {task.name}")
            print(Fore.CYAN + Style.DIM + f"     {task.description}")
        else:
            color = Fore.GREEN if task.enabled else Fore.WHITE + Style.DIM
            print(color + f"{prefix}{checkbox} {task.name}")
            print(Fore.WHITE + Style.DIM + f"     {task.description}")
        print()

    print()
    print(Fore.YELLOW + "Opções rápidas:")
    print(Fore.WHITE + "  [A] Marcar Tudo    [D] Desmarcar Tudo    [Q] Sair")
    print()


def interactive_menu(tasks):
    """Menu interativo para seleção de tarefas"""
    selected_index = 0

    while True:
        display_menu(tasks, selected_index)

        # Lê input do usuário
        print(Fore.CYAN + "Escolha: ", end='', flush=True)

        choice = input().strip().lower()

        if choice == '':  # ENTER
            break
        elif choice == 'q':
            print(Fore.RED + "\nOperação cancelada.")
            sys.exit(0)
        elif choice == 'a':
            for task in tasks:
                task.enabled = True
        elif choice == 'd':
            for task in tasks:
                task.enabled = False
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(tasks):
                selected_index = idx
                tasks[selected_index].enabled = not tasks[selected_index].enabled
        elif choice == 'w' or choice == 'k':  # Cima
            selected_index = (selected_index - 1) % len(tasks)
        elif choice == 's' or choice == 'j':  # Baixo
            selected_index = (selected_index + 1) % len(tasks)
        elif choice == ' ':  # Espaço
            tasks[selected_index].enabled = not tasks[selected_index].enabled

    return tasks


def select_drives_menu():
    """Menu de seleção de drives"""
    drives = get_available_drives()

    if len(drives) == 1:
        # Apenas C:\, retorna automaticamente
        return [drives[0]['letter']]

    print_header()
    print(Fore.CYAN + Style.BRIGHT + "💾 Selecione os Drives para Limpar:\n")
    print(Fore.WHITE + Style.DIM + "(Afeta: Arquivos Temporários e Lixeira)\n")

    drive_selection = {}
    for drive in drives:
        # C:\ marcado por padrão
        drive_selection[drive['letter']] = (drive['letter'] == 'C')
        checkbox = "[✓]" if drive_selection[drive['letter']] else "[ ]"
        color = Fore.GREEN if drive_selection[drive['letter']] else Fore.WHITE
        print(color + f"  {checkbox} {drive['label']}")

    print()
    print(Fore.YELLOW + "Digite as letras dos drives separadas por vírgula (ex: C,D,E)")
    print(Fore.WHITE + "Ou pressione ENTER para usar a seleção atual")
    print()

    choice = input(Fore.CYAN + "Drives: ").strip().upper()

    if choice:
        # Parse da entrada
        selected = []
        for letter in choice.replace(',', ' ').replace(';', ' ').split():
            letter = letter.strip().replace(':', '')
            if letter and any(d['letter'] == letter for d in drives):
                selected.append(letter)

        if selected:
            return selected

    # Retorna drives marcados
    return [letter for letter, enabled in drive_selection.items() if enabled]


def execute_cleanup(tasks, selected_drives=None):
    """Executa a limpeza com barra de progresso"""
    print_header()

    if selected_drives is None:
        selected_drives = ['C']

    enabled_tasks = [t for t in tasks if t.enabled]

    if not enabled_tasks:
        print(Fore.RED + "Nenhuma tarefa selecionada!")
        return

    print(Fore.CYAN + f"💾 Drives selecionados: {', '.join([d + ':' for d in selected_drives])}\n")
    print(Fore.CYAN + Style.BRIGHT + "Iniciando limpeza...\n")

    total_freed = 0
    start_time = time.time()

    for task in enabled_tasks:
        print(Fore.YELLOW + f"\n{task.name}...")

        # Cria barra de progresso
        with tqdm(total=100,
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}',
                 colour='cyan',
                 ncols=70) as pbar:

            try:
                # Funções que precisam de drives
                if task.function in [clean_temp_folders, clean_recycle_bin]:
                    space = task.function(pbar, selected_drives)
                else:
                    space = task.function(pbar)

                task.space_freed = space
                total_freed += space
                pbar.n = 100
                pbar.refresh()
            except Exception as e:
                print(Fore.RED + f"  Erro: {str(e)}")
                continue

        print(Fore.GREEN + f"  ✓ Liberado: {format_bytes(task.space_freed)}")

    end_time = time.time()
    duration = end_time - start_time

    # Resultados finais
    print("\n" + Fore.CYAN + Style.BRIGHT + "╔" + "═" * 78 + "╗")
    print(Fore.CYAN + Style.BRIGHT + "║" + " " * 28 + "LIMPEZA CONCLUÍDA!" + " " * 33 + "║")
    print(Fore.CYAN + Style.BRIGHT + "╚" + "═" * 78 + "╝")
    print()
    print(Fore.GREEN + Style.BRIGHT + f"  Total liberado: {format_bytes(total_freed)}")
    print(Fore.WHITE + f"  Tempo decorrido: {duration:.2f} segundos")
    print()
    print(Fore.YELLOW + "  Recomendação: Reinicie o computador para completar a limpeza")
    print()


def main():
    """Função principal"""

    # Define todas as tarefas disponíveis
    tasks = [
        CleanupTask(
            "1. Arquivos Temporários do Windows",
            "Limpa TEMP, TMP e pastas temporárias do sistema",
            clean_temp_folders,
            True
        ),
        CleanupTask(
            "2. Prefetch do Windows",
            "Remove arquivos .pf de pré-carregamento",
            clean_windows_prefetch,
            True
        ),
        CleanupTask(
            "3. Cache de Navegadores",
            "Limpa cache de Chrome, Edge, Firefox, Opera, Brave (mantém senhas e sessões)",
            clean_browser_cache,
            True
        ),
        CleanupTask(
            "4. Cache do Windows Update",
            "Remove downloads antigos do Windows Update",
            clean_windows_update_cache,
            True
        ),
        CleanupTask(
            "5. Lixeira",
            "Esvazia a lixeira do Windows",
            clean_recycle_bin,
            True
        ),
        CleanupTask(
            "6. Cache do Node.js/npm",
            "Limpa cache do npm (não afeta node_modules dos projetos)",
            clean_node_cache,
            True
        ),
        CleanupTask(
            "7. Cache do Docker (Apenas Não Utilizados)",
            "Remove containers, imagens e volumes não utilizados",
            clean_docker_cache,
            False  # Desabilitado por padrão
        ),
        CleanupTask(
            "8. Docker - REMOVER TUDO ⚠️",
            "⚠️ CUIDADO: Remove TODOS containers, imagens, volumes e builds do Docker",
            clean_docker_everything,
            False  # Desabilitado por padrão
        ),
        CleanupTask(
            "9. Logs Antigos do Windows",
            "Remove logs com mais de 30 dias",
            clean_windows_logs,
            True
        ),
        CleanupTask(
            "10. Cache de Miniaturas",
            "Limpa cache de ícones e thumbnails",
            clean_thumbnail_cache,
            True
        ),
        CleanupTask(
            "11. Limpeza de Disco do Windows",
            "Executa o utilitário cleanmgr do Windows",
            run_disk_cleanup,
            False  # Desabilitado por padrão
        ),
    ]

    # Mostra menu interativo
    tasks = interactive_menu(tasks)

    # Seleção de drives
    selected_drives = select_drives_menu()

    # Confirmação final
    print_header()
    enabled_count = sum(1 for t in tasks if t.enabled)
    drives_str = ', '.join([d + ':' for d in selected_drives])
    print(Fore.YELLOW + f"Você selecionou {enabled_count} tarefa(s) para executar.")
    print(Fore.CYAN + f"Drives a limpar: {drives_str}")
    print()
    confirm = input(Fore.CYAN + "Deseja continuar? (S/n): ").strip().lower()

    if confirm == 'n':
        print(Fore.RED + "\nOperação cancelada.")
        sys.exit(0)

    # Executa a limpeza
    execute_cleanup(tasks, selected_drives)


if __name__ == "__main__":
    try:
        main()
        input(Fore.CYAN + "\nPressione ENTER para sair...")
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nOperação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n\nErro inesperado: {str(e)}")
        input("Pressione ENTER para sair...")
        sys.exit(1)
