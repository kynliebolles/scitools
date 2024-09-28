from flask import Flask, request, render_template, redirect, url_for, flash
import os
import numpy as np
import chardet
from scipy import stats  # 确保正确导入 scipy.stats
from ucrm import calculate_ucrm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB limit
app.config['ALLOWED_EXTENSIONS'] = {'txt'}
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def calculate_statistics(matrix):
    m, n = matrix.shape
    X_mean = np.mean(matrix)  # 总体均值
    row_means = np.mean(matrix, axis=1)  # 行均值
    N = matrix.size  # 总元素数
    
    # 计算单元间方差 M_between (对应Q1)
    M_between = np.sum(n * (row_means - X_mean)**2) / (m - 1)
    
    # 计算单元内方差 M_within (对应Q2)
    M_within = np.sum((matrix - row_means[:, np.newaxis])**2) / (N - m)
    
    # 计算F统计量
    F_statistic = M_between / M_within
    
    # 计算自由度
    df1 = m - 1  # 单元间自由度
    df2 = N - m  # 单元内自由度
    
    alpha = 0.05  # 显著性水平
    F_critical = stats.f.ppf(1 - alpha, df1, df2)
    
    significant_difference = F_statistic > F_critical
    
    # 计算u_bb
    if M_between > M_within:
        s_bb_squared = (M_between - M_within) / n
        u_bb = np.sqrt(s_bb_squared) if s_bb_squared >= 0 else "s_bb_squared为负,请检查M_between和M_within的值。"
    else:
        u_bb = None
    
    return {
        'm': m,
        'n': n,
        'X_mean': X_mean,
        'row_means': row_means,
        'N': N,
        'M_between': M_between,
        'M_within': M_within,
        'df1': df1,
        'df2': df2,
        'F_statistic': F_statistic,
        'F_critical': F_critical,
        'significant_difference': significant_difference,
        'u_bb': u_bb
    }

@app.route('/anova', methods=['GET', 'POST'])
def anova():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # 检测文件编码
            with open(filepath, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
            
            # 使用检测到的编码读取文件
            matrix = np.loadtxt(filepath, delimiter='\t', encoding=encoding)
            
            # 计算统计数据
            results = calculate_statistics(matrix)
            
            return render_template('results.html', results=results)
    return render_template('upload.html')

@app.route('/ucrm', methods=['GET', 'POST'])
def ucrm():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有文件部分')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # 检测文件编码
            with open(filepath, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
            
            # 读取文件数据
            data = {}
            required_keys = ['2SE1', '2SE2', '2SE3', '2SE4', 'VALUE1', 'VALUE2', 'VALUE3', 'VALUE4']
            with open(filepath, 'r', encoding=encoding) as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) < 2:
                        continue
                    key = parts[0]
                    values = [float(x) for x in parts[1:] if x]
                    data[key] = np.array(values)
            
            # 验证所有必需的键是否存在
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                flash(f'文件缺少以下必需的列：{", ".join(missing_keys)}')
                return redirect(request.url)
            
            # 计算 UCRM
            try:
                results = calculate_ucrm(data)
                return render_template('ucrm_results.html', results=results)
            except Exception as e:
                flash(f'计算 UCRM 时发生错误：{str(e)}')
                return redirect(request.url)
    return render_template('ucrm_upload.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, host='127.0.0.1', port=5001)