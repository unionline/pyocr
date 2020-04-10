import core.baidu_ocr as core
import os


def test():

    image_sample_dir = './images/sample/ok/'
    files = readFiles(image_sample_dir)
    print(files)
    ocr = core.BaiduOCR
    for f in files:
        ocr.set_img_path(ocr, image_sample_dir + f)
        type_index = int(f[:1])
        print('+++' + core.type_map[type_index] + '+++')
        print('filename=' + f)
        retsult = ocr.img2txt_by_type(ocr, type_index)
        print(retsult)


def readFiles(dir):
    files = os.listdir(dir)
    return files


def main():
    print("Sample Test Start")
    test()
    print("Sample Test End")


if __name__ == '__main__':
    main()
