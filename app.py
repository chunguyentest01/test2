from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Mã từ test.py
data = pd.read_csv('test_data.csv')

# Loại bỏ các dòng không hợp lệ
data = data[data['Month'].str.contains('^\w{3}-\d{2}$', regex=True)]

# Chuyển đổi cột 'Month' sang định dạng ngày-tháng
data['Month'] = pd.to_datetime(data['Month'], format='%b-%y')

games = data['Name'].unique()

# Hàm tạo biểu đồ từ test.py
def create_plot(game_data, game_name):
    plt.plot(game_data['Month'], game_data['Avg. Players'], label='Average Players')
    plt.plot(game_data['Month'], game_data['Peak Players'], label='Peak Players')

    plt.title(game_name)
    plt.xlabel('Month')
    plt.ylabel('Number of Players')

    plt.legend()
    plt.grid(True)

    plt.show()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['GET'])
def plot():
    # Tạo biểu đồ từ test.py
    for game in games:
        game_data = data[data['Name'] == game]
        create_plot(game_data, game)

    # Lưu biểu đồ dưới dạng hình ảnh PNG
    image = io.BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)

    # Chuyển đổi hình ảnh thành dữ liệu base64
    encoded_image = base64.b64encode(image.getvalue()).decode('utf-8')

    return jsonify({'image': encoded_image})

if __name__ == '__main__':
    app.run()