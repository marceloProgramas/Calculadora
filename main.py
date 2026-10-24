def digitToInt(x):
    return int(x, 16)

def isSpace(c):
    return c.isspace()

def main():
    conta = "(2+4)-(4/2)"
    print(eval(conta))


def temEsp(s):
    return any(isSpace(c) for c in s)


def remEsp(s):
    return "".join(c for c in s if not isSpace(c))


def temOper(s):
    return any(c in "+-*/()" for c in s)


def toNum(s):
    if s == "":
        return 0
    if len(s) == 1:
        return digitToInt(s[0])
    x, xs = s[0], s[1:]
    return (digitToInt(x) * 10 ** len(xs)) + toNum(xs)


def eval(text):
    # where
    ind = verUlt(text, 0, 0, 0, '(')

    def eEnvolto(t):
        if t != "" and t[0] == '(':
            def go(cs_, n):
                if cs_ == "":
                    return False
                c, cs = cs_[0], cs_[1:]
                if c == '(':
                    return go(cs, n + 1)
                elif c == ')':
                    return (cs == "") if n == 1 else go(cs, n - 1)
                else:
                    return go(cs, n)
            return go(t[1:], 1)
        return False

    def desembrulhar(t):
        return t[1:len(t) - 1]  # take (length t - 2) (drop 1 t)

    # guards
    if temEsp(text):
        return eval(remEsp(text))
    elif eEnvolto(text):
        return eval(desembrulhar(text))
    elif ind > 0:
        return eval2((text, ""), ind, 0)
    elif text != "" and text[0] == '-':
        resto = text[1:]
        return -(eval(resto))
    elif text != "" and text[0] == '+':
        resto = text[1:]
        return eval(resto)
    else:
        return toNum(text)


def eval2(par, ind, ct):
    texto, y = par
    if texto == "":
        return eval(y)
    x, xs = texto[0], texto[1:]
    # where
    character = (ct + 1 == ind)

    if character and x == '+':
        return eval(y) + eval(xs)
    elif character and x == '-':
        return eval(y) - eval(xs)
    elif character and x == '*':
        return eval(y) * eval(xs)
    elif character and x == '/':
        return eval(y) // eval(xs)  # div do Haskell = divisão com piso
    else:
        return eval2((xs, y + x), ind, ct + 1)


def verUlt(lista, ct, ind, c, prev):
    if lista == "":
        return ind
    x, xs = lista[0], lista[1:]
    # where
    p = prioridade(x)
    binario = prev not in "+-*/("

    if x == '(':
        return achaFim(xs, ct + 1, 1, ind, c)
    elif p >= c and p > 0 and binario:
        return verUlt(xs, ct + 1, ct + 1, p, x)
    else:
        return verUlt(xs, ct + 1, ind, c, x)


def achaFim(lista, ct, n, ind, c):
    if lista == "":
        return ind
    x, xs = lista[0], lista[1:]

    if x == ')' and n == 1:
        return verUlt(xs, ct + 1, ind, c, ')')
    elif x == ')':
        return achaFim(xs, ct + 1, n - 1, ind, c)
    elif x == '(':
        return achaFim(xs, ct + 1, n + 1, ind, c)
    else:
        return achaFim(xs, ct + 1, n, ind, c)


def prioridade(c):
    if c == '+':
        return 2
    elif c == '-':
        return 2
    elif c == '*':
        return 1
    elif c == '/':
        return 1
    else:
        return 0


if __name__ == "__main__":
    main()