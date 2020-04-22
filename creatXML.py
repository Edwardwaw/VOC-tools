#-*- coding:utf-8 -*-
'''
    该代码是将数据转为VOC2007，该代码实现了XML生成和图片位置更改以及文件重命名
'''


import xml.dom
import xml.dom.minidom
import os
# from PIL import Image
import cv2
# xml文件规范定义

_TXT_PATH= '../../SynthText-master/myresults/groundtruth'
_IMAGE_PATH= '../../SynthText-master/myresults/images'

_INDENT= ''*4
_NEW_LINE= '\n'
_FOLDER_NODE= 'VOC2007'
_ROOT_NODE= 'annotation'
_DATABASE_NAME= 'LOGODection'
_ANNOTATION= 'PASCAL VOC2007'
_AUTHOR= 'DaZhangFu_CSDN'
_SEGMENTED= '0'
_DIFFICULT= '0'
_TRUNCATED= '0'
_POSE= 'Unspecified'


_IMAGE_COPY_PATH= 'JPEGImages'
_ANNOTATION_SAVE_PATH= 'Annotations'
# _IMAGE_CHANNEL= 3

# 封装创建节点的过�?
def createElementNode(doc,tag, attr):  # 创建一个元素节�?
    element_node = doc.createElement(tag)

    # 创建一个文本节�?
    text_node = doc.createTextNode(attr)

    # 将文本节点作为元素节点的子节�?
    element_node.appendChild(text_node)

    return element_node

    # 封装添加一个子节点的过�?
def createChildNode(doc,tag, attr,parent_node):



    child_node = createElementNode(doc, tag, attr)

    parent_node.appendChild(child_node)

# object节点比较特殊

def createObjectNode(doc,attrs):

    object_node = doc.createElement('object')

    createChildNode(doc, 'name', attrs['classification'],
                    object_node)

    createChildNode(doc, 'pose',
                    _POSE, object_node)

    createChildNode(doc, 'truncated',
                    _TRUNCATED, object_node)

    createChildNode(doc, 'difficult',
                    _DIFFICULT, object_node)

    bndbox_node = doc.createElement('bndbox')

    createChildNode(doc, 'xmin', attrs['xmin'],
                    bndbox_node)

    createChildNode(doc, 'ymin', attrs['ymin'],
                    bndbox_node)

    createChildNode(doc, 'xmax', attrs['xmax'],
                    bndbox_node)

    createChildNode(doc, 'ymax', attrs['ymax'],
                    bndbox_node)

    object_node.appendChild(bndbox_node)

    return object_node

# 将documentElement写入XML文件�?
def writeXMLFile(doc,filename):

    tmpfile =open('tmp.xml','w')

    doc.writexml(tmpfile, addindent=''*4,newl = '\n',encoding = 'utf-8')

    tmpfile.close()

    # 删除第一行默认添加的标记

    fin =open('tmp.xml')

    fout =open(filename, 'w')

    lines = fin.readlines()

    for line in lines[1:]:

        if line.split():

         fout.writelines(line)

        # new_lines = ''.join(lines[1:])

        # fout.write(new_lines)

    fin.close()

    fout.close()

def getFileList(path):

    fileList = []
    files = os.listdir(path)
    for f in files:
        if (os.path.isfile(path + '/' + f)):
            fileList.append(f)
    # print len(fileList)
    return fileList


