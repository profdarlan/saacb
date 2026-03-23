"""
Script de Diagnóstico para erro de modelos já registrados em Django
Autor: Assistente SAACB
Data: 2025-12-12

Este script ajuda a identificar:
1. Modelos duplicados em models.py
2. Importações circulares
3. Problemas com INSTALLED_APPS
4. Registros duplicados em admin.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class DiagnosticoDjango:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.warnings = []
        
    def verificar_modelos_duplicados(self):
        """Procura por classes de modelo com mesmo nome em models.py"""
        print("\n" + "="*70)
        print("🔍 VERIFICANDO MODELOS DUPLICADOS")
        print("="*70)
        
        for app_dir in self.project_root.glob("*/models.py"):
            if "__pycache__" in str(app_dir):
                continue
                
            with open(app_dir, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                
            # Procurar por definições de classe
            classes = re.findall(r'^class\s+(\w+)\s*\(', conteudo, re.MULTILINE)
            
            # Encontrar duplicatas
            contador_classes = defaultdict(list)
            for i, classe in enumerate(classes):
                contador_classes[classe].append(i)
            
            # Verificar se há duplicatas
            for classe, posicoes in contador_classes.items():
                if len(posicoes) > 1:
                    msg = f"❌ DUPLICATA ENCONTRADA: Classe '{classe}' definida {len(posicoes)}x em {app_dir}"
                    self.issues.append(msg)
                    print(msg)
        
        if not self.issues:
            print("✅ Nenhum modelo duplicado encontrado")
    
    def verificar_imports_admin(self):
        """Verifica registros duplicados em admin.py"""
        print("\n" + "="*70)
        print("🔍 VERIFICANDO REGISTROS EM admin.py")
        print("="*70)
        
        for admin_file in self.project_root.glob("*/admin.py"):
            if "__pycache__" in str(admin_file):
                continue
                
            with open(admin_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Procurar por admin.site.register
            registros = re.findall(r'admin\.site\.register\((\w+)', conteudo)
            
            # Encontrar duplicatas
            contador = defaultdict(int)
            for registro in registros:
                contador[registro] += 1
            
            for modelo, count in contador.items():
                if count > 1:
                    msg = f"❌ DUPLICATA EM ADMIN: '{modelo}' registrado {count}x em {admin_file}"
                    self.issues.append(msg)
                    print(msg)
        
        if not self.issues:
            print("✅ Nenhum registro duplicado encontrado em admin.py")
    
    def verificar_init_py(self):
        """Verifica importações em __init__.py"""
        print("\n" + "="*70)
        print("🔍 VERIFICANDO __init__.py FILES")
        print("="*70)
        
        for init_file in self.project_root.glob("*/__init__.py"):
            if "__pycache__" in str(init_file):
                continue
                
            with open(init_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Procurar por imports de models
            if 'models' in conteudo or 'from' in conteudo:
                print(f"⚠️  ATENÇÃO: {init_file} contém imports")
                print(f"   Conteúdo:\n{conteudo[:200]}...")
                self.warnings.append(str(init_file))
        
        if not self.warnings:
            print("✅ __init__.py files estão limpos")
    
    def verificar_installed_apps(self):
        """Verifica settings.py para problemas com INSTALLED_APPS"""
        print("\n" + "="*70)
        print("🔍 VERIFICANDO settings.py")
        print("="*70)
        
        settings_paths = [
            self.project_root / "settings.py",
            self.project_root / "config/settings.py",
            self.project_root / "projeto/settings.py"
        ]
        
        for settings_file in settings_paths:
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                
                # Procurar INSTALLED_APPS
                if 'INSTALLED_APPS' in conteudo:
                    # Extrair seção INSTALLED_APPS
                    match = re.search(
                        r'INSTALLED_APPS\s*=\s*\[(.*?)\]',
                        conteudo,
                        re.DOTALL
                    )
                    
                    if match:
                        apps_section = match.group(1)
                        apps = re.findall(r"['\"]([^'\"]+)['\"]", apps_section)
                        
                        # Verificar duplicatas
                        contador = defaultdict(int)
                        for app in apps:
                            contador[app] += 1
                        
                        print(f"✅ Aplicativos encontrados em INSTALLED_APPS:")
                        for app, count in contador.items():
                            if count > 1:
                                msg = f"   ❌ DUPLICATA: '{app}' listado {count}x"
                                print(msg)
                                self.issues.append(msg)
                            else:
                                print(f"   ✅ {app}")
                        
                        # Verificar se contenttypes está antes de apps customizados
                        if apps[0] != 'django.contrib.contenttypes':
                            self.warnings.append(
                                "⚠️  django.contrib.contenttypes deveria estar primeiro"
                            )

    def verificar_importacoes_circulares(self):
        """Verifica possíveis importações circulares"""
        print("\n" + "="*70)
        print("🔍 VERIFICANDO IMPORTAÇÕES POTENCIALMENTE CIRCULARES")
        print("="*70)
        
        # Criar mapa de importações
        imports_map = defaultdict(set)
        
        for py_file in self.project_root.glob("*/*.py"):
            if "__pycache__" in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                
                # Procurar por imports (simplificado)
                imports = re.findall(
                    r'^(?:from|import)\s+(?:\.+)?(\w+)',
                    conteudo,
                    re.MULTILINE
                )
                
                app_name = py_file.parent.name
                for imp in imports:
                    if imp != app_name:  # Ignorar auto-imports
                        imports_map[app_name].add(imp)
            
            except Exception as e:
                pass
        
        print("📊 Mapa de Importações:")
        for app, imports in sorted(imports_map.items()):
            print(f"   {app}: {', '.join(sorted(imports))}")
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        print("\n" + "="*70)
        print("📋 RELATÓRIO FINAL")
        print("="*70)
        
        if self.issues:
            print(f"\n❌ PROBLEMAS ENCONTRADOS ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   {issue}")
        else:
            print("\n✅ Nenhum problema crítico encontrado")
        
        if self.warnings:
            print(f"\n⚠️  AVISOS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
        
        print("\n" + "="*70)
    
    def executar(self):
        """Executa todos os testes"""
        print("\n🚀 INICIANDO DIAGNÓSTICO DJANGO\n")
        
        self.verificar_modelos_duplicados()
        self.verificar_imports_admin()
        self.verificar_init_py()
        self.verificar_installed_apps()
        self.verificar_importacoes_circulares()
        self.gerar_relatorio()


if __name__ == "__main__":
    # Ajuste o caminho para sua projeto
    project_root = r"C:\Users\profd\OneDrive\Documentos\Python\projeto-saacb"
    
    diagnostico = DiagnosticoDjango(project_root)
    diagnostico.executar()
