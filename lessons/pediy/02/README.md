####简介 : 
```
该程序利用读取 license文件(keyfile.dat) , 并判断这个文件中字符 'G' 的个数是否大于 8 来确定是否注册成功
```
####分析过程 : 
1. OD 载入程序 , 由于程序很小 , 直接阅读关键汇编代码 : 
![打开文件](https://coding.net/u/yihangwang/p/crackme/git/raw/master/lessons/pediy/02/pictures/0x01.png)
```
0040105C   .  6A 00         push 0x0                                 ; |/hTemplateFile = NULL
0040105E   .  68 6F214000   push reverseM.0040216F                   ; ||Attributes = READONLY|HIDDEN|SYSTEM|ARCHIVE|TEMPORARY|402048
00401063   .  6A 03         push 0x3                                 ; ||Mode = OPEN_EXISTING
00401065   .  6A 00         push 0x0                                 ; ||pSecurity = NULL
00401067   .  6A 03         push 0x3                                 ; ||ShareMode = FILE_SHARE_READ|FILE_SHARE_WRITE
00401069   .  68 000000C0   push 0xC0000000                          ; ||Access = GENERIC_READ|GENERIC_WRITE
0040106E   .  68 79204000   push reverseM.00402079                   ; ||FileName = "Keyfile.dat"
00401073   .  E8 0B020000   call <jmp.&KERNEL32.CreateFileA>         ; |\CreateFileA
```
![逐字符读取文件内容](https://coding.net/u/yihangwang/p/crackme/git/raw/master/lessons/pediy/02/pictures/0x02.png)
```
0040109A   > \6A 00         push 0x0                                 ; /pOverlapped = NULL
0040109C   .  68 73214000   push reverseM.00402173                   ; |pBytesRead = reverseM.00402173
004010A1   .  6A 46         push 0x46                                ; |BytesToRead = 46 (70.)
004010A3   .  68 1A214000   push reverseM.0040211A                   ; |Buffer = reverseM.0040211A
004010A8   .  50            push eax                                 ; |hFile = 3857D2E0
004010A9   .  E8 2F020000   call <jmp.&KERNEL32.ReadFile>            ; \ReadFile
004010AE   .  85C0          test eax,eax
004010B0   .  75 02         jnz short reverseM.004010B4
004010B2   .  EB 43         jmp short reverseM.004010F7
004010B4   >  33DB          xor ebx,ebx
004010B6   .  33F6          xor esi,esi                              ;  reverseM.<ModuleEntryPoint>
004010B8   .  833D 73214000>cmp dword ptr ds:[0x402173],0x10         ; 比较文件内容的长度 , 是否大于 0x10
004010BF   .  7C 36         jl short reverseM.004010F7
004010C1   >  8A83 1A214000 mov al,byte ptr ds:[ebx+0x40211A]        ; 将文件的一个字节读取到 al 寄存器中
004010C7   .  3C 00         cmp al,0x0                               ; 比较是否达到了文件末尾
004010C9   .  74 08         je short reverseM.004010D3
004010CB   .  3C 47         cmp al,0x47                              ; 比较这个字符是不是等于 0x47 也就是 ascii 的 'G'
004010CD   .  75 01         jnz short reverseM.004010D0              ; 如果等于 , 则不进行跳转 , 那么下一行的 inc esi 就会执行 , 也就是记录 'G' 的个数的寄存器就会自增
004010CF   .  46            inc esi                                  ;  reverseM.<ModuleEntryPoint>
004010D0   >  43            inc ebx
004010D1   .^ EB EE         jmp short reverseM.004010C1
004010D3   >  83FE 08       cmp esi,0x8                              ; 当整个文件读取完毕后 , 再来判断 esi (也就是存储了 'G' 的个数的寄存器) 是否大于 0x08
004010D6   .  7C 1F         jl short reverseM.004010F7               ; 如果大于 , 则跳转到成功的界面 , 反之则到失败的界面
004010D8   .  E9 28010000   jmp reverseM.00401205
```
####参考资料 : 
![汇编跳转手册](https://coding.net/u/yihangwang/p/crackme/git/raw/master/lessons/pediy/02/pictures/0x03.png)
