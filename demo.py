# -*- coding: utf-8 -*-
"""
@Time ： 2022/8/6 21:32
@Auth ： ghm
@File ：demo.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
root = ttk.Window(size=(500,200))
f = ttk.Frame(root).pack(fill=BOTH, expand=YES)
text_content = '''
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''
# t = ttk.Text(f)
# t.insert("0.0",text_content)
# t.place(x=10,y=10,width=480,height=200)
# sl_x = ttk.Scrollbar(t,orient=HORIZONTAL) #使滚动条水平放置
# #放到窗口的底部, 填充X轴竖直方向
# sl_x.pack(side=ttk.BOTTOM, fill=ttk.X)
# sl_y = ttk.Scrollbar(t,bootstyle="round-success") #滚动条默认垂直放置
# #放到窗口的右侧, 填充Y轴竖直方向
# sl_y.pack(side=ttk.RIGHT, fill=ttk.Y)
# #两个控件相关联
# sl_x.config(command=t.xview)
# t.config(yscrollcommand=sl_x.set)
# sl_y.config(command=t.yview)
# t.config(yscrollcommand=sl_y.set)

##滚动文本框
from ttkbootstrap.scrolled import ScrolledText
st = ScrolledText(f, padding=5, height=10, autohide=True)
st.pack(fill=BOTH, expand=YES)
st.insert(END, text_content)

root.mainloop()
