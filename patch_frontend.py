#!/usr/bin/env python3
"""
Parches para frontend de Back4App
Modifica los archivos JS para usar URLs relativas
"""

import re
import os

def patch_requirement_rally_js():
    """Parchear requirement-rally.js para usar URLs relativas"""
    js_file = 'requirement-rally-frontend/requirement-rally.js'
    
    if not os.path.exists(js_file):
        print(f"⚠️ File not found: {js_file}")
        return False
    
    try:
        # Leer archivo
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar URL hardcodeada con URL relativa
        old_pattern = r"this\.apiUrl = 'http://127\.0\.0\.1:8001';"
        new_pattern = "this.apiUrl = window.location.origin; // Back4App dynamic URL"
        
        if old_pattern in content or re.search(old_pattern, content):
            content = re.sub(old_pattern, new_pattern, content)
            
            # Escribir archivo parcheado
            with open(js_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Patched {js_file} for Back4App")
            return True
        else:
            print(f"⚠️ Pattern not found in {js_file}")
            return False
            
    except Exception as e:
        print(f"❌ Error patching {js_file}: {e}")
        return False

def patch_usability_universe_js():
    """Verificar que usability-universe.js use configuración dinámica"""
    js_file = 'usability-universe-frontend/usability-universe.js'
    
    if not os.path.exists(js_file):
        print(f"⚠️ File not found: {js_file}")
        return False
    
    try:
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que use window.CONFIG (ya debería estar correcto)
        if 'window.CONFIG' in content and 'API_BASE_URL' in content:
            print(f"✅ {js_file} already using dynamic config")
            return True
        else:
            print(f"⚠️ {js_file} may need manual configuration")
            return False
            
    except Exception as e:
        print(f"❌ Error checking {js_file}: {e}")
        return False

def apply_patches():
    """Aplicar todos los parches necesarios"""
    print("🔧 Applying frontend patches for Back4App...")
    
    patches_applied = 0
    
    if patch_requirement_rally_js():
        patches_applied += 1
    
    if patch_usability_universe_js():
        patches_applied += 1
    
    print(f"✅ Applied {patches_applied} patches")
    return patches_applied > 0

if __name__ == "__main__":
    apply_patches()