import fitz
import os
import glob
import shutil

import PyPDF2

'''
def merge_pdf(dirname):
    postfix = set(['pdf','txt'])  # 设置要保存的文件格式
    for maindir, subdir, file_name_list in os.walk(dirname):
        print("maindir",maindir)
        print("subdir",subdir)
        print("file_name_list",file_name_list)
'''

def merge_and_double_height(input_pdf_path, output_pdf_path):
    with open(input_pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        total_pages = pdf_reader.getNumPages()

        if total_pages % 2 != 0:
            total_pages -= 1

        output_pdf = PyPDF2.PdfFileWriter()

        for i in range(0, total_pages, 2):
            first_page = pdf_reader.getPage(i)
            second_page = pdf_reader.getPage(i + 1)

            width = first_page.mediaBox.getWidth()
            height = first_page.mediaBox.getHeight() + second_page.mediaBox.getHeight()

            merged_page = PyPDF2.pdf.PageObject.createBlankPage(width=width, height=height)

            merged_page.mergeTranslatedPage(first_page, 0, second_page.mediaBox.getHeight())
            merged_page.mergePage(second_page)

            #merged_page.mergePage(first_page)
            #merged_page.mergeTranslatedPage(second_page, 0, first_page.mediaBox.getHeight())

            output_pdf.addPage(merged_page)

        with open(output_pdf_path, 'wb') as output_file:
            output_pdf.write(output_file)

def scale_pdf(input_pdf_path, output_pdf_path):
    with open(input_pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        total_pages = pdf_reader.getNumPages()

        output_pdf = PyPDF2.PdfFileWriter()

        for i in range(total_pages):
            page = pdf_reader.getPage(i)

            # 获取原始页面的大小
            width = page.mediaBox.getWidth()
            height = page.mediaBox.getHeight()/2

            # 计算新的宽度
            new_width = width / 2

            # 计算缩放比例
            scale = new_width / width

            # 创建新的页面，并应用缩放
            new_page = page.createBlankPage(width=new_width, height=height)
            new_page.mergeScaledTranslatedPage(page, scale, 0, 0)

            output_pdf.addPage(new_page)

        with open(output_pdf_path, 'wb') as output_file:
            output_pdf.write(output_file)


def merge_pages(input_pdf_path, output_pdf_path):
    with open(input_pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        total_pages = pdf_reader.getNumPages()

        if total_pages % 2 != 0:
            total_pages -= 1

        output_pdf = PyPDF2.PdfFileWriter()

        for i in range(0, total_pages, 2):
            left_page = pdf_reader.getPage(i)
            right_page = pdf_reader.getPage(i + 1)

            merged_page = PyPDF2.pdf.PageObject.createBlankPage(
                width=left_page.mediaBox.getWidth() + right_page.mediaBox.getWidth(),
                height=max(left_page.mediaBox.getHeight(), right_page.mediaBox.getHeight())
            )

            merged_page.mergeTranslatedPage(left_page, 0, 0)
            merged_page.mergeTranslatedPage(right_page, left_page.mediaBox.getWidth(), 0)

            output_pdf.addPage(merged_page)

        with open(output_pdf_path, 'wb') as output_file:
            output_pdf.write(output_file)


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
                #new_pdf.new_page(-1, width=cur_page.mediabox_size.x,
                                   # height=cur_page.mediabox_size.y)
               # new_pdf.new_page(-1, width=cur_page.mediabox_size.x,
                                #    height=cur_page.mediabox_size.y)
            print(cur_page)
            new_pdf.insert_pdf(file_pdf1,from_page=i,to_page=i)
            new_pdf.new_page(-1, width=cur_page.mediabox_size.x,
                                    height=cur_page.mediabox_size.y)
            i=i+1
        new_pdf.save(filename[0] + "_middle.pdf")
        input_pdf_path = filename[0] + "_middle.pdf"
        output_pdf_path = filename[0]+"_output.pdf"  # 输出PDF文件路径
        final_pdf_path = filename[0]+"_final.pdf" 


        merge_pages(input_pdf_path, 
                          output_pdf_path)
        scale_pdf(output_pdf_path,final_pdf_path)
        output_pdffinal_path = filename[0] + "_done.pdf"
        merge_and_double_height(final_pdf_path,output_pdffinal_path)
        
        file_pdf1.close()
        new_pdf.close()
        dst_dir_origin = dirname + '/pdf_origin/'

        mymovefile(file, dst_dir_origin)
        dst_dir_middle = dirname + '/pdf_middle/'
        mymovefile(output_pdf_path, dst_dir_middle)

        mymovefile(final_pdf_path, dst_dir_middle)
        mymovefile(input_pdf_path, dst_dir_middle)

    
    #for file in path:
       # dst_dir = dirname + '/pdf_done/'
        #mymovefile(file, dst_dir)
    


if __name__ == '__main__':
    root = os.path.abspath(os.path.join(os.getcwd(), "."))
    print('当前项目所在目录:',root)
    merge_pdf(root)
    os.system("pause")