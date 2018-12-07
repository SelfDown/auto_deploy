"# auto_deploy" 
前端vue项目要部署服务，总是要远程登录，找到目录然后解压

写了一个服务，自动上传，并且解压到固定目录
上传文件是zip包

目录结构

***.zip
   dist
      static
      index.html
      
      
**server 是服务端代码

config.json 定义
   
    "port":8000, 服务器端口

    "upload_path":"E:/file",定义服务器上传目录
    
	  "dest_dir":"E:/file/4d",nginx 部署目录，此目录必须包含dist


**master 是客户端代码

config.json 定义


    "upload_url":"http://127.0.0.1:8000/auto/upload", 服务器上传路径
	
    "deploy_url":"http://127.0.0.1:8000/auto/deploy",服务器部署
	  
    "file_name":"./zip/dist.zip"，本地zip 位置
    
    
 各自dist 包里有对应exe文件，直接可用
