# 根据可见手牌和牌河生成天凤牌谱
 一个简单的脚本，功能是根据可见手牌和牌河生成天凤牌谱，

 也可以对牌谱中的手牌、牌河、点数状况等信息进行自定义编辑, 方便跑ai。
 
  打包好的应用程序：https://raw.githubusercontent.com/wuye999/tenhou/main/天凤牌谱生成.zip

  对应用程序有疑问，请直接使用源代码
  
  源代码：https://raw.githubusercontent.com/wuye999/tenhou/main/生成2.py
  
1. 下载压缩包或者源代码解压得到两个文件

   ![image](https://github.com/wuye999/tenhou/assets/79479594/a4e83411-594a-4d19-b8cd-cb60467e5623)


3. 首先，

    我们拿到这样一个局面，我们不知道牌谱，又或者想改牌河、手牌。
   
    天凤编辑需要编辑四家配牌，取牌等。十分麻烦时。

    ![image](https://github.com/wuye999/tenhou/assets/79479594/d414be09-0f5b-4b59-9e5b-ed350c1e6f7f)


4. 我们用记事本打开** 配置.json **, 填写信息

   需要输入 **主视角手牌** 和 **四家牌河信息**、**四家副露信息** 其余留空

    ![image](https://github.com/wuye999/tenhou/assets/79479594/dff2e149-7ec2-487b-98c3-0c27ea1d3f3e)


    然后双击执行exe程序，会自动生成完整的取牌，出牌部分。

    在软件目录生成一个txt文件，里面是对应的是生成的天凤牌谱链接

    ![image](https://github.com/wuye999/tenhou/assets/79479594/93304ec1-aa56-4ef9-8c54-5dd5cea5fc01)


5. 结果

    ![image](https://github.com/wuye999/tenhou/assets/79479594/b1d2b759-aa92-458f-8e49-4c01c485c874)


6. 问题

    不能出现4枚以上一样的牌，不能出现2枚相同的赤宝牌。否则会报错
   
    副露请写在副露区，包括暗杠，多个副露请用空格隔开，如"55碰5z 吃340s"
   
    指定副露时，相关牌河里一定要有打出被副露的牌。例如指定碰对家8s，对家牌河需要存在8s才能被碰。
  
    牌河手模切写法：手切标志无，模切标志"d"。  手切8s:"8s"   模切8s:"d8s"
  
    立直写法：立直标志"r"，立直后无需模切标志，统统模切。   打8s立直:"r8s"    模切8s立直"dr8s"
  
    副露写法
  
    吃。    13m吃2m:"吃213m"。
  
    碰。    碰上家8s:"碰888s"   碰对家8s:"8碰88s"    碰下家8s:"88碰8s"
  
    杠。    杠上家8s:"杠8888s"  杠对家8s:"8杠888s"   杠下家8s:"888杠8s"
  
    暗杠。  暗杠8s:"888暗8m"
  
    加杠。  碰上家8s,之后加杠8s:"碰888s 加8888s"   碰对家8s,之后加杠8s:"8碰88s 8加888s"   碰下家8s,之后加杠8s:"88碰8s 88加88s"
  

