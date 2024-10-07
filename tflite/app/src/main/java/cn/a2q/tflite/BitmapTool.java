package cn.a2q.tflite;

import android.graphics.Bitmap;

public class BitmapTool {
    public static float[][][][] bitmap2GrayArr(Bitmap bitmap, int imgSize){
        // 进行图像预处理
        int imgWidth = imgSize; // 期望的图像宽度
        int imgHeight = imgSize; // 期望的图像高度
        Bitmap resizedBitmap = Bitmap.createScaledBitmap(bitmap, imgWidth, imgHeight, true);
        int[] intValues = new int[imgWidth * imgHeight];
        resizedBitmap.getPixels(intValues, 0, imgWidth, 0, 0, imgWidth, imgHeight);
        // 转换为float数组
        float[] floatValues = new float[imgWidth * imgHeight];
        for (int i = 0; i < intValues.length; ++i) {
            final int val = intValues[i];
            floatValues[i] = (val & 0xFF) / 1.0f; // 灰度值
        }
        // 创建输入数组
        float[][][][] inputArr = new float[1][imgHeight][imgWidth][1];
        for (int i = 0; i < imgHeight; ++i) {
            for (int j = 0; j < imgWidth; ++j) {
                inputArr[0][i][j][0] = floatValues[i * imgWidth + j];
            }
        }
        return inputArr;
    }
}
