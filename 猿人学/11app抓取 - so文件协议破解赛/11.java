package com.dta.yuanrenxue8;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.wrapper.DvmLong;
import com.github.unidbg.memory.Memory;

import java.io.File;
import java.io.IOException;

import java.util.Random;

public class MainActivity2 {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;
    private final DvmClass TTEncryptUtils;
    private final boolean logging;

    MainActivity2(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.yuanrenxue.onlinejudge2020").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(new File("unidbg-android/src/test/java/com/dta/yuanrenxue8/YuanRenXueOJ_1.2-release.apk")); // 创建Android虚拟机
        vm.setVerbose(logging); // 设置是否打印Jni调用细节

        vm.setJni(new AbstractJni() {
            @Override
            public DvmObject<?> callStaticObjectMethodV(BaseVM vm, DvmClass dvmClass, DvmMethod dvmMethod, VaList vaList) {
                if ("android/os/Looper->myLooper()Landroid/os/Looper;".equals(dvmMethod.toString())){
                    return vm.resolveClass("android/os/Looper").newObject(null);
                }
                return null;
            }
            @Override
            public DvmObject<?> newObjectV(BaseVM vm, DvmClass dvmClass, DvmMethod dvmMethod, VaList vaList) {
                if ("java/util/Random-><init>()V".equals(dvmMethod.toString())){
                    return vm.resolveClass("java/util/Random").newObject(new Random());
                }else if("java/util/Random-><init>(J)V".equals(dvmMethod.toString())){
                    return vm.resolveClass("java/util/Random").newObject(new Random(vaList.getLongArg(0)));
                }
                return null;
            }
            @Override
            public int callIntMethodV(BaseVM vm, DvmObject<?> dvmObject, DvmMethod dvmMethod, VaList vaList) {
                if ("java/util/Random->nextInt(I)I".equals(dvmMethod.toString())){
                    Random a = (Random)dvmObject.getValue();
                    return a.nextInt(vaList.getIntArg(0));
                }
                return 0;
            }
            @Override
            public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, DvmMethod dvmMethod, VaList vaList) {
                if("android/content/ContextWrapper->getFilesDir()Ljava/io/File;".equals(dvmMethod.toString())){
                    return vm.resolveClass("java/io/File").newObject(new File("/"));
                }else if("java/io/File->getAbsolutePath()Ljava/lang/String;".equals(dvmMethod.toString())){
                    return new StringObject(vm, "/");
                    // 这里会在你的电脑C:\Users\用户名称\AppData\Local\Temp\rootfs\default目录下创建一个.did.bin的文件
                }
                return null;
            }
            @Override
            public boolean acceptMethod(DvmClass dvmClass, String signature, boolean isStatic) {
                return true;
            }
        });

        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/resources/example_binaries/armeabi-v7a/libyuanrenxue_native.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数

        DvmClass cContextWrapper = vm.resolveClass("android/content/ContextWrapper");
        TTEncryptUtils = vm.resolveClass("com/yuanrenxue/onlinejudge2020/OnlineJudgeApp", cContextWrapper);

        dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
        module = dm.getModule(); // 加载好的libttEncrypt.so对应为一个模块

    }

    void destroy() throws IOException {
        emulator.close();
        if (logging) {
            System.out.println("destroy");
        }
    }

    public static void main(String[] args) throws Exception {
        MainActivity2 test = new MainActivity2(false);
       // test.ttEncrypt(args[0]);
        test.ttEncrypt("1");
        test.destroy();
    }

    void ttEncrypt(String number){
        StringObject signobj = TTEncryptUtils.newObject(null).callJniMethodObject(emulator, "getSign(J)Ljava/lang/String;", DvmLong.valueOf(vm, Long.parseLong(number))); // 执行Jni方法
        String sign = signobj.getValue();
        System.out.println(sign);
    }
}
