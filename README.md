# Avaliação A2 - Paradigmas de Linguagens de Programação

## Grupo F1

### Integrantes:

* Marcelo Martins Farinasso Junior (34061649)

* Gustavo Gimenez (33900515)

* João Pedro Campos Santos (34134271)

## Definição do Tema

* **Paradigma:** Funcional

* **Linguagem:** Haskell

* **Código do Tema:** F1

* **Descrição do Desafio:** Avaliador de expressões aritméticas

## Execução do Código

### Ambiente Online Utilizado:

* [Acesse o projeto no OnlineGDB](https://onlinegdb.com/7TWVmQXO0)

### Instruções de Teste (Entrada e Saída)

1. Abra o link do OnlineGDB.

2. Aperte o botão **Run**.

3. Insira a expressão matemática no terminal (utilizando `*` para multiplicação).

4. O sistema retornará o resultado calculado.

*Escolhemos usar o OnlineGDB pois o Play Haskell executa o código todo de uma vez e não permite o uso da biblioteca interativa para a entrada de dados pelo usuário.*

#### Entrada de Exemplo:

```
1+(2-3)*4

```

#### Saída Esperada:

```
-3

```

## Relatório Técnico

### Descrição da Solução

Como nosso trabalho consiste em uma calculadora, invertemos a ordem comum de precedência de cálculo. O algoritmo analisa o texto da expressão e procura o operador de menor precedência mais à direita (soma e subtração têm menor precedência que multiplicação e divisão, que por sua vez são menores que os parênteses). Quando encontra parênteses, ele ignora o conteúdo interno até que o parêntese seja fechado.

Com o menor cálculo identificado, o algoritmo divide a expressão em duas partes — antes e depois do operador — e chama recursivamente o método da calculadora. Esse processo se repete até restarem apenas números, que são convertidos de texto para valores numéricos, retornando em seguida para resolver todas as operações. Por fim, quando a expressão está cercada por parênteses, o algoritmo remove os parênteses externos e continua o processamento.

## Análise Comparativa

### 1. Sintaxe

Como trabalhamos com Haskell, que é uma linguagem funcional, há algumas peculiaridades estruturais que se aproximam bastante de uma fórmula matemática. Um ponto notável é a chamada de funções:

```
main :: IO () -- Define o tipo do main
main = do     -- Executa as ações em sequência
    putStrLn "Qual sua conta?" 
    conta <- getLine -- Cria a variável conta com o texto inserido pelo usuário
    print (eval conta) -- Chama o print e eval encapsulando a conta corretamente
    -- print eval conta -- Causaria erro de compilação por múltiplos argumentos

```

```
def main():
   print("Qual sua conta")
   conta = input()
   print(eval_expr(conta))

```

Em Haskell, não declaramos explicitamente todos os tipos de forma imperativa; definimos o nome da função, sua estrutura e deixamos que o interpretador deduza o comportamento de acordo com os atributos definidos na chamada:

```
toNum :: String -> Int  -- Define que o método toNum aceita uma String e retorna um Int
toNum [] = 0 -- Caso a String esteja vazia, retorna zero
toNum [x] = digitToInt x -- Se houver apenas um valor, converte para número
toNum (x:xs) = (digitToInt x * 10^(length xs)) + toNum xs -- Calcula multiplicando por 10 e chama recursivamente com o resto da string

```

```
def to_num(s: str) -> int:
   if not s:
       return 0
   if len(s) == 1:
       return int(s[0])
   return (int(s[0]) * (10 ** (len(s) - 1))) + to_num(s[1:])

```

A linguagem não utiliza laços de repetição tradicionais (`for`/`while`). Para percorrer listas, trabalhamos com recursão. Por exemplo, a função `verUlt` (que procura pelo último operador de menor prioridade), que em outra linguagem exigiria um laço imperativo, torna-se a própria estrutura recursiva:

```
verUlt :: String -> Int -> Int -> Int -> Int 
verUlt [] _ ind _ = ind -- Quando a lista acaba, retorna o índice
verUlt (x:xs) ct ind c -- Parâmetros: string dividida, contador, índice e nível
  | x == '(' = achaFim xs (ct + 1) 1 ind c -- Trata os parênteses chamando função específica
  | p >= c && p > 0 = verUlt xs (ct + 1) (ct + 1) p -- Encontra operador de menor ou igual prioridade
  | otherwise = verUlt xs (ct + 1) ind c -- Continua a busca
  where
    p = prioridade x 

```

```
def ver_ult(s: str, ct: int, ind: int, c: int) -> int:
   if not s:
       return ind
   x = s[0]
   xs = s[1:]
   p = prioridade(x)
   if x == "(":
       return acha_fim(xs, ct + 1, 1, ind, c)
   if p >= c and p > 0:
       return ver_ult(xs, ct + 1, ct + 1, p)
   return ver_ult(xs, ct + 1, ind, c)

```

### 2. Semântica

Haskell é uma linguagem fortemente tipada, o que gera a maioria dos erros durante o desenvolvimento. Ela não permite a conversão implícita entre números inteiros e de ponto flutuante sem o tratamento devido, exigindo atenção em divisões. Apesar disso, permite definir tipos genéricos para lidar com situações flexíveis.

Comparado ao C, que é fortemente tipado mas não possui o mesmo sistema de inferência genérica, a escrita em Haskell possui outra dinâmica. Outra característica marcante é a imutabilidade: as variáveis não mudam de valor após definidas. Tentar reatribuir `x = 2` e depois `x = 1` resulta em erro de compilação. As variáveis funcionam como constantes, sendo úteis para representar valores fixos (como constantes matemáticas).

Por fim, Haskell utiliza avaliação preguiçosa (*lazy evaluation*): lê todo o código, mas posterga ao máximo a execução. Funções não avaliadas imediatamente são armazenadas como *thunks* (promessas de execução) e só são computadas quando funções de saída, como `print`, forçam o resultado.

### 3. Gerenciamento de Memória

Diferente do C, que exige gerenciamento manual, Haskell trabalha com gerenciamento automático proporcionado pelo GHC Runtime System.

| Critério | C (Manual) | Haskell (Runtime / GHC) |
| :--- | :--- | :--- |
| **Alocação e Liberação** | Manual via `malloc()`, `calloc()` e `free()`. O programador escolhe o momento exato da desalocação. | Totalmente automática via GHC Runtime System. O programador não manipula ponteiros de forma explícita. |
| **Modelagem de Dados** | Blocos contíguos de bytes. Variáveis locais e *structs* simples vão para a *Stack*; alocações dinâmicas vão para o *Heap*. | Quase tudo no *Heap* é representado como um *Closure* (nó em um grafo de computação, podendo ser um valor calculado ou um *thunk*). |
| **Vazamentos de Memória** | *Memory Leaks*: Ocorrem quando o programador se esquece de dar `free()` num ponteiro alocado no *Heap*. | *Space Leaks*: Ocorrem devido à *Lazy Evaluation*. A memória fica cheia pelo acúmulo de *thunks* não avaliados que mantêm referências ativas. |
| **Segurança (*Memory Safety*)** | Baixa. Suscetível a *Dangling Pointers*, *Buffer Overflow*, *Double Free* e *Use-After-Free*. | Alta (*Memory Safe*). Erros de violação de memória são impossíveis no código Haskell puro em tempo de execução. | 

### 4. Trade-offs

Haskell apresenta vantagens expressivas como a recursividade pura e a avaliação preguiçosa, que permitem estruturar o código sem se prender estritamente à ordem de declaração dos métodos e facilitam a manipulação de expressões. A tipagem estática e polimórfica oferece segurança robusta. A principal barreira é a curva de aprendizado acentuada devido à imutabilidade de variáveis e à ausência de laços imperativos tradicionais, exigindo repensar a lógica algorítmica.

### Resumo da Análise Comparativa

* **Sintaxe:** Modificações pontuais na forma de escrita e grandes alterações estruturais devido à ausência de variáveis mutáveis e laços de repetição.

* **Semântica:** A avaliação preguiçosa traz facilidades no desenvolvimento, e a tipagem forte auxilia na definição rigorosa do escopo.

* **Gerenciamento de Memória:** Automática, porém exige cuidado para evitar o acúmulo de promessas não resolvidas (*thunks*).

* **Trade-offs:** Mais complexa para aplicações comerciais tradicionais, mas excelente como estudo de caso e para o paradigma funcional.

## Log de Uso de Inteligência Artificial (IA)

* **O que foi pedido à IA:** Auxílio na estruturação e formatação em Markdown, além de correções gramaticais e conversão de blocos de código.

* **Qual IA foi utilizada:** Gemini 3 Flash.

* **O que foi aproveitado:** A organização dos tópicos do relatório técnico e a formatação das tabelas e blocos de código em Haskell e Python.

* **O que foi reescrito/entendido pelo grupo:** A adaptação conceitual da lógica da calculadora e a revisão final da análise comparativa para garantir a fidelidade ao projeto desenvolvido.
