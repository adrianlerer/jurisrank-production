#!/usr/bin/env python3
"""
Script para recalcular la relevancia jurisprudencial de todas las referencias existentes
con el algoritmo mejorado
"""

import sys
import os
sys.path.append('src')

from bibliography_manager import JurisRankBibliographyManager, BibliographyDatabase, BibliographyAnalyzer

def recalculate_all_relevance():
    """Recalcula la relevancia de todas las referencias en la base de datos"""
    
    print("🔄 Iniciando recálculo de relevancia jurisprudencial...")
    
    # Inicializar componentes usando la misma base de datos que el servicio
    database = BibliographyDatabase("jurisrank_bibliography.db")
    analyzer = BibliographyAnalyzer()
    
    # Obtener todas las referencias
    all_references = database.search_references("")  # Obtiene todas
    
    print(f"📊 Encontradas {len(all_references)} referencias para recalcular")
    
    updated_count = 0
    failed_count = 0
    
    for i, ref in enumerate(all_references, 1):
        try:
            # Calcular nueva relevancia
            old_relevance = ref.jurisprudential_relevance
            new_relevance = analyzer.calculate_jurisprudential_relevance(ref)
            
            if abs(old_relevance - new_relevance) > 0.01:  # Solo actualizar si hay cambio significativo
                ref.jurisprudential_relevance = new_relevance
                
                # Actualizar en base de datos
                if database.update_reference(ref):
                    updated_count += 1
                    print(f"✅ {i:3d}/{len(all_references)} - \"{ref.title[:40]}...\" "
                          f"{old_relevance:.3f} → {new_relevance:.3f}")
                else:
                    failed_count += 1
                    print(f"❌ {i:3d}/{len(all_references)} - Error updating: {ref.title[:40]}...")
            else:
                print(f"➡️  {i:3d}/{len(all_references)} - \"{ref.title[:40]}...\" "
                      f"(sin cambios: {old_relevance:.3f})")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ {i:3d}/{len(all_references)} - Error: {str(e)}")
    
    print(f"\n📋 Resumen del recálculo:")
    print(f"   📊 Total referencias: {len(all_references)}")
    print(f"   ✅ Actualizadas: {updated_count}")
    print(f"   ❌ Fallos: {failed_count}")
    print(f"   ➡️  Sin cambios: {len(all_references) - updated_count - failed_count}")
    
    return updated_count > 0

def test_sample_references():
    """Muestra una muestra de referencias con sus nuevas relevancia"""
    
    print("\n🧪 Muestra de referencias con nueva relevancia:")
    print("=" * 70)
    
    database = BibliographyDatabase("jurisrank_bibliography.db")
    sample_refs = database.search_references("")[:10]  # Primeras 10
    
    for ref in sample_refs:
        print(f"📄 {ref.title}")
        print(f"   👥 {', '.join(ref.authors[:2])}{'...' if len(ref.authors) > 2 else ''}")
        print(f"   📰 {ref.publication}")
        print(f"   ⚖️  Relevancia: {ref.jurisprudential_relevance:.3f}")
        print()

if __name__ == "__main__":
    print("🧬 JurisRank - Recálculo de Relevancia Jurisprudencial")
    print("=" * 60)
    
    try:
        # Recalcular todas las referencias
        success = recalculate_all_relevance()
        
        if success:
            print("\n✅ Recálculo completado exitosamente!")
            
            # Mostrar muestra de resultados
            test_sample_references()
            
            print("\n🌐 Reinicia el servicio para ver los cambios:")
            print("   cd /home/user/webapp && supervisorctl -c supervisord_bibliography.conf restart bibliography_api")
            
        else:
            print("\n⚠️  No se encontraron cambios significativos")
            
    except Exception as e:
        print(f"\n❌ Error durante el recálculo: {str(e)}")
        import traceback
        traceback.print_exc()