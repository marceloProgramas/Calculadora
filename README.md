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

* [Acesse o projeto no PlayHaskell](https://play.haskell.org/saved/lexsPuxM)

### Instruções de Teste (Entrada e Saída)

1. Abra o link do OnlineGDB.

2. Insira a expressão aritmética no na variável conta entre as aspas duplas(utilizando `*` para multiplicação).

3. Aperte o botão **Run**.

4. O sistema retornará o resultado calculado.

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

semelhante ao Python, Haskell trabalha com gerenciamento automático proporcionado pelo GHC Runtime System.

| Critério | Python (CPython) | Haskell (GHC Runtime) |
| :--- | :--- | :--- |
| **Mecanismo do GC** | Contagem de Referências (Reference Counting) como mecanismo principal, auxiliado por um GC cíclico para detectar referências circulares. | Garbage Collector Copiador e Generacional baseado em rastreamento (tracing). Não utiliza contagem de referências. |
| **Momento de Liberação** | Imediato: Na maioria dos casos, quando a contagem de referências de um objeto chega a zero, ele é desalocado instantaneamente na memória. | Pausado/Por Lotes: A memória não é liberada imediatamente ao perder a referência; a varredura e liberação ocorrem em ciclos organizados pelas gerações do GC. |
| **Mutabilidade x Imutabilidade** | Permite objetos mutáveis por padrão (listas, dicionários). Modificações ocorrem diretamente no local de memória (in-place). | Dados são estritamente imutáveis. Alterar uma estrutura gera novos nós no Heap que compartilham referências com a estrutura antiga (structural sharing). |
| **Estrutura de Avaliação** | Avaliação Estrita (Eager Evaluation): As expressões e argumentos são calculados imediatamente ao serem declarados ou passados para funções. | Avaliação Preguiçosa (Lazy Evaluation): Cria thunks (promessas de cálculo) no Heap. A memória armazena o grafo do cálculo pendente até que o valor seja estritamente necessário. |
| **Sobrecarga de Alocação** | Objetos em Python têm alto overhead devido aos cabeçalhos PyObject (para manter contagem de referências e tipo dinâmico). | Variáveis são empacotadas (boxed closures) para suportar thunks, mas o GHC realiza otimizações agressivas de compilação nativa para reduzir essa sobrecarga. |
### 4. Trade-offs

Haskell apresenta vantagens expressivas como a recursividade pura e a avaliação preguiçosa, que permitem estruturar o código sem se prender estritamente à ordem de declaração dos métodos e facilitam a manipulação de expressões. A tipagem estática e polimórfica oferece segurança robusta. A principal barreira é a curva de aprendizado acentuada devido à imutabilidade de variáveis e à ausência de laços imperativos tradicionais, exigindo repensar a lógica algorítmica.

### Resumo da Análise Comparativa

* **Sintaxe:** Modificações pontuais na forma de escrita e grandes alterações estruturais devido à ausência de variáveis mutáveis e laços de repetição.

* **Semântica:** A avaliação preguiçosa traz facilidades no desenvolvimento, e a tipagem forte auxilia na definição rigorosa do escopo.

* **Gerenciamento de Memória:** Automática, porém exige cuidado para evitar o acúmulo de promessas não resolvidas (*thunks*).

* **Trade-offs:** Mais complexa para aplicações comerciais tradicionais, mas excelente como estudo de caso e para o paradigma funcional.

## Log de Uso de Inteligência Artificial (IA)

**O que foi pedido à IA:** Utilizamos para tirar dúvidas sobre métodos da própria linguagem.
**Qual IA foi utilizada:** Google Gemini<br>
**O que foi aproveitado:** Usamos esses métodos em diversas funções. Exemplos de métodos: `digitToInt`, `length`, `filter`, `any`, entre outros.<br>
**O que foi entendido pelo grupo:** Temos diversos métodos pré-existentes para lidar com situações como limpar uma string ou verificar o que tem dentro. Exemplo:
```haskell
temOper :: String -> Bool
temOper = any (`elem` "+-*/()")

```
Caso utilizássemos a função `any`, teríamos que fazer uma recursão para olhar toda a string.

---

**O que foi pedido à IA:** Tem como eu mapear alguns caracteres para que a linguagem verifique qual tem o maior valor e dê prioridade para ele?<br>
**Qual IA foi utilizada:** Google Gemini<br>
**O que foi aproveitado:** Ela deu algumas ideias de funções que pudessem ser usadas; uma delas foi o método `prioridade`.<br>
**O que foi reescrito pelo grupo:** Modificamos o método `prioridade` para ficar mais fácil de lidar.<br>

---

**O que foi pedido à IA:** Quero fazer uma condição primária e depois algumas condições secundárias.<br>
**Qual IA foi utilizada:** Google Gemini<br>
**O que foi aproveitado:** Explicou sobre como no Haskell os métodos dão prioridade.<br>
**O que foi entendido pelo grupo:** Dando prioridade ao que é escrito primeiro e depois verificando os outros, fazendo termos que modificar a ordem de alguns *guards* e de formas de alguns métodos.<br>

---

**O que foi pedido à IA:** Tenho um problema, como eu faço para caso eu precise tirar dois fins de parênteses como nesse código?<br>
**Qual IA foi utilizada:** Google Gemini<br>
**O que foi aproveitado:** Ele deu exemplos de formas de fazer para lidar com essa situação.<br>
**O que foi entendido pelo grupo:** O método `achaFim` foi adaptado para fazer a função dele e manter o método `verUlt` correto.<br>

---

**O que foi pedido à IA:** O método para lidar com parênteses foi escrito de forma que gasta muitos recursos e dando erro de *run time*, como posso otimizá-lo?<br>
**Qual IA foi utilizada:** Google Gemini<br>
**O que foi aproveitado:** O método `eval` tem uma forma de lidar com os parênteses, pois eles sempre chegam nele sendo os últimos a se lidar.<br>
**O que foi reescrito pelo grupo:** Ele deu os métodos `eEnvolto` e `desembrulhar`, que fazem a verificação se está envolto e retiram o primeiro e último valor da string, respectivamente.<br>

---

**O que foi pedido à IA:** Estou com um problema na situação de `(1+2)*(4/2)`, como posso arrumar isso?<br>
**Qual IA foi utilizada:** Anthropic Claude Sonnet 5.5 médio<br>
**O que foi aproveitado:** Ele fez o método de verificação se o cálculo está completamente envelopado, e não são só duas contas distintas.<br>
**O que foi entendido pelo grupo:** Ele desenvolveu um método que verifica se o último parênteses fecha; se tiver mais conta, ele devolve como negativo e passa para a próxima conta.<br>

---

**O que foi pedido à IA:** Como posso tratar esses casos de número negativo e unitário?<br>
**Qual IA foi utilizada:** Anthropic Claude Sonnet 5.5 médio<br>
**O que foi aproveitado:** Implementou o cálculo melhor de negativos e unitários.<br>
**O que foi entendido pelo grupo:** Ele implementou uma verificação no `verUlt` para saber se o caractere prévio é um número; se for, ele conta como se fosse o último caractere atual; se não for, ele não conta como o último.

