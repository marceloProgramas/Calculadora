import Data.Char (isSpace, digitToInt)

main :: IO ()
main = do
    putStrLn "qual sua conta"
    conta <- getLine
    print (eval conta)
    
temEsp :: String -> Bool
temEsp = any isSpace

remEsp :: String -> String
remEsp = filter (not . isSpace)

temOper :: String -> Bool
temOper = any (`elem` "+-*/()")

toNum :: String -> Int
toNum [] = 0
toNum [x] = digitToInt x
toNum (x:xs) = (digitToInt x * 10^(length xs)) + toNum xs

eval :: String -> Int
eval text
  | temEsp text = eval (remEsp text)
  | eEnvolto text = eval (desembrulhar text)
  | ind > 0 = eval2 (text, "") ind 0
  | ('-':resto) <- text = negate (eval resto)
  | ('+':resto) <- text = eval resto
  | otherwise = toNum text
  where
    ind = verUlt text 0 0 0 '('
    eEnvolto ('(':xs) = go xs 1
      where
        go [] _ = False
        go (c:cs) n
          | c == '(' = go cs (n + 1)
          | c == ')' = if n == 1 then null cs else go cs (n - 1)
          | otherwise = go cs n
    eEnvolto _ = False
    desembrulhar t = take (length t - 2) (drop 1 t)


eval2 :: (String, String) -> Int -> Int -> Int
eval2 ([], y) _ _ = eval y
eval2 (x:xs, y) ind ct
  | character && x == '+' = eval y + eval xs
  | character && x == '-' = eval y - eval xs
  | character && x == '*' = eval y * eval xs
  | character && x == '/' = eval y `div` eval xs
  | otherwise = eval2 (xs, y ++ [x]) ind (ct + 1)
  where
    character = (ct + 1 == ind)

verUlt :: String -> Int -> Int -> Int -> Char -> Int
verUlt [] _ ind _ _ = ind
verUlt (x:xs) ct ind c prev
  | x == '(' = achaFim xs (ct + 1) 1 ind c
  | p >= c && p > 0 && binario = verUlt xs (ct + 1) (ct + 1) p x
  | otherwise = verUlt xs (ct + 1) ind c x
  where
    p = prioridade x
    binario = prev `notElem` "+-*/("

achaFim :: String -> Int -> Int -> Int -> Int -> Int
achaFim [] _ _ ind _ = ind
achaFim (x:xs) ct n ind c
  | x == ')' && n == 1 = verUlt xs (ct + 1) ind c ')'
  | x == ')' = achaFim xs (ct + 1) (n - 1) ind c
  | x == '(' = achaFim xs (ct + 1) (n + 1) ind c
  | otherwise = achaFim xs (ct + 1) n ind c

prioridade :: Char -> Int
prioridade '+' = 2
prioridade '-' = 2
prioridade '*' = 1
prioridade '/' = 1
prioridade _   = 0