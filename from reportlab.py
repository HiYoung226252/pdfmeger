from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import fitz
import os
import glob
import shutil


def merge_pages(input_pdf_path, output_pdf_path):
    # 打开插入空白页后的PDF文件
    pdf = fitz.open(input_pdf_path)
    pdf_writer = fitz.open()

    for page_num in range(0, pdf.page_count, 2):
        left_page = pdf.load_page(page_num)

        if page_num + 1 < pdf.page_count:
            right_page = pdf.load_page(page_num + 1)
        else:
            # 创建空白页，大小与原始PDF页面相同
            right_page = fitz.new_page(width=left_page.rect.width, height=left_page.rect.height)

        new_page = pdf_writer.new_page(width=left_page.rect.width * 2, height=left_page.rect.height)
        new_page.insert_pdf(pdf, from_page=page_num, to_page=page_num)
        new_page.insert_pdf(pdf, from_page=page_num + 1, to_page=page_num + 1)

        pdf_writer.insert_pdf(new_page, from_page=0, to_page=0)  # 将新页面插入到新文档

    pdf_writer.save(output_pdf_path)
    pdf.close()
    pdf_writer.close()


def mymovefile(srcfile,dstpath):                       # 移动函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.move(srcfile, dstpath + fname)          # 移动文件
        print ("move %s -> %s"%(srcfile, dstpath + fname))

def merge_pdf(dirname):
    path = glob.glob(dirname + '/pdf/**/*.pdf',recursive=True)
    print("file",path)
    done = 'done'
    for file in path:
        filename = file.split('.')
        if done in filename[-2]:
           continue
        file_pdf1 = fitz.open(file)
        new_pdf = fitz.open()  # 完成后要写入的pdf
        i=0
        for index in range (len(file_pdf1)) :
       # for cur_page in file_pdf1:
            #print('正在合并第{}页...'.format(i+1))
            cur_page = file_pdf1[index]
            if (index == 0):
                print("Add two new page !")
                new_pdf.new_page(-1, width=cur_page.mediabox_size.x,
                                    height=cur_page.mediabox_size.y)
                new_pdf.new_page(-1, width=cur_page.mediabox_size.x,
                                    height=cur_page.mediabox_size.y)
            print(cur_page)
            new_pdf.insert_pdf(file_pdf1,from_page=i,to_page=i)
            new_pdf.new_page(-1, width=cur_page.mediabox_size.x,
                                    height=cur_page.mediabox_size.y)
            i=i+1
        new_pdf.save(filename[0] + "_done.pdf")
        input_pdf_path = filename[0] + "_done.pdf"
        output_pdf_path = "output.pdf"  # 输出PDF文件路径
        pages_per_sheet = 2  # 每张纸上放置的页数

        merge_pages(input_pdf_path, 
                          output_pdf_path)

        file_pdf1.close()
        new_pdf.close()
        dst_dir = dirname + '/pdf_done/'
        mymovefile(file, dst_dir)
    
    #for file in path:
       # dst_dir = dirname + '/pdf_done/'
        #mymovefile(file, dst_dir)
    


if __name__ == '__main__':
    root = os.path.abspath(os.path.join(os.getcwd(), "."))
    print('当前项目所在目录:',root)
    merge_pdf(root)
    os.system("pause")

