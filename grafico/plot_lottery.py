#!/usr/bin/env python3
"""
Gerador de Gráficos do Lottery Scheduler (Versão Compatível com CSV)
Lê a saída CSV do xv6 e gera gráficos reais de comportamento.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import csv

def parse_csv_output(filename):
    time_points = []
    # Dicionário para armazenar listas de ticks: {'A': [], 'B': [], 'C': []}
    data = {'A': [], 'B': [], 'C': []}
    
    # Configuração dos tickets (fixo conforme o teste em C)
    tickets = {'A': 30, 'B': 20, 'C': 10}
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader) # Pula o cabeçalho: time,A_ticks,B_ticks,C_ticks
            
            for row in reader:
                if len(row) < 4: continue
                try:
                    # O CSV do xv6 pode ter linhas de lixo no inicio/fim, filtramos
                    t = int(row[0])
                    ta = int(row[1])
                    tb = int(row[2])
                    tc = int(row[3])
                    
                    time_points.append(t)
                    data['A'].append(ta)
                    data['B'].append(tb)
                    data['C'].append(tc)
                except ValueError:
                    continue
                    
        return time_points, data, tickets
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        sys.exit(1)

def create_graphs(time_points, data, tickets_info):
    if not time_points:
        print("Nenhum dado encontrado!")
        return

    # Totais finais
    labels = ['A', 'B', 'C']
    final_ticks = [data['A'][-1], data['B'][-1], data['C'][-1]]
    total_ticks = sum(final_ticks)
    total_tickets = sum(tickets_info.values())
    
    # Cores
    colors = {'A': '#3498db', 'B': '#e74c3c', 'C': '#2ecc71'}

    # Configura a figura
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # --- GRÁFICO 1: Evolução Temporal (Real) ---
    ax1 = fig.add_subplot(gs[0, :]) # Ocupa toda a largura superior
    
    for label in labels:
        ax1.plot(time_points, data[label], label=f'Processo {label} ({tickets_info[label]} tkts)', 
                 color=colors[label], linewidth=2)
        
        # Linha de expectativa teórica (pontilhada)
        expected_pct = tickets_info[label] / total_tickets
        expected_line = [t * (total_ticks/time_points[-1]) * expected_pct for t in time_points] 
        # Nota: A linha teórica acima é uma aproximação linear para referência visual
    
    ax1.set_title('Evolução Real dos Ticks (Acumulado)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Tempo (ticks do sistema)', fontsize=11)
    ax1.set_ylabel('Ticks de CPU Recebidos', fontsize=11)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # --- GRÁFICO 2: Distribuição Final (Barras) ---
    ax2 = fig.add_subplot(gs[1, 0])
    
    x = np.arange(len(labels))
    bars = ax2.bar(x, final_ticks, color=[colors[l] for l in labels], alpha=0.8, edgecolor='black')
    
    ax2.set_title('Distribuição Final de CPU', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'Proc {l}\n({tickets_info[l]} tkts)' for l in labels])
    ax2.set_ylabel('Total Ticks')
    
    # Adiciona porcentagens nas barras
    for bar in bars:
        height = bar.get_height()
        pct = (height / total_ticks) * 100
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                 f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')

    # --- GRÁFICO 3: Comparação Real vs Ideal ---
    ax3 = fig.add_subplot(gs[1, 1])
    
    width = 0.35
    real_pcts = [(t/total_ticks)*100 for t in final_ticks]
    ideal_pcts = [(tickets_info[l]/total_tickets)*100 for l in labels]
    
    ax3.bar(x - width/2, real_pcts, width, label='Real', color='#95a5a6')
    ax3.bar(x + width/2, ideal_pcts, width, label='Ideal (Teórico)', color='#34495e', hatch='//')
    
    ax3.set_title('Precisão da Loteria (Real vs Ideal)', fontsize=14, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels)
    ax3.set_ylabel('Porcentagem (%)')
    ax3.legend()
    
    plt.suptitle(f'Análise do Lottery Scheduler (Total Ticks: {total_ticks})', fontsize=16)
    
    output_file = 'lottery_results.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo com sucesso em: {output_file}")
    print("-" * 30)
    print("Resumo Final:")
    for i, l in enumerate(labels):
        print(f"Proc {l}: {real_pcts[i]:.1f}% (Ideal: {ideal_pcts[i]:.1f}%)")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 plot_lottery.py <arquivo_saida_xv6.txt>")
        sys.exit(1)
        
    filename = sys.argv[1]
    time_points, data, tickets = parse_csv_output(filename)
    create_graphs(time_points, data, tickets)

if __name__ == "__main__":
    main()