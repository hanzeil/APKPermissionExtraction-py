__author__ = 'hanze'
import xml.etree.ElementTree as ET
import os


class PermissionExtraction:
    def __init__(self):
        self.path = "C:/Users/hanze/Documents/Visual Studio 2015/Projects/APKPermissionExtraction/Debug/apk/"
        self.manifest = dict()  # 所有manifest文件目录 appName->appPath
        self.app = dict()  # 应用编号，便于管理 app->No.
        self.app2permission = dict()  # 每个应用的权限集合 appNo->appPermissions
        self.permission = dict()  # 权限编号，便于管理  permission->No.
        self.permissionCount = dict()  # 每个权限出现的个数 permission->count
        self.matrix = [[]]  # 特征矩阵，表示第几个app具有第几个权限，目测这是一个稀疏矩阵，暂时使用邻接矩阵存储

    def start(self):
        """开始执行以下功能
        """
        self.__findAllManifest()
        self.__allPermission()
        self.__countPermission()
        self.__FeatureMatrix()
        self.__print()

    def __findAllManifest(self):
        """找到目录中所有的AndroidManifest.xml文件
        """
        aNum = 0
        for path1 in os.listdir(self.path):
            dir2 = os.path.join(self.path, path1)
            for files in os.listdir(dir2):
                xmlPath = os.path.join(dir2, files + '/AndroidManifest.xml')
                if (os.path.exists(xmlPath)):
                    self.manifest[files] = xmlPath
                    self.app[files] = aNum
                    aNum += 1

    def __allPermission(self):
        """找到所有应用具有的权限,保存在app2permisison变量中
        """
        android = '{http://schemas.android.com/apk/res/android}'
        for files in self.manifest:
            root = ET.parse(self.manifest[files]).getroot()
            appNo = self.app[files]
            if (self.app2permission.get(appNo) == None):
                self.app2permission[appNo] = list()
                # 找到uses-permission label
            for item in root.iter('uses-permission'):
                # 记录在app2permission里
                self.app2permission[appNo].append(item.get(android + 'name'))

    def __countPermission(self):
        """计算所有权限出现的次数
        """
        pNum = 0
        for appNo in self.app2permission:
            for p in self.app2permission[appNo]:
                if (self.permissionCount.get(p) == None):
                    self.permissionCount[p] = 1
                else:
                    self.permissionCount[p] += 1
                if (self.permission.get(p) == None):
                    self.permission[p] = pNum
                    pNum += 1

    def __FeatureMatrix(self):
        """构建特征矩阵
        """
        self.matrix = [[0] * len(self.permission) for i in range(len(self.manifest))]
        number = 0
        for i in range(len(self.matrix)):
            for itemOfPermission in self.app2permission[i]:
                j = self.permission[itemOfPermission]
                self.matrix[i][j] = 1

    def __print(self):
        """打印特征矩阵和permissionCount
        """
        f1 = open('permissionCount.txt', 'w')
        f2 = open('matrix.txt', 'w')
        for item in self.permissionCount:
            f1.write(item)
            f1.write(' ')
            f1.write(str(self.permissionCount[item]))
            f1.write('\n')
        f1.close()
        for line in self.matrix:
            for col in line:
                f2.write(str(col) + ' ')
            f2.write('\n')
        f2.close()
if __name__ == '__main__':
    p = PermissionExtraction()
    p.start()