if __name__ == "__main__":

    fileList = getFileList(_TXT_PATH)
    if fileList == 0:
        os._exit(-1)

    current_dirpath = os.path.dirname(os.path.abspath('__file__'))

    if not os.path.exists(_ANNOTATION_SAVE_PATH):
        os.mkdir(_ANNOTATION_SAVE_PATH)

    if not os.path.exists(_IMAGE_COPY_PATH):
        os.mkdir(_IMAGE_COPY_PATH)

    for xText in range(len(fileList)):

        saveName= "%05d" %(xText+1)
        pos = fileList[xText].rfind(".")
        textName = fileList[xText][:pos]

        ouput_file = open(_TXT_PATH + '/' + fileList[xText])
        # ouput_file =open(_TXT_PATH)

        lines = ouput_file.readlines()

        xml_file_name = os.path.join(_ANNOTATION_SAVE_PATH, (saveName + '.xml'))

        img=cv2.imread(os.path.join(_IMAGE_PATH,(textName+'.jpg')))

        height,width,channel=img.shape
        print os.path.join(_IMAGE_COPY_PATH,(textName+'.jpg'))
        cv2.imwrite(os.path.join(_IMAGE_COPY_PATH,(saveName+'.jpg')),img)
        my_dom = xml.dom.getDOMImplementation()

        doc = my_dom.createDocument(None,_ROOT_NODE,None)

        # 获得根节�?
        root_node = doc.documentElement

        # folder节点

        createChildNode(doc, 'folder',_FOLDER_NODE, root_node)

        # filename节点

        createChildNode(doc, 'filename', saveName+'.jpg',root_node)

        # source节点

        source_node = doc.createElement('source')

        # source的子节点

        createChildNode(doc, 'database',_DATABASE_NAME, source_node)

        createChildNode(doc, 'annotation',_ANNOTATION, source_node)

        createChildNode(doc, 'image','flickr', source_node)

        createChildNode(doc, 'flickrid','NULL', source_node)

        root_node.appendChild(source_node)

        # owner节点

        owner_node = doc.createElement('owner')

        # owner的子节点

        createChildNode(doc, 'flickrid','NULL', owner_node)

        createChildNode(doc, 'name',_AUTHOR, owner_node)

        root_node.appendChild(owner_node)

        # size节点

        size_node = doc.createElement('size')

        createChildNode(doc, 'width',str(width), size_node)

        createChildNode(doc, 'height',str(height), size_node)

        createChildNode(doc, 'depth',str(channel), size_node)

        root_node.appendChild(size_node)

        # segmented节点

        createChildNode(doc, 'segmented',_SEGMENTED, root_node)


        for line in lines:

            s = line.rstrip('\n')

            array = s.split()

            print array

            attrs = dict()

            attrs['xmin']= array[0]

            attrs['ymin']= array[1]

            attrs['xmax']= array[2]

            attrs['ymax']= array[3]

            attrs['classification'] = array[4]
            # 构建XML文件名称

            print xml_file_name

            # 创建XML文件

            # createXMLFile(attrs, width, height, xml_file_name)
            # object节点

            object_node = createObjectNode(doc, attrs)

            root_node.appendChild(object_node)

            # 写入文件
            writeXMLFile(doc, xml_file_name)






