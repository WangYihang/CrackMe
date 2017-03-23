####简介 : 
```
需要输入用户名和密码
因此程序的认证流程可能是 : 
1. 输入用户名
2. 输入密码
3. 根据用户名计算出一个正确的密码
4. 对比用户输入的密码和正确的密码
```
####分析过程 : 
ida 载入 , 定位到关键函数 : 
```C
INT_PTR __stdcall DialogFunc(HWND hWnd, UINT a2, WPARAM a3, LPARAM a4)
{
  int v4; // eax@10

  if ( a2 == 272 )
  {
    dword_403100 = (int)hWnd;
    lParam = (LPARAM)LoadIconA(hInstance, IconName);
    SendMessageA(hWnd, 0x80u, 1u, lParam);
    SendDlgItemMessageA(hWnd, 1002, 0xC5u, 0xBu, 0);
  }
  else if ( a2 == 16 )
  {
    EndDialog(hWnd, 0);
  }
  else if ( a2 == 273 && !HIWORD(a3) )
  {
    if ( (_WORD)a3 == 1004 )
    {
      EndDialog(hWnd, 0);
    }
    else if ( (_WORD)a3 == 1003 )
    {
      GetDlgItemTextA(hWnd, 1001, String, 25);
      GetDlgItemTextA(hWnd, 1002, byte_403015, 25);
      v4 = sub_40117F(); // 核心函数
      if ( v4 == 63428 ) // 成功
      {
        MessageBoxA(hWnd, Text, Caption, 0x30u);
      }
      else
      {
        if ( v4 == 333 ) // 用户名长度必须大于 4 
        {
          MessageBoxA(hWnd, aTheNameMustBeA, aUhhhhhhhhhhhhh, 0x10u);
          return 0;
        }
        if ( v4 == 111 ) // 没有输入密码
        {
          MessageBoxA(hWnd, aYouHaveForgetT, aUhhhhhhhhhhhhh, 0x10u);
          return 0;
        }
		// 密码错误
        MessageBoxA(hWnd, aBestLuckTheNex, aUhhhhhhhhhhhhh, 0x10u);
      }
      EndDialog(hWnd, 0);
      return 0;
    }
  }
  return 0;
}
```
再进入核心函数 : 
```
signed int sub_40117F()
{
  signed int result; // eax@2
  unsigned int v1; // eax@3
  int v2; // edi@7
  CHAR *v3; // esi@7
  int v4; // ecx@7
  signed int v5; // ebx@7
  int v6; // eax@8

  if ( (unsigned int)lstrlenA(String) >= 4 )
  {
    v1 = lstrlenA(byte_403015); // v1 是 byte_403015 这个字符串的长度
    if ( v1 <= 8 ) // 当 byte_403015 这个字符串长度大于 8 , 可以看到下面返回 222 , 根据上一个函数 , 可以知道 , 当返回 222 的时候显示注册码错误 , 因此 byte_403015 这个字符串应该是用户输入的密码
    {
      if ( v1 >= 1 )
      {
        v2 = 0;
        v3 = String;
        v4 = lstrlenA(String);
        v5 = 45;
        do
        {
          v6 = v5 * (unsigned __int8)*v3++;
          v2 += v6;
          ++v5;
          --v4;
        }
        while ( v4 );
        wsprintfA(byte_4030E0, aD, v2);
        if ( *(_DWORD *)byte_403015 != *(_DWORD *)byte_4030E0
          || *(_DWORD *)&byte_403015[4] != *(_DWORD *)&byte_4030E0[4] )
        {
          result = 444;
        }
        else
        {
          wsprintfA(Text, aD, 925176);
          result = 63428; // 通过分析上一个函数我们可以知道 , 注册成功的时候 , 这个函数应该返回 63428 , 因此必须得让上面的那个 if 不成立
        }
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
```
根据分析 , 我们必须得让下面的语句不成立 : 
( *(_DWORD *)byte_403015 != *(_DWORD *)byte_4030E0 || *(_DWORD *)&byte_403015[4] != *(_DWORD *)&byte_4030E0[4] )
其中 : 
byte_403015 是 用户输入的密码
byte_4030E0 是 根据用户名计算出来的注册码(密码)
我们再来看看程序是如何计算注册码(密码)的

v2 = 0;
v3 = String;
v4 = lstrlenA(String); // String 表示的应该就是用户名了
v5 = 45;
do
{
  v6 = v5 * (unsigned __int8)*v3++; // 循环遍历 用户名 这个字符串
  v2 += v6;
  ++v5;
  --v4;
}
while ( v4 );
wsprintfA(byte_4030E0, aD, v2); // 将 v2 格式化为 char[] 并保存到 byte_4030E0 中

这样的话 , 我们只需要模拟一下这个算法就可以写出一个注册机(keygen.py/keygen.c)
```
