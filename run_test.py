import unittest
from unittest.mock import patch
import io
import sys
import memsim  # 导入主程序模块
import matplotlib.pyplot as plt
import os

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
                print("CurrentTrace: ", traces[i], " Current MMU: ", m)
                for k in range(1, 101):
                    with self.subTest(param=i):
                    # 构建参数列表，类似 ["main.py", "func1", "func2", "func3", "func4"]
                        args  = ["memsim.py"] + [traces[i],k,m,"quiet"]
                    # 使用@patch修改sys.argv的值，模拟命令行参数
                    with patch("sys.argv", args):
                        # 调用主函数
                        output.append(memsim.main())
                #创建文件夹output/traces[i]，如果已经存在则不创建
                os.makedirs('./output/'+traces[i], exist_ok=True)
                
                               
                #output写入名为m的文件 路径为./output/traces[i]/m.txt，m是mmu的名称。output每个元素占一行，前面加上行号+1

                f = open('./output/'+traces[i]+'/'+m+'.txt','w')
                for j in range(len(output)):
                    f.write(str(j+1)+' '+str(output[j])+'\n')
                ##以output绘制折线图，x轴为1-output的长度，y轴为output的值
               
                line1_handle, = ax.plot(range(1,len(output)+1),output,  linestyle='-',label=m)
                line_handle.append(line1_handle)

                nearest_x = None
                nearest_y = None
                nearest_distance = float('inf')

                for j in range(len(output)):
                    if output[j] > 0.95:
                        distance = abs(output[j] - 0.95)
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_x = j + 1
                            nearest_y = output[j]

                if nearest_x is not None:
                    ax.plot(nearest_x, nearest_y, 'ro')
                    ax.annotate('(%d, %.3f)' % (nearest_x, nearest_y), xy=(nearest_x, nearest_y), xytext=(nearest_x, nearest_y + 0.01))


            ax.set_xlabel('Page Frame Count')
            ax.set_ylabel('Hit Rate')
            ax.legend(handles=line_handle, loc='upper right')
               
                

        # 显示所有图表
        plt.show()








if __name__ == '__main__':
    unittest.main()
