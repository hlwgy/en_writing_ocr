package cn.a2q.tflite;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import org.tensorflow.lite.Interpreter;

public class WriteActivity extends Activity {

    String TAG = "NumWriteActivity";
    Interpreter interpreter;

    private DrawingView drawingView;
    private TextView result;
    private TextView time;

    @SuppressLint("WrongViewCast")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_write);

        interpreter = TFliteTool.getInterpreter(this, "char.tflite");

        if (interpreter == null){
            Log.e(TAG, "没有找到文件");
            return;
        }

        drawingView = findViewById(R.id.drawing_surface);
        result = findViewById(R.id.tv_result);
        result.setText("");
        time = findViewById(R.id.tv_time);
        time.setText("");
    }

    public void save(View view) {
        Bitmap bitmap = drawingView.getBitmap();
        capImg(interpreter, bitmap);
    }

    public void clear(View view) {
        drawingView.clear();
        result.setText("");
        time.setText("");
    }

    private void capImg(final Interpreter interpreter, final Bitmap bitmap){

        if (interpreter == null){
            Log.e(TAG, "没有找到文件");
            mHandler.sendEmptyMessage(-1);
            return;
        }
        new Thread(new Runnable() {
            @Override
            public void run() {
//                saveImage(bitmap);
                long time1 = System.currentTimeMillis();
                String strResNum = TFliteTool.writeNumClass(interpreter, bitmap, 28);
                long time_sep = System.currentTimeMillis() - time1;
                Message msg = new Message();
                msg.what = 1;
                msg.obj = strResNum;
                msg.arg1 = (int) time_sep;
                mHandler.sendMessage(msg);
            }
        }).start();
    }
    public Handler mHandler = new Handler() {

        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            if (msg.what == 1){
                String s = msg.obj.toString();
                showResult(s, msg.arg1);
            }else if (msg.what == -1){
                Log.e(TAG, "没有找到文件，模型初始化失败");
            }
        }
    };

    public void showResult(String text, int ms){
        result.setText("结果："+text);
        time.setText("用时"+ms/1000f+"秒");
    }

    @Override
    protected void onStop() {
        mHandler.removeMessages(1);
        super.onStop();
    }

//    /**
//     * 想看绘制的图片
//     */
//    private void saveImage(Bitmap bitmap) {
//        if (bitmap != null) {
//            try {
//                File file = new File(getExternalFilesDir(null), "write.png");
//                FileOutputStream fos = new FileOutputStream(file);
//                bitmap.compress(Bitmap.CompressFormat.PNG, 100, fos);
//                fos.close();
//                Log.e(TAG, "Image saved "+file.getAbsolutePath());
//            } catch (IOException e) {
//                e.printStackTrace();
//                Log.e(TAG, "Failed to save image");
//            }
//        } else {
//            Log.e(TAG, "No image to save");
//        }
//    }

}