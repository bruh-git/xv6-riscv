#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/pstat.h"

#define TICKET_A 30
#define TICKET_B 20
#define TICKET_C 10

// Duração total do teste em ticks (tempo do xv6)
#define TOTAL_TICKS 500 
// Intervalo para imprimir os dados para o gráfico
#define INTERVAL 10     

// Função para gastar CPU (Busy Wait)
void spin() {
    int i = 0;
    while(1) { i++; } // Loop infinito para gastar CPU
    asm volatile("nop");
}

int
main(int argc, char *argv[])
{
  int pid_a, pid_b, pid_c;
  struct pstat st;
  
  printf("Iniciando Lottery Test (CSV mode)...\n");
  
  // Cria Processo A (30 tickets)
  pid_a = fork();
  if(pid_a == 0) {
    settickets(TICKET_A);
    for(;;) spin();
  }
  
  // Cria Processo B (20 tickets)
  pid_b = fork();
  if(pid_b == 0) {
    settickets(TICKET_B);
    for(;;) spin();
  }
  
  // Cria Processo C (10 tickets)
  pid_c = fork();
  if(pid_c == 0) {
    settickets(TICKET_C);
    for(;;) spin();
  }
  
  // --- O PAI (MONITOR) ---
  
  // Cabeçalho para o Excel (CSV)
  printf("time,A_ticks,B_ticks,C_ticks\n");

  int time = 0;
  while(time < TOTAL_TICKS) {
    // 1. Espera um pouco
    pause(INTERVAL);
    time += INTERVAL;

    // 2. Pega as estatísticas atuais
    if(getpinfo(&st) < 0) {
        printf("Erro em getpinfo\n");
        break;
    }

    // 3. Extrai os dados dos filhos
    int ticks_a = 0, ticks_b = 0, ticks_c = 0;
    for(int i = 0; i < NPROC; i++) {
        if(st.inuse[i]) {
            if(st.pid[i] == pid_a) ticks_a = st.ticks[i];
            else if(st.pid[i] == pid_b) ticks_b = st.ticks[i];
            else if(st.pid[i] == pid_c) ticks_c = st.ticks[i];
        }
    }

    // 4. Imprime no formato CSV para o gráfico
    printf("%d,%d,%d,%d\n", time, ticks_a, ticks_b, ticks_c);
  }

  // --- LIMPEZA ---
  kill(pid_a);
  kill(pid_b);
  kill(pid_c);
  wait(0);
  wait(0);
  wait(0);
  
  printf("Teste finalizado.\n");
  exit(0);
}