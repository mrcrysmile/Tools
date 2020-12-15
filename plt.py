# 各种绘图方法

# %%
import matplotlib.pyplot as plt
x = [100,250,500,750,1000]
y1 = [75,42,53.2,49.9,48.6]
y2 = [89,86.4,84.2,85.5,85.4]
z1 = [0, 0, 0, 0, 0]
z2 = [99,94.8,96.6,96.9,97.7]
#开一个新窗口，创建1个子图。facecolor设置背景颜色
ax1 = plt.subplot(1,1,1,facecolor='white')  
ax1.set_xlim(0, 1100)
ax1.set_ylim(0, 100)
ax1.set_xlabel('picture amount')
ax1.set_ylabel('accurate/%')
plt.plot(x,y1)
plt.plot(x,y2)
plt.legend()
plt.tight_layout()
plt.show()
# %%
