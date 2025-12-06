#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpeza Inteligente do Windows - Interface Gráfica Moderna
Versão GUI com tema escuro e design moderno
EXECUTA SEMPRE COMO ADMINISTRADOR
"""

import os
import shutil
import subprocess
import ctypes
import sys
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


# ============================================================================
# ELEVAÇÃO DE PRIVILÉGIOS
# ============================================================================

def is_admin():
    """Verifica se o script está sendo executado como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Solicita elevação de privilégios e reinicia o programa como admin"""
    try:
        if sys.argv[0].endswith('.py'):
            # Rodando como script Python
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1
            )
        else:
            # Rodando como executável
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, None, None, 1
            )
    except:
        pass
    sys.exit()


# ============================================================================
# FUNÇÕES DE LIMPEZA (MESMAS DA VERSÃO CLI)
# ============================================================================


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


def safe_remove(path):
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
                    # Verifica se é um drive fixo (HD/SSD) usando ctypes
                    drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                    # DRIVE_FIXED = 3 (HD/SSD local)
                    if drive_type == 3:
                        # Tenta obter informações do volume
                        total_bytes = ctypes.c_ulonglong(0)
                        free_bytes = ctypes.c_ulonglong(0)

                        if ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                            drive, None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes)
                        ):
                            total_gb = total_bytes.value / (1024**3)
                            free_gb = free_bytes.value / (1024**3)
                            used_gb = total_gb - free_gb

                            drives.append({
                                'letter': letter,
                                'path': drive,
                                'total_gb': total_gb,
                                'free_gb': free_gb,
                                'used_gb': used_gb,
                                'label': f"{letter}: - {total_gb:.1f} GB ({free_gb:.1f} GB livre)"
                            })
                except:
                    pass
    except:
        # Fallback: pelo menos retorna C:\
        drives.append({
            'letter': 'C',
            'path': 'C:\\',
            'total_gb': 0,
            'free_gb': 0,
            'used_gb': 0,
            'label': 'C: - Drive do Sistema'
        })

    return drives


def clean_temp_folders(selected_drives=None):
    """Limpa pastas temporárias do Windows"""
    if selected_drives is None:
        selected_drives = ['C']

    total_freed = 0

    # Pastas temporárias do usuário (independente de drive)
    user_temp_paths = [
        os.environ.get('TEMP'),
        os.environ.get('TMP'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
    ]

    for temp_path in user_temp_paths:
        if temp_path and os.path.exists(temp_path):
            try:
                for item in os.listdir(temp_path):
                    item_path = os.path.join(temp_path, item)
                    total_freed += safe_remove(item_path)
            except:
                pass

    # Pastas temporárias do sistema em cada drive selecionado
    for drive_letter in selected_drives:
        system_temp = f"{drive_letter}:\\Windows\\Temp"
        if os.path.exists(system_temp):
            try:
                for item in os.listdir(system_temp):
                    item_path = os.path.join(system_temp, item)
                    total_freed += safe_remove(item_path)
            except:
                pass

    return total_freed


def clean_windows_prefetch():
    """Limpa arquivos prefetch do Windows"""
    total_freed = 0
    prefetch_path = 'C:\\Windows\\Prefetch'
    if os.path.exists(prefetch_path):
        try:
            for item in os.listdir(prefetch_path):
                if item.endswith('.pf'):
                    item_path = os.path.join(prefetch_path, item)
                    total_freed += safe_remove(item_path)
        except:
            pass
    return total_freed


def clean_browser_cache():
    """Limpa cache dos navegadores"""
    total_freed = 0
    local_app_data = os.environ.get('LOCALAPPDATA', '')

    browser_caches = [
        os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
        os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
        os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'GPUCache'),
        os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
        os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
        os.path.join(local_app_data, 'Mozilla', 'Firefox', 'Profiles'),
        os.path.join(local_app_data, 'Opera Software', 'Opera Stable', 'Cache'),
        os.path.join(local_app_data, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Cache'),
    ]

    for cache_path in browser_caches:
        if 'Firefox' in cache_path and os.path.exists(cache_path):
            try:
                for profile in os.listdir(cache_path):
                    profile_cache = os.path.join(cache_path, profile, 'cache2')
                    if os.path.exists(profile_cache):
                        total_freed += safe_remove(profile_cache)
            except:
                pass
        elif os.path.exists(cache_path):
            total_freed += safe_remove(cache_path)
    return total_freed


def clean_windows_update_cache():
    """Limpa cache do Windows Update"""
    total_freed = 0
    update_cache = 'C:\\Windows\\SoftwareDistribution\\Download'
    if os.path.exists(update_cache):
        try:
            subprocess.run(['net', 'stop', 'wuauserv'],
                         capture_output=True, timeout=10)
            for item in os.listdir(update_cache):
                item_path = os.path.join(update_cache, item)
                total_freed += safe_remove(item_path)
            subprocess.run(['net', 'start', 'wuauserv'],
                         capture_output=True, timeout=10)
        except:
            pass
    return total_freed


def clean_recycle_bin(selected_drives=None):
    """Esvazia a lixeira"""
    if selected_drives is None:
        selected_drives = ['C']

    total_freed = 0

    # Calcula tamanho de todas as lixeiras
    for drive_letter in selected_drives:
        recycle_bin = f'{drive_letter}:\\$Recycle.Bin'
        if os.path.exists(recycle_bin):
            total_freed += get_folder_size(recycle_bin)

    # Esvazia todas as lixeiras de uma vez
    try:
        # O comando Clear-RecycleBin sem drive específico limpa todas
        subprocess.run(['powershell.exe', '-Command',
                       'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'],
                      capture_output=True, timeout=30)
    except:
        pass

    return total_freed


def clean_node_cache():
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
    except:
        pass

    for cache_path in node_caches:
        if os.path.exists(cache_path):
            total_freed += safe_remove(cache_path)
    return total_freed


def clean_docker_cache():
    """Limpa cache e recursos não utilizados do Docker"""
    try:
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            subprocess.run(['docker', 'container', 'prune', '-f'],
                         capture_output=True, timeout=60)
            subprocess.run(['docker', 'image', 'prune', '-a', '-f'],
                         capture_output=True, timeout=60)
            subprocess.run(['docker', 'volume', 'prune', '-f'],
                         capture_output=True, timeout=60)
            subprocess.run(['docker', 'network', 'prune', '-f'],
                         capture_output=True, timeout=60)
            subprocess.run(['docker', 'system', 'prune', '-a', '-f', '--volumes'],
                          capture_output=True, timeout=120)
    except:
        pass
    return 0


def clean_docker_everything():
    """Remove TUDO do Docker"""
    try:
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            containers_result = subprocess.run(['docker', 'ps', '-aq'],
                                              capture_output=True, timeout=10, text=True)
            if containers_result.stdout.strip():
                container_ids = containers_result.stdout.strip().split('\n')
                subprocess.run(['docker', 'stop'] + container_ids,
                             capture_output=True, timeout=60)
                subprocess.run(['docker', 'rm', '-f'] + container_ids,
                             capture_output=True, timeout=60)

            images_result = subprocess.run(['docker', 'images', '-aq'],
                                          capture_output=True, timeout=10, text=True)
            if images_result.stdout.strip():
                image_ids = images_result.stdout.strip().split('\n')
                subprocess.run(['docker', 'rmi', '-f'] + image_ids,
                             capture_output=True, timeout=120)

            volumes_result = subprocess.run(['docker', 'volume', 'ls', '-q'],
                                           capture_output=True, timeout=10, text=True)
            if volumes_result.stdout.strip():
                volume_ids = volumes_result.stdout.strip().split('\n')
                subprocess.run(['docker', 'volume', 'rm'] + volume_ids,
                             capture_output=True, timeout=60)

            subprocess.run(['docker', 'network', 'prune', '-f'],
                         capture_output=True, timeout=60)
            subprocess.run(['docker', 'builder', 'prune', '-a', '-f'],
                         capture_output=True, timeout=60)
    except:
        pass
    return 0


def clean_windows_logs():
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
                for item in os.listdir(log_path):
                    item_path = os.path.join(log_path, item)
                    if os.path.isfile(item_path):
                        try:
                            mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
                            if datetime.now() - mtime > timedelta(days=30):
                                total_freed += safe_remove(item_path)
                        except:
                            pass
            except:
                pass
    return total_freed


def clean_thumbnail_cache():
    """Limpa cache de miniaturas"""
    total_freed = 0
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    thumbnail_cache = os.path.join(local_app_data, 'Microsoft', 'Windows', 'Explorer')

    if os.path.exists(thumbnail_cache):
        try:
            for item in os.listdir(thumbnail_cache):
                if 'thumbcache' in item.lower() or item.startswith('iconcache'):
                    item_path = os.path.join(thumbnail_cache, item)
                    total_freed += safe_remove(item_path)
        except:
            pass
    return total_freed


def run_disk_cleanup():
    """Executa a limpeza de disco do Windows"""
    try:
        subprocess.run(['cleanmgr', '/sagerun:1'],
                      capture_output=True, timeout=300)
    except:
        pass
    return 0


# ============================================================================
# INTERFACE GRÁFICA MODERNA
# ============================================================================

class CleanupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Limpeza Inteligente do Windows")
        self.root.geometry("900x750")
        self.root.resizable(False, False)

        # Cores do tema escuro moderno
        self.bg_dark = "#1e1e1e"
        self.bg_medium = "#252526"
        self.bg_light = "#2d2d30"
        self.accent = "#007acc"
        self.accent_hover = "#1e90ff"
        self.text_color = "#ffffff"
        self.text_dim = "#969696"
        self.success = "#4ec9b0"
        self.warning = "#ce9178"
        self.danger = "#f48771"

        self.root.configure(bg=self.bg_dark)

        # Define tarefas de limpeza
        self.tasks = [
            {"name": "Arquivos Temporários do Windows",
             "desc": "Limpa TEMP, TMP e pastas temporárias",
             "func": clean_temp_folders,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Prefetch do Windows",
             "desc": "Remove arquivos .pf de pré-carregamento",
             "func": clean_windows_prefetch,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Cache de Navegadores",
             "desc": "Limpa cache (mantém senhas e sessões)",
             "func": clean_browser_cache,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Cache do Windows Update",
             "desc": "Remove downloads antigos do Windows Update",
             "func": clean_windows_update_cache,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Lixeira",
             "desc": "Esvazia a lixeira do Windows",
             "func": clean_recycle_bin,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Cache do Node.js/npm",
             "desc": "Limpa cache do npm (não afeta projetos)",
             "func": clean_node_cache,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Docker - Apenas Não Utilizados",
             "desc": "Remove containers/imagens não utilizados",
             "func": clean_docker_cache,
             "enabled": tk.BooleanVar(value=False)},

            {"name": "Docker - REMOVER TUDO ⚠️",
             "desc": "⚠️ Remove TODOS containers, imagens e volumes",
             "func": clean_docker_everything,
             "enabled": tk.BooleanVar(value=False)},

            {"name": "Logs Antigos do Windows",
             "desc": "Remove logs com mais de 30 dias",
             "func": clean_windows_logs,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Cache de Miniaturas",
             "desc": "Limpa cache de ícones e thumbnails",
             "func": clean_thumbnail_cache,
             "enabled": tk.BooleanVar(value=True)},

            {"name": "Limpeza de Disco do Windows",
             "desc": "Executa o utilitário cleanmgr",
             "func": run_disk_cleanup,
             "enabled": tk.BooleanVar(value=False)},
        ]

        # Detecta drives disponíveis
        self.available_drives = get_available_drives()
        self.drive_vars = {}
        for drive in self.available_drives:
            # C:\ marcado por padrão, outros desmarcados
            default_value = drive['letter'] == 'C'
            self.drive_vars[drive['letter']] = tk.BooleanVar(value=default_value)

        self.is_cleaning = False
        self.create_widgets()

    def create_widgets(self):
        """Cria todos os widgets da interface"""

        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_medium, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🧹 LIMPEZA INTELIGENTE DO WINDOWS",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_medium,
            fg=self.accent
        )
        title_label.pack(pady=(15, 5))

        subtitle_label = tk.Label(
            header_frame,
            text="Versão 2.0 - Interface Gráfica Moderna",
            font=("Segoe UI", 10),
            bg=self.bg_medium,
            fg=self.text_dim
        )
        subtitle_label.pack()

        # Admin warning
        if not is_admin():
            warning_frame = tk.Frame(self.root, bg=self.warning, height=30)
            warning_frame.pack(fill=tk.X, pady=(0, 10))
            warning_frame.pack_propagate(False)

            warning_label = tk.Label(
                warning_frame,
                text="⚠ Execute como Administrador para melhores resultados",
                font=("Segoe UI", 9, "bold"),
                bg=self.warning,
                fg=self.bg_dark
            )
            warning_label.pack(pady=5)

        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Left panel - Checkboxes
        left_panel = tk.Frame(main_container, bg=self.bg_dark, width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas com scroll para as opções
        canvas = tk.Canvas(left_panel, bg=self.bg_dark, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_dark)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Seção de seleção de drives
        drives_frame = tk.Frame(scrollable_frame, bg=self.bg_medium, relief=tk.FLAT)
        drives_frame.pack(fill=tk.X, pady=(0, 10), padx=5)

        drives_header = tk.Label(
            drives_frame,
            text="💾 Selecione os Drives para Limpar:",
            bg=self.bg_medium,
            fg=self.accent,
            font=("Segoe UI", 10, "bold"),
            anchor=tk.W
        )
        drives_header.pack(anchor=tk.W, padx=10, pady=(10, 5))

        drives_desc = tk.Label(
            drives_frame,
            text="Escolha quais HDs/SSDs serão limpos (afeta Temp e Lixeira)",
            bg=self.bg_medium,
            fg=self.text_dim,
            font=("Segoe UI", 8),
            anchor=tk.W
        )
        drives_desc.pack(anchor=tk.W, padx=10, pady=(0, 5))

        # Checkboxes dos drives
        for drive in self.available_drives:
            drive_cb = tk.Checkbutton(
                drives_frame,
                text=drive['label'],
                variable=self.drive_vars[drive['letter']],
                bg=self.bg_medium,
                fg=self.text_color,
                selectcolor=self.bg_light,
                activebackground=self.bg_medium,
                activeforeground=self.accent,
                font=("Segoe UI", 9),
                cursor="hand2",
                relief=tk.FLAT,
                highlightthickness=0
            )
            drive_cb.pack(anchor=tk.W, padx=25, pady=2)

        # Separador
        separator = tk.Frame(scrollable_frame, bg=self.text_dim, height=2)
        separator.pack(fill=tk.X, pady=10, padx=5)

        # Criar checkboxes de tarefas
        for i, task in enumerate(self.tasks):
            self.create_task_checkbox(scrollable_frame, task, i)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Right panel - Log e controles
        right_panel = tk.Frame(main_container, bg=self.bg_medium, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        # Log label
        log_label = tk.Label(
            right_panel,
            text="Log de Execução",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_medium,
            fg=self.text_color
        )
        log_label.pack(pady=(10, 5))

        # Log text
        self.log_text = scrolledtext.ScrolledText(
            right_panel,
            height=20,
            width=45,
            bg=self.bg_light,
            fg=self.text_color,
            font=("Consolas", 9),
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.log_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # Progress bar
        self.progress = ttk.Progressbar(
            right_panel,
            mode='determinate',
            length=360
        )
        self.progress.pack(padx=10, pady=(0, 10))

        # Status label
        self.status_label = tk.Label(
            right_panel,
            text="Pronto para iniciar",
            font=("Segoe UI", 9),
            bg=self.bg_medium,
            fg=self.text_dim
        )
        self.status_label.pack(pady=(0, 10))

        # Bottom buttons
        button_frame = tk.Frame(self.root, bg=self.bg_dark)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Quick select buttons
        quick_frame = tk.Frame(button_frame, bg=self.bg_dark)
        quick_frame.pack(side=tk.LEFT)

        select_all_btn = tk.Button(
            quick_frame,
            text="✓ Marcar Tudo",
            command=self.select_all,
            bg=self.bg_light,
            fg=self.text_color,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        select_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.add_hover_effect(select_all_btn)

        deselect_all_btn = tk.Button(
            quick_frame,
            text="✗ Desmarcar Tudo",
            command=self.deselect_all,
            bg=self.bg_light,
            fg=self.text_color,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        deselect_all_btn.pack(side=tk.LEFT)
        self.add_hover_effect(deselect_all_btn)

        # Action buttons
        action_frame = tk.Frame(button_frame, bg=self.bg_dark)
        action_frame.pack(side=tk.RIGHT)

        self.clean_btn = tk.Button(
            action_frame,
            text="🚀 INICIAR LIMPEZA",
            command=self.start_cleanup,
            bg=self.accent,
            fg=self.text_color,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.clean_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.add_hover_effect(self.clean_btn, self.accent, self.accent_hover)

        exit_btn = tk.Button(
            action_frame,
            text="✕ Sair",
            command=self.root.quit,
            bg=self.bg_light,
            fg=self.text_color,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        exit_btn.pack(side=tk.LEFT)
        self.add_hover_effect(exit_btn)

        self.log("Sistema pronto. Selecione as opções e clique em 'Iniciar Limpeza'.")

    def create_task_checkbox(self, parent, task, index):
        """Cria um checkbox estilizado para cada tarefa"""
        frame = tk.Frame(parent, bg=self.bg_light, relief=tk.FLAT)
        frame.pack(fill=tk.X, pady=5, padx=5)

        # Checkbox
        cb = tk.Checkbutton(
            frame,
            text=f"{index + 1}. {task['name']}",
            variable=task['enabled'],
            bg=self.bg_light,
            fg=self.text_color,
            selectcolor=self.bg_medium,
            activebackground=self.bg_light,
            activeforeground=self.accent,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            highlightthickness=0
        )
        cb.pack(anchor=tk.W, padx=10, pady=(8, 2))

        # Description
        desc_label = tk.Label(
            frame,
            text=task['desc'],
            bg=self.bg_light,
            fg=self.text_dim,
            font=("Segoe UI", 8),
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, padx=30, pady=(0, 8))

    def add_hover_effect(self, button, normal_color=None, hover_color=None):
        """Adiciona efeito hover aos botões"""
        if normal_color is None:
            normal_color = self.bg_light
        if hover_color is None:
            hover_color = self.bg_medium

        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    def log(self, message, color=None):
        """Adiciona mensagem ao log"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")

        if color:
            self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.log_text.insert(tk.END, f"{message}\n", color)
        else:
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")

        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def select_all(self):
        """Marca todas as opções"""
        for task in self.tasks:
            task['enabled'].set(True)
        self.log("✓ Todas as opções foram marcadas")

    def deselect_all(self):
        """Desmarca todas as opções"""
        for task in self.tasks:
            task['enabled'].set(False)
        self.log("✗ Todas as opções foram desmarcadas")

    def start_cleanup(self):
        """Inicia o processo de limpeza"""
        if self.is_cleaning:
            return

        enabled_tasks = [t for t in self.tasks if t['enabled'].get()]

        if not enabled_tasks:
            messagebox.showwarning("Aviso", "Nenhuma opção foi selecionada!")
            return

        # Confirmação
        count = len(enabled_tasks)
        response = messagebox.askyesno(
            "Confirmação",
            f"Você selecionou {count} tarefa(s) para executar.\n\n"
            "Deseja continuar?"
        )

        if not response:
            self.log("Operação cancelada pelo usuário")
            return

        # Inicia limpeza em thread separada
        self.is_cleaning = True
        self.clean_btn.config(state=tk.DISABLED, text="⏳ Limpando...")
        threading.Thread(target=self.run_cleanup, args=(enabled_tasks,), daemon=True).start()

    def run_cleanup(self, enabled_tasks):
        """Executa a limpeza"""
        total_freed = 0
        start_time = time.time()

        # Obtém drives selecionados
        selected_drives = [letter for letter, var in self.drive_vars.items() if var.get()]

        if not selected_drives:
            self.log("⚠ Nenhum drive selecionado! Usando C:\\ por padrão", "warning")
            selected_drives = ['C']

        self.log(f"💾 Drives selecionados: {', '.join([d + ':' for d in selected_drives])}\n")

        self.log("\n" + "="*50)
        self.log("INICIANDO LIMPEZA...", "info")
        self.log("="*50 + "\n")

        total_tasks = len(enabled_tasks)

        for i, task in enumerate(enabled_tasks):
            task_name = task['name']
            self.log(f"\n[{i+1}/{total_tasks}] {task_name}...")
            self.status_label.config(text=f"Limpando: {task_name}")

            try:
                # Funções que precisam de drives selecionados
                if task['func'] in [clean_temp_folders, clean_recycle_bin]:
                    space = task['func'](selected_drives)
                else:
                    space = task['func']()

                total_freed += space

                if space > 0:
                    self.log(f"  ✓ Liberado: {format_bytes(space)}", "success")
                else:
                    self.log(f"  ✓ Concluído", "success")

            except Exception as e:
                self.log(f"  ✗ Erro: {str(e)}", "error")

            # Atualiza progress bar
            progress_value = ((i + 1) / total_tasks) * 100
            self.progress['value'] = progress_value
            self.root.update()

        end_time = time.time()
        duration = end_time - start_time

        # Resultados finais
        self.log("\n" + "="*50)
        self.log("LIMPEZA CONCLUÍDA!", "success")
        self.log("="*50)
        self.log(f"\n✓ Total liberado: {format_bytes(total_freed)}", "success")
        self.log(f"⏱ Tempo: {duration:.2f} segundos")
        self.log("\n💡 Recomendação: Reinicie o computador\n")

        self.status_label.config(text=f"Concluído! {format_bytes(total_freed)} liberados")
        self.clean_btn.config(state=tk.NORMAL, text="🚀 INICIAR LIMPEZA")
        self.is_cleaning = False

        # Mensagem final
        messagebox.showinfo(
            "Limpeza Concluída!",
            f"Limpeza finalizada com sucesso!\n\n"
            f"Espaço liberado: {format_bytes(total_freed)}\n"
            f"Tempo decorrido: {duration:.2f} segundos\n\n"
            f"Recomendação: Reinicie o computador para completar a limpeza."
        )


def main():
    """Função principal"""
    # Verifica se está rodando como admin, senão solicita elevação
    if not is_admin():
        run_as_admin()
        return

    root = tk.Tk()

    # Estilo do tema
    style = ttk.Style()
    style.theme_use('clam')

    # Cores do progressbar
    style.configure("TProgressbar",
                   thickness=20,
                   troughcolor='#2d2d30',
                   background='#007acc',
                   bordercolor='#1e1e1e',
                   lightcolor='#007acc',
                   darkcolor='#007acc')

    # Cria GUI
    app = CleanupGUI(root)

    # Configura tags de cores para o log
    app.log_text.tag_config("success", foreground="#4ec9b0")
    app.log_text.tag_config("error", foreground="#f48771")
    app.log_text.tag_config("warning", foreground="#ce9178")
    app.log_text.tag_config("info", foreground="#007acc")
    app.log_text.tag_config("timestamp", foreground="#969696")

    root.mainloop()


if __name__ == "__main__":
    main()
