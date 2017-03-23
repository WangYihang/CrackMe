####简介 : 
```
需要输入用户名和密码
因此程序的认证流程可能是 : 
1. 输入用户名
2. 输入密码
3. 根据用户名计算出一个正确的密码
4. 对比用户输入的密码和正确的密码
```
####详细分析 : 
ida 打开载入 , 定位到关键函数 : 
```
signed int __fastcall sub_40117F(int a1, int a2)
{
  signed int result; // eax@2
  unsigned int v3; // eax@3
  int v4; // edi@7
  CHAR *v5; // esi@7
  int v6; // ecx@7
  signed int v7; // ebx@7
  int v8; // eax@8
  int v9; // [sp-24h] [bp-24h]@7

  sub_40125A(a2);
  if ( (unsigned int)lstrlenA(String) >= 4 )
  {
    v3 = lstrlenA(byte_403021);
    if ( v3 <= 9 )
    {
      if ( v3 >= 1 )
      {
        v9 = sub_401211(); // 等一下需要深入去看
        v4 = 0;
        v5 = String;
        v6 = lstrlenA(String);
        v7 = 1;
        do
        {
          v8 = v7 * (unsigned __int8)*v5++;
          v4 += v8;
          v7 += 6;
          --v6;
        }
        while ( v6 );
        if ( v4 << 8 == v9 ) // 成功 , 这里将 v4 左移 4 位 , 然后和 v9 比较 , 如果相等 , 则说明密码正确 , 这里 v9 即为 sub_401211() 函数的返回值
          result = 666;
        else
          result = 1;
      }
      else
      {
        result = 111;
      }
    }
    else
    {
      result = 222;
    }
  }
  else
  {
    result = 333;
  }
  return result;
}
```
可以看到密码验证成功的条件就是 : 
```
v4 << 8 == v9
```
这里 v4 根据 01 , 02 节课就可以很容易仿照写出 python 或者 C 的代码来生成
因此 , 我们现在需要分析的是 v9 的值是多少 : 
定位关键函数 ` sub_401211() `
```
__int64 sub_401211()
{
  CHAR *v0; // esi@1
  int v1; // ebx@1
  int v2; // eax@1
  bool v3; // zf@2
  int v4; // ecx@2
  int v5; // eax@2
  int v7; // [sp-4h] [bp-4h]@2

  v0 = byte_403021;
  unk_4031CD = a46576698546454 - byte_403021;
  v1 = 0;
  lstrlenA(byte_403021);
  v2 = 0;
  while ( 1 )
  {
    LOBYTE(v1) = *v0;
    v7 = v2;
    v3 = sub_40133D(*v0, (int)v0) == 0;
    v5 = v7;
    if ( v3 )
      break;
    LOBYTE(v1) = v1 - 48;
    v5 = v1 + v7;
    if ( v4 == 1 )
      break;
    v2 = 10 * v5;
    ++v0;
  }
  return sub_401292(v5);
}
```
可以看到这个函数又调用了其他的函数 , 比如说 : 
```
1. v3 = sub_40133D(*v0, (int)v0) == 0;
2. return sub_401292(v5);
```
继续深入分析这两个函数 : 
在这之前 , 我们先来记录一下函数的调用关系 : 
DialogFunc
	sub_40117F
		sub_40125A
		sub_401211
			sub_40133D
			sub_401292
先看 ` sub_40133D ` : 
```
int __usercall sub_40133D@<eax>(char a1@<bl>, int a2@<esi>)
{
  // 传入的参数 a1 是 密码这个字符串的第一个字符
  // 传入的参数 a2 是 密码字符串的长度
  int v2; // edi@1
  int result; // eax@3

  v2 = unk_4031CD; // unk_4031CD 这个是内存中一段空的字符串的首地址
  *(_BYTE *)(unk_4031CD + a2) = a1; // 将 a1 这个字符赋值到 这个空字符串的首地址偏移用户输入的密码的长度的位置
  result = *(_BYTE *)(v2 + a2) <= 0x39u && *(_BYTE *)(v2 + a2) >= 0x30u; // 判断这个位置的字符 , 也就是 a1 是不是在 0x30 (字符 '0') 和 0x39 (字符 '9') 之间
  unk_4031CD += 3; // 这个内存中的空字符串自增 3
  return result; // 返回
}
```
这么分析一下(如果不考虑对内存中的那个空字符串的操作的话 , 这个操作暂时还不知道有啥用 , 先记着) , 貌似这个函数就是用来判断某一个字符是不是一个数字字符的
