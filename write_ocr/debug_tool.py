"""
显示图片
"""
import matplotlib.pyplot as plt

def show_img(im, is_gray = True, is_show=True):
    if is_gray:
        plt.imshow(im, cmap="gray")
    else:
        plt.imshow(im)
    # plt.axis('off') # 不显示坐标
    plt.show()

"""
绘制训练结果
代码来源
https://tensorflow.google.cn/tutorials/images/classification?hl=zh-cn
"""
# 显示训练验证集的曲线
def show_history(history, epochs):

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()