# #-*- coding:utf-8 -*-
# '''
#     该代码是将数据转为VOC2007，该代码实现了XML生成和图片位置更改以及文件重命名
# '''
#
#
# import xml.dom
# import xml.dom.minidom
# import os
# # from PIL import Image
# import cv2
# # xml文件规范定义
#
#
# _INDENT= ''*4
# _NEW_LINE= '\n'
# _FOLDER_NODE= 'VOC2007'
# _ROOT_NODE= 'annotation'
# _DATABASE_NAME= 'LOGODection'
# _ANNOTATION= 'PASCAL VOC2007'
# _AUTHOR= 'DaZhangFu_CSDN'
# _SEGMENTED= '0'
# _DIFFICULT= '0'
# _TRUNCATED= '0'
# _POSE= 'Unspecified'
#
#
# _ANNOTATION_SAVE_PATH= 'Annotations'
# # _IMAGE_CHANNEL= 3
#
# # 封装创建节点的过�?
# def createElementNode(doc,tag, attr):  # 创建一个元素节�?
#     element_node = doc.createElement(tag)
#
#     # 创建一个文本节�?
#     text_node = doc.createTextNode(attr)
#
#     # 将文本节点作为元素节点的子节�?
#     element_node.appendChild(text_node)
#
#     return element_node
#
#     # 封装添加一个子节点的过�?
# def createChildNode(doc,tag, attr,parent_node):
#
#
#
#     child_node = createElementNode(doc, tag, attr)
#
#     parent_node.appendChild(child_node)
#
# # object节点比较特殊
#
# def createObjectNode(doc,attrs):
#
#     object_node = doc.createElement('object')
#
#     createChildNode(doc, 'name', attrs['classification'],
#                     object_node)
#
#     createChildNode(doc, 'pose',
#                     _POSE, object_node)
#
#     createChildNode(doc, 'truncated',
#                     _TRUNCATED, object_node)
#
#     createChildNode(doc, 'difficult',
#                     _DIFFICULT, object_node)
#
#     bndbox_node = doc.createElement('bndbox')
#
#     createChildNode(doc, 'xmin', attrs['xmin'],
#                     bndbox_node)
#
#     createChildNode(doc, 'ymin', attrs['ymin'],
#                     bndbox_node)
#
#     createChildNode(doc, 'xmax', attrs['xmax'],
#                     bndbox_node)
#
#     createChildNode(doc, 'ymax', attrs['ymax'],
#                     bndbox_node)
#
#     object_node.appendChild(bndbox_node)
#
#     return object_node
#
# # 将documentElement写入XML文件�?
# def writeXMLFile(doc,filename):
#
#     tmpfile =open('tmp.xml','w')
#
#     doc.writexml(tmpfile, addindent=''*4,newl = '\n',encoding = 'utf-8')
#
#     tmpfile.close()
#
#     # 删除第一行默认添加的标记
#
#     fin =open('tmp.xml')
#
#     fout =open(filename, 'w')
#
#     lines = fin.readlines()
#
#     for line in lines[1:]:
#
#         if line.split():
#
#          fout.writelines(line)
#
#         # new_lines = ''.join(lines[1:])
#
#         # fout.write(new_lines)
#
#     fin.close()
#
#     fout.close()
#
#
#
# if __name__ == "__main__":
#     image_info=[['000003',380,500,3],[20,20,100,120,'dog'],[30,15,250,250,'cat']]
#
#     if not os.path.exists(_ANNOTATION_SAVE_PATH):
#         os.mkdir(_ANNOTATION_SAVE_PATH)
#
#
#     saveName= image_info[0][0]
#     lines = image_info[1:]
#
#     xml_file_name = os.path.join(_ANNOTATION_SAVE_PATH, (saveName + '.xml'))
#
#     height,width,channel=image_info[0][1],image_info[0][2],image_info[0][3]
#     my_dom = xml.dom.getDOMImplementation()
#
#     doc = my_dom.createDocument(None,_ROOT_NODE,None)
#
#     # 获得根节�?
#     root_node = doc.documentElement
#
#     # folder节点
#
#     createChildNode(doc, 'folder',_FOLDER_NODE, root_node)
#
#     # filename节点
#
#     createChildNode(doc, 'filename', saveName+'.jpg',root_node)
#
#     # source节点
#
#     source_node = doc.createElement('source')
#
#     # source的子节点
#
#     createChildNode(doc, 'database',_DATABASE_NAME, source_node)
#
#     createChildNode(doc, 'annotation',_ANNOTATION, source_node)
#
#     createChildNode(doc, 'image','flickr', source_node)
#
#     createChildNode(doc, 'flickrid','NULL', source_node)
#
#     root_node.appendChild(source_node)
#
#     # owner节点
#
#     owner_node = doc.createElement('owner')
#
#     # owner的子节点
#
#     createChildNode(doc, 'flickrid','NULL', owner_node)
#
#     createChildNode(doc, 'name',_AUTHOR, owner_node)
#
#     root_node.appendChild(owner_node)
#
#     # size节点
#
#     size_node = doc.createElement('size')
#
#     createChildNode(doc, 'width',str(width), size_node)
#
#     createChildNode(doc, 'height',str(height), size_node)
#
#     createChildNode(doc, 'depth',str(channel), size_node)
#
#     root_node.appendChild(size_node)
#
#     # segmented节点
#
#     createChildNode(doc, 'segmented',_SEGMENTED, root_node)
#
#
#     for line in lines:
#
#         array = line
#
#         attrs = dict()
#
#         attrs['xmin']= "%d"%array[0]
#
#         attrs['ymin']= "%d"%array[1]
#
#         attrs['xmax']= "%d"%array[2]
#
#         attrs['ymax']= "%d"%array[3]
#
#         attrs['classification'] = array[4]
#         # 构建XML文件名称
#
#         print(xml_file_name)
#
#         # 创建XML文件
#
#         # createXMLFile(attrs, width, height, xml_file_name)
#         # object节点
#
#         object_node = createObjectNode(doc, attrs)
#
#         root_node.appendChild(object_node)
#
#         # 写入文件
#
#         writeXMLFile(doc, xml_file_name)
