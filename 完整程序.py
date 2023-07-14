import os
import shutil #用于删除文件夹，os.rmdir()只能删除空文件夹，shutil.rmtree()更强大
import zipfile

# 重要参数
modelname = '博物馆'
model_dir_path=r'G:\MJ 九江学院博物馆'

# 不删除的文件名，查看盈建科程序打包文件，yjk 2.0.3版本

savedFiles = [modelname+'.pre',modelname+'.rel',modelname+'.yjb',modelname+'.yjk',modelname+'_F.yjc']
savedFiles.append('dsnctrl.ini')
savedFiles.append('fea.dat')
# 以下三项为基础模型文件
savedFiles.append('jccad.pre')
savedFiles.append('Jccad_0')
savedFiles.append('Jccad_0.dat')
# 以下两个文件属于基础前处理文件
savedFiles.append('jcfea.pre')
savedFiles.append('jcdlg.pre')
# jccad，jcdlg,jcfea在‘基础计算及结果输出’文件夹里也有
# 官方打包的是里面的文件，大小更小，我就用外面那个了

# 基础设计所需的上部计算结果文件
# KF.dat 上部结构刚度文件
savedFiles.append('KF.dat')
savedFiles.append('KF.dat.md5')
# 上部前处理计算参数
savedFiles.append('SPara.par')
# 以下两个不知什么用的文件，好像跟基础相关？
savedFiles.append('spretobase.dat')
savedFiles.append('spretobase2.dat')
# 
savedFiles.append('yjkTransLoad.sav')

# 非结构推荐的，好像不包括基础
# savedFiles=["yjkTransLoad.sav","spretobase2.dat","spretobase.dat","SPara.par","fea.dat","dsnctrl.ini","FileName.yjk","FileName.rel","FileName.pre","dsnjc.data"]
model_list =os.listdir(model_dir_path)
for model in model_list:
    model_path = os.path.join(model_dir_path, model)
    flist = os.listdir(model_path) # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
    for f in flist:
        fullpath = model_path + '\\' + f
        # 可以用join方法，效果相同
        # fullpath = os.path.join(fullpath,f)
        if os.path.isdir(fullpath):
            # ‘中间数据’文件夹只保留dsnjc.data
            # dsnjc.data 是上部结构的计算荷载文件，基础读取时用（荷载来源：YJK-A计算荷载）
            # 如果是砌体结构，一般不需要进行整体有限元分析，因此没有此文件。此时基础荷载来源：平面恒活标准值
            if f == '中间数据':
                flist_2 = os.listdir(fullpath)
                for f2 in flist_2:
                    f2path = fullpath + '\\' + f2
                    if os.path.isdir(f2path):
                        shutil.rmtree(f2path)
                    else:
                        if f2 != 'dsnjc.data':
                            os.remove(f2path)
            # 保留整个衬图文件夹
            elif f == '衬图':
                continue
            # 把'jcdlg.pre'和'jcfea.pre'移到外面
            # 还有'jccad.pre'，但有同名文件会报错
            # elif f == '基础计算及结果输出':
            #     # 旧路径(包含文件名)，新路径（只是文件夹名）
            #     file1path = fullpath + '\\' + 'jcdlg.pre'
            #     file2path = fullpath + '\\' + 'jcfea.pre'
            #     # file3path = fullpath + '\\' + 'jccad.pre'
            #     shutil.move(file1path, model_path)
            #     shutil.move(file2path, model_path)
            #     # shutil.move(file3path, model_path)
            #     shutil.rmtree(fullpath)
            else:
                shutil.rmtree(fullpath)
        else:
            if f not in savedFiles:
                fpath = model_path + '\\' + f
                os.remove(fpath)

    # 压缩+打包
    # 注意第三个参数控制是否压缩
    z = zipfile.ZipFile(model_path+'.zip','w',zipfile.ZIP_DEFLATED)
    for i in os.listdir(model_path):
        i_fullpath = os.path.join(model_path,i)
        # 压缩文件
        if os.path.isfile(i_fullpath):
            z.write(i_fullpath,i)
        # 压缩文件夹
        else:
            for j in os.listdir(i_fullpath):
                j_fullpath = os.path.join(i_fullpath,j)
                j_halfpath = os.path.join(i,j)
                # 第二个参数不能使用全路径，否则会出现多层目录
                z.write(j_fullpath,j_halfpath)
    z.close()