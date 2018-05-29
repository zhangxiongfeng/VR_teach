import os
import sys  
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
import numpy as np
import cv2
import tensorflow as tf
#from object_detection.utils import label_map_util
#from object_detection.utils import visualization_utils as vis_util
class Detector(object):
    def __init__(self):
        self.PATH_TO_CKPT = './model/hand_model_faster_rcnn_resnet101.pb'   # 选择模型文件
        self.PATH_TO_LABELS = r'./model/hands_label_map.pbtxt'  # 选择类别标签文件
        self.NUM_CLASSES = 1
        self.detection_graph = self._load_model()   # 加载模型
        #self.category_index = self._load_label_map()
    def _load_model(self):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph
    def _load_label_map(self):
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        #category_index = label_map_util.create_category_index(categories)
        #return category_index
    def detect(self, image):
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image, axis=0)
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    #self.category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)
                
        return image
class DetectUI(QWidget):
     
    def __init__(self):
        super().__init__()
         
        self.initUI()
        #self.detector = Detector()
        self.cap = cv2.VideoCapture()
         
    def initUI(self):  
        self.timer = QTimer(self)   # 初始化一个定时器
        self.timer.timeout.connect(self.showFrame)  # 计时结束调用showFrame()方法
        
        self.show_pic_label = QLabel(self) 
        self.show_pic_label.resize(640, 480)
        self.show_pic_label.move(10, 10)
        self.show_pic_label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgb(255, 170, 0);")            
        self.show_filename_lineEdit = QLineEdit(self) 
        self.show_filename_lineEdit.resize(200, 22)
        self.show_filename_lineEdit.move(10, 500) 
        self.select_img_btn = QPushButton('Select File', self)   
        self.select_img_btn.clicked.connect(self.selectImg) 
        self.select_img_btn.resize(self.select_img_btn.sizeHint())
        self.select_img_btn.move(218, 500) 
        self.open_camera_btn = QPushButton('Open Camera', self)   
        self.open_camera_btn.clicked.connect(self.openCamera) 
        self.open_camera_btn.resize(self.open_camera_btn.sizeHint())
        self.open_camera_btn.move(292, 500)
        self.select_model_btn = QPushButton('Select Model', self)   
        self.select_model_btn.clicked.connect(self.selectModel) 
        self.select_model_btn.resize(self.select_model_btn.sizeHint())
        self.select_model_btn.move(366, 500) 
        self.show_modelname_lineEdit = QLineEdit(self) 
        self.show_modelname_lineEdit.setText('hand_model_faster_rcnn_resnet101.pb')
        self.show_modelname_lineEdit.resize(200, 22)
        self.show_modelname_lineEdit.move(450, 500) 
        self.setGeometry(200, 100, 660, 530)
        self.setWindowTitle('Hand Detector')   
        self.show()

    def showImg(self, src_img, qlabel):
        src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
        # src_img = self.detector.detect(src_img) # 检测目标
        height, width, bytesPerComponent = src_img.shape
        bytesPerLine = bytesPerComponent * width
        # 转为QImage对象
        q_image = QImage(src_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qlabel.setPixmap(QPixmap.fromImage(q_image).scaled(qlabel.width(), qlabel.height())) 
    
    def showFrame(self):
        if(self.cap.isOpened()):
            ret, frame = self.cap.read()
            print (frame)
            if ret:
                self.showImg(frame, self.show_pic_label)
            else:
                self.cap.release()
                self.timer.stop()   # 停止计时器
    
    def selectImg(self):
        if self.cap.isOpened():
            self.cap.release()
        file_name, file_type = QFileDialog.getOpenFileName(self,  
                                    "选取文件",  
                                    "./",  
                                    "Image Files (*.jpg *.png *.bmp *.tif);;Video Files (*.avi *.mp4)")   #设置文件扩展名过滤,注意用双分号间隔过滤，用空格分隔多个文件  
        # print(file_name,file_type)
        if file_type.find("Image") >= 0:
            if file_name:
                self.show_filename_lineEdit.setText(os.path.split(file_name)[1])
            
                img = cv2.imread(file_name, cv2.IMREAD_COLOR)
                cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
                img = self.detector.detect(img) # 检测目标
                height, width, bytesPerComponent = img.shape
                bytesPerLine = bytesPerComponent * width
                # 转为QImage对象
                q_image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
                self.show_pic_label.setPixmap(QPixmap.fromImage(q_image).scaled(self.show_pic_label.width(), self.show_pic_label.height()))

        if file_type.find("Video") >= 0:
            if file_name:
                self.show_filename_lineEdit.setText(os.path.split(file_name)[1])
                self.cap.open(file_name)
                self.timer.start(30)    # 设置时间隔30ms并启动

    def openCamera(self):
        self.cap.open(0)    # 默认打开0号摄像头
        self.timer.start(30)    # 设置时间隔30ms并启动

    def selectModel(self):  
        model_name, file_type = QFileDialog.getOpenFileName(self,  
                                    "选取文件",  
                                    "./",  
                                    "model Files (*.pb);;All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔过滤，用空格分隔多个文件  
        '''       
        if model_name:
            self.show_modelname_lineEdit.setText(os.path.split(model_name)[1])
            self.detector.PATH_TO_CKPT = model_name
            self.detector.detection_graph = self.detector._load_model() # 重新加载模型
        
        '''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dtcui = DetectUI()
    sys.exit(app.exec_())
