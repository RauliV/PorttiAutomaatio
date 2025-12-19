#!/usr/bin/env python3
"""
KiCad PDF Export Script
Vie kaikki schematic-arkit PDF-muotoon
"""

import os
import subprocess
import sys
from pathlib import Path

# Projektin tiedot
PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = "PorttiAutomaatio"
EXPORT_DIR = PROJECT_DIR / "exports"

# Arkkitiedostot
SCHEMATICS = [
    f"{PROJECT_NAME}.kicad_sch",  # Pääarkki
    "230v_ac.kicad_sch",
    "12v_dc.kicad_sch",
    "esp32_control.kicad_sch",
]

def find_kicad_cli():
    """Etsi KiCad CLI-työkalu"""
    possible_paths = [
        "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
        "/usr/local/bin/kicad-cli",
        "/opt/homebrew/bin/kicad-cli",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Kokeile löytää PATH:sta
    try:
        result = subprocess.run(["which", "kicad-cli"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

def export_schematic_to_pdf(schematic_file, output_file, kicad_cli):
    """Vie yksittäinen schematic PDF:ksi"""
    cmd = [
        kicad_cli,
        "sch", "export", "pdf",
        "--output", str(output_file),
        str(schematic_file)
    ]
    
    print(f"📄 Viedään: {schematic_file.name} → {output_file.name}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              cwd=PROJECT_DIR)
        if result.returncode == 0:
            print(f"   ✅ Onnistui!")
            return True
        else:
            print(f"   ❌ Virhe: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Poikkeus: {e}")
        return False

def merge_pdfs(pdf_files, output_file):
    """Yhdistä PDF:t (vaatii PyPDF2)"""
    try:
        from PyPDF2 import PdfMerger
        
        merger = PdfMerger()
        for pdf in pdf_files:
            if pdf.exists():
                merger.append(str(pdf))
        
        merger.write(str(output_file))
        merger.close()
        print(f"📚 Yhdistetty PDF: {output_file}")
        return True
    except ImportError:
        print("⚠️  PyPDF2 ei asennettu. Asenna: pip install PyPDF2")
        print("   PDF:t ovat erikseen exports/ kansiossa")
        return False
    except Exception as e:
        print(f"❌ PDF yhdistäminen epäonnistui: {e}")
        return False

def main():
    print("=" * 60)
    print(f"KiCad PDF Export - {PROJECT_NAME}")
    print("=" * 60)
    
    # Etsi KiCad CLI
    kicad_cli = find_kicad_cli()
    if not kicad_cli:
        print("❌ KiCad CLI ei löytynyt!")
        print("   Asenna KiCad: brew install --cask kicad")
        sys.exit(1)
    
    print(f"✅ KiCad CLI löytyi: {kicad_cli}\n")
    
    # Luo export-kansio
    EXPORT_DIR.mkdir(exist_ok=True)
    
    # Vie jokainen arkki
    exported_pdfs = []
    for schematic in SCHEMATICS:
        schematic_path = PROJECT_DIR / schematic
        
        if not schematic_path.exists():
            print(f"⚠️  Tiedosto puuttuu: {schematic}")
            continue
        
        pdf_name = schematic.replace(".kicad_sch", ".pdf")
        pdf_path = EXPORT_DIR / pdf_name
        
        if export_schematic_to_pdf(schematic_path, pdf_path, kicad_cli):
            exported_pdfs.append(pdf_path)
    
    # Yhdistä PDF:t
    if len(exported_pdfs) > 1:
        print("\n" + "=" * 60)
        combined_pdf = EXPORT_DIR / f"{PROJECT_NAME}_complete.pdf"
        merge_pdfs(exported_pdfs, combined_pdf)
    
    print("\n" + "=" * 60)
    print(f"✅ Valmis! PDF:t löytyvät: {EXPORT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
