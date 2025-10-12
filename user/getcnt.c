#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  if(argc != 2){
    fprintf(2, "Uso: getcnt <numero_da_syscall>\n");
    exit(1);
  }

  int syscall_num = atoi(argv[1]);
  int count = getcnt(syscall_num);

  if (count < 0) {
    fprintf(2, "Numero de syscall inválido.\n");
    exit(1);
  }

  printf("syscall %d foi chamado %d vezes\n", syscall_num, count);

  exit(0);
}