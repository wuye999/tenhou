# 根据可见手牌和牌河生成天凤牌谱
* 写了一个简单的脚本，功能是根据可见手牌和牌河生成天凤牌谱，用法如下
* 
  脚本链接：[raw.githubusercontent.com/wuye999/tenhou/main/生成2.py](https://raw.githubusercontent.com/wuye999/tenhou/main/%E7%94%9F%E6%88%902.py)

1. 首先，

    我们拿到这样一个局面，我们不知道牌谱，又或者想改牌河、手牌。
   
    天凤编辑需要编辑四家配牌，取牌等。十分麻烦时。

    ![image](https://github.com/wuye999/tenhou/assets/79479594/ad691823-748b-4aac-9f8d-0dfc8732e3a6)



3. 我们在脚本里填写信息

    使用此脚本需要输入 **主视角手牌** 和 **四家牌河信息**、**副露信息** 其余留空

    ![image](https://github.com/wuye999/tenhou/assets/79479594/0952be62-cba8-4877-bfbf-5e926339a303)

    然后执行脚本(python 脚本.py)，会自动生成完整的取牌，出牌部分。

    在脚本目录生成一个txt文件，里面是对应的是生成的天凤牌谱链接

    ![image](https://github.com/wuye999/tenhou/assets/79479594/b17103e0-9186-4272-b161-898f562749ee)

4. 结果

    ![image](https://github.com/wuye999/tenhou/assets/79479594/df62c44f-25af-4f7b-9bc2-4869a3d10911)

5. 问题

    如果您遇到报错，请先确认您输入的牌河和手牌是否有5枚一样的牌。

    杠方面的代码还没写，等考试完在看看怎么写吧。鸽~
