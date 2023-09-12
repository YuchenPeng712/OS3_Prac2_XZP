import unittest
from unittest.mock import patch
import io
import sys
import memsim  # 导入主程序模块
import matplotlib.pyplot as plt

class TestMainFunction(unittest.TestCase):
    def setUp(self):
        # 重定向标准输出以捕获主函数的输出
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        # 恢复标准输出
        sys.stdout = sys.__stdout__

    def test_main_with_valid_args(self):
        
        traces = ["sixpack.trace","gcc.trace","swim.trace","bzip.trace"]
        mmu = ["rand","lru","clock"]
        fig, axs = plt.subplots(2,2)
        for i in range(len(traces)):
            ax = axs[i//2,i%2]
            ax.set_title(traces[i])
            line_handle = []
            for m in mmu:
                output = []
                
                for k in range(1, 122):
                    with self.subTest(param=i):
                    # 构建参数列表，类似 ["main.py", "func1", "func2", "func3", "func4"]
                        args  = ["memsim.py"] + [traces[i],k,m,"quiet"]
                    # 使用@patch修改sys.argv的值，模拟命令行参数
                    with patch("sys.argv", args):
                        # 调用主函数
                        output.append(memsim.main())
                line1_handle, =ax.plot(output,  linestyle='-',label=m)
                line_handle.append(line1_handle)
                
                #显示最接近0.05的值
                min = 100
                for j in range(len(output)):
                    if abs(output[j]-0.05) < min:
                        min = abs(output[j]-0.05)
                        index = j
                ax.plot(index,output[index], 'ro')
                #显示最接近0.05的坐标
                ax.annotate('(%d,%.3f)'%(index,output[index]), xy=(index, output[index]), xytext=(index, output[index]+0.01))
                


                
            ax.legend(handles=line_handle, loc='upper right')
               
                

        # 显示所有图表
        plt.show()








if __name__ == '__main__':
    unittest.main()
