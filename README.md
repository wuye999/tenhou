# 根据可见手牌和牌河生成天凤牌谱
* 写了一个简单的脚本，功能是根据可见手牌和牌河生成天凤牌谱，可以对牌谱中的手牌、牌河、点数状况等信息进行自定义编辑, 用法如下
* 
  脚本链接：[raw.githubusercontent.com/wuye999/tenhou/main/生成2.py](https://raw.githubusercontent.com/wuye999/tenhou/main/%E7%94%9F%E6%88%902.py)

1. 首先，

    我们拿到这样一个局面，我们不知道牌谱，又或者想改牌河、手牌。
   
    天凤编辑需要编辑四家配牌，取牌等。十分麻烦时。

    ![image](https://github.com/wuye999/tenhou/assets/79479594/d414be09-0f5b-4b59-9e5b-ed350c1e6f7f)


2. 我们在脚本里填写信息

    使用此脚本 第14到40行 需要输入 **主视角手牌** 和 **四家牌河信息**、**副露信息** 其余留空

    ![image](https://github.com/wuye999/tenhou/assets/79479594/574e8768-6575-4fce-8bf6-614a3b32bb6a)

    然后执行脚本(python 脚本.py)，会自动生成完整的取牌，出牌部分。

    在脚本目录生成一个txt文件，里面是对应的是生成的天凤牌谱链接

    ![image](https://github.com/wuye999/tenhou/assets/79479594/b17103e0-9186-4272-b161-898f562749ee)

3. 结果

    ![image](https://github.com/wuye999/tenhou/assets/79479594/d92ea9ae-d9f6-4932-9459-af4927ee2d8d)

4. 问题

    如果您遇到报错，请先确认您输入的牌河和手牌是否有5枚一样的牌。

