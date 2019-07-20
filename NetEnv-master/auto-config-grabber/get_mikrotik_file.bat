
(
    get %5
    bye
) | psftp -batch -l %3 -pw %4 -P %2 %3@%1
move %5 %6