 
  一、概述  
  项目名称：starNeck  
  项目描述：基于头部姿态识别的活动颈椎小游戏  
  小组名称：第七小组  
  小组成员：张佩、肖琦诗、张可儿、杨诚  
  
  二、小组分工  
  为了确保项目的顺利进行和高效完成，我们团队制定了详细的分工计划。本文档旨在明确团队成员的职责、任务和工作范围，确保每位成员都清楚自己的角色和期望。  
  
  1、成员：肖琦诗</br>
  分工：</br>
  ①Blender模型资源的搜寻、筛选；</br>
  ②修改、优化“星之卡比”Blender模型材质，对角色模型上色，适当修改形状；</br>  
  修改、优化“草坪、金币”blender模型形状、位置，添加相对应的纹理，调整布局；</br>
  ③制作StartNeck游戏开始和结束的UI界面，并在界面中设计选择单人&双人模式功能、开关游戏功能、开始结束游戏功能；</br>
  ④编写StartNeck游戏开始结束界面C#脚本，包括UI界面中面板跳转函数，开关函数，场景跳转函数，音乐控制函数。</br>

  2、成员：张佩</br>
  分工：</br>
  ①人脸姿态识别模型的实现与调试；</br>
  ②选择合适pynput模块，使人脸姿态的欧拉角输出得以模拟实际的键盘输入；</br>
  ③调整欧拉角参数以适应玩家头部运动，比如，将滚转角的区间设为±15、偏航角区间设为±20度，俯仰角则设为±5度；</br>
   另外，利用counter参数对每一个玩家的动作识别进行限制，使其不至于同一个动作连续识别；</br>
  ④调用摄像头，使其画面置顶，并切分为两个画面；然后，使两个画面的画框分别为红、紫，并分别在两个画面中添加白色标准框以便玩家校准；</br>
  ⑤使用多线程，得以在python中调用游戏exe文件，实现便捷启动；</br>
  ⑥使用pyinstaller打包所有文件，使其最后汇总为一个exe可执行文件，点击即可运行；</br>
  ⑦进行ppt讲解，游戏调试与展示；完成部分需求文档。</br>   
  
  
  3、成员：杨诚</br>
  分工：</br>
  ①游戏本体的设计以及实现；</br>
  ②游戏场景的搭建：包括地板的生成和销毁、金币的生成和销毁、路障的生成和销毁；</br>
  ③玩家控制的实现：利用unity的input插件包实现玩家控制物体左右移动、跳跃以及滚动，以及玩家控制的一些细节；</br>
  ④物体之间的交互：实现了金币和player之间碰撞的判定以及后续实现，路障和player之间碰撞的判定以及游戏流程控制；</br>
  ⑤unity的版本控制以及各场景之间的整合。</br>

  4、成员：张可儿</br>
  分工：</br>
  ①面部识别和面部特征点检测的模型文件及数据集获取；</br>
  ②人脸姿态识别模型的实现与调试，如面部特征点的识别、欧拉角计算以及面部识别点的二维投影；</br>
  ③通过模拟键盘按键将面部识别结果输出到Unity，控制玩家移动；</br>
  ④调整欧拉角参数以及停滞时间（获取动作指令后一段时间内不接收新的动作指令）以适应玩家头部运动；</br>
  ⑤使用多线程，得以在python中调用游戏exe文件，实现便捷启动；</br>
  ⑥使用pyinstaller打包所有python文件，使其最后汇总为一个exe可执行文件，点击即可运行。</br>
  ⑦Blender模型在Unity中的导入，场景优化以及Unity组件功能完善；</br>
  ⑧完成部分需求文档；</br>
  ⑨进行游戏调试与展示。</br>
