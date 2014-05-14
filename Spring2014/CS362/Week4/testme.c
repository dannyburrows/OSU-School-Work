#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<time.h>

char inputChar()
{
    // TODO: rewrite this function
  int val;
  char c;

  val = rand() % 9;
  switch (val) {
    case 0:
      c = '[';
      break;

    case 1:
      c = '(';
      break;

    case 2:
      c = '{';
      break;

    case 3:
      c = ' ';
      break;

    case 4:
      c = 'a';
      break;

    case 5:
      c = 'x';
      break;

    case 6:
      c = '}';
      break;

    case 7:
      c = ')';
      break;

    case 8:
      c = ']';
      break;
  }

  return c;
}

char *inputString()
{
    // TODO: rewrite this function
    return "";
}

void testme()
{
  int tcCount = 0;
  char *s;
  char c;
  int state = 0;
  while (1)
  {
    tcCount++;
    c = inputChar();
    s = inputString();
    printf("Iteration %d: c = %c, s = %s, state = %d\n", tcCount, c, s, state);

    if (c == '[' && state == 0) state = 1;
    if (c == '(' && state == 1) state = 2;
    if (c == '{' && state == 2) state = 3;
    if (c == ' '&& state == 3) state = 4;
    if (c == 'a' && state == 4) state = 5;
    if (c == 'x' && state == 5) state = 6;
    if (c == '}' && state == 6) state = 7;
    if (c == ')' && state == 7) state = 8;
    if (c == ']' && state == 8) state = 9;
    if (s[0] == 'r' && s[1] == 'e'
       && s[2] == 's' && s[3] == 'e'
       && s[4] == 't' && s[5] == '\0'
       && state == 9)
    {
      printf("error ");
      exit(200);
    }
  }
}


int main(int argc, char *argv[])
{
    srand(time(NULL));
    testme();
    return 0;
}
