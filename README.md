## PYOCR

### 1 简介：

1. 利用baidu-aip技术，实现OCR等功能;
2. 可视化采用tkinter库

### 2 部署

#### 2.1 安装

#### 2 .2 配置

- 在config/config.py填上你的百度开发者appId，apiKey，secretKey

  ```sh
  config = {
      'appId': '192***06',
      'apiKey': 'MV5F1Ap******nMaxIKGvIp',
      'secretKey': 'bi6xTwV7******dcDZZXirQ8S7Zb'
  }
  ```

- 运行main.py

#### 2.3 生成exe

- 安装pyinstaller

  ```
  pip3 install pyinstaller
  ```

- 进入项目根目录

  ```
  pyinstaller -F main.py
  ```

- 生成可执行文件在根目录下dist文件夹

### 3 效果图

![pyocr001.png](http://img.unionline.top/images/2020/04/10/pyocr001.png)
![pyocr002.png](http://img.unionline.top/images/2020/04/10/pyocr002.png)
![pyocr003.png](http://img.unionline.top/images/2020/04/10/pyocr003.png)
![pyocr004.png](http://img.unionline.top/images/2020/04/10/pyocr004.png)
![pyocr005.png](http://img.unionline.top/images/2020/04/10/pyocr005.png)

### 4 计划开发功能：

- [ ] ~~OCR功能，采用web方式Token操作~~
- [x] 打包成exe软件
- [ ] 关于图片类型细分
  - [ ] General
    - [x] basicGeneral
    - [ ] 高精度
    - [ ] 带位置
    - [ ] 高精度加带位置
  - [ ] webImage
  - [ ] idcard_front
  - [ ] idcard_back
  - [ ] bankcard
  - [ ] drivingLicense
  - [ ] vehicleLicense
  - [ ] licensePlate
  - [ ] businessLicense
- [ ] 开发账号配置窗口
- [ ] 登录验证无数据库版

