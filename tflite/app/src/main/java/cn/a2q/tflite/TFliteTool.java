package cn.a2q.tflite;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import org.tensorflow.lite.Interpreter;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;

public class TFliteTool {

    static String TAG = "TFliteTool";

    static String[] classNames = {
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",  // 0-9
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",  // A-J
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",  // K-T
            "U", "V", "W", "X", "Y", "Z",                      // U-Z
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",  // a-j
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",  // k-t
            "u", "v", "w", "x", "y", "z"                       // u-z
    };

    public static String writeNumClass(Interpreter interpreter, Bitmap bitmap, int imgSize){
        float[][][][] inputArr = BitmapTool.bitmap2GrayArr(bitmap, imgSize);// 获取输入层数据
        float[][] outputArray = new float[1][62]; // 输出层大小是[1, 10]
        interpreter.run(inputArr, outputArray);
        int predictedClassIndex = argmax(outputArray[0]); // argmax函数返回数组中最大值的索引

        return classNames[predictedClassIndex];
    }

    // 找到数组中最大值的索引
    public static int argmax(float[] array) {
        float maxVal = array[0];
        int maxIndex = 0;
        for (int i = 1; i < array.length; i++) {
            if (array[i] > maxVal) {
                maxVal = array[i];
                maxIndex = i;
            }
        }
        return maxIndex;
    }

    private static MappedByteBuffer loadModelFile(Context context, String fileName) throws IOException {
        AssetFileDescriptor fileDescriptor = context.getAssets().openFd(fileName);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    public static Interpreter getInterpreter(Context context, String tfName){
        Interpreter.Options options = new Interpreter.Options();
        options.setNumThreads(4);
        Interpreter interpreter = null;
        try {
            interpreter = new Interpreter(loadModelFile(context, tfName), options);
        } catch (IOException e) {
            throw new RuntimeException("Error loading model file.", e);
        }
        return interpreter;
    }
}
