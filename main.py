# encoding: utf-8
from flask import Flask
from flask import request

app = Flask(__name__)

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>银行卡号在线检测工具</title>
    <style>
        @import url(http://fonts.googleapis.com/css?family=Open+Sans:400italic,400,300,600);

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-box-sizing: border-box;
            -moz-box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            -moz-font-smoothing: antialiased;
            -o-font-smoothing: antialiased;
            font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
        }

        body {
            font-family: "Open Sans", Helvetica, Arial, sans-serif;
            font-weight: 300;
            font-size: 12px;
            line-height: 30px;
            color: #777;
            background: #0CF;
        }

        .container {
            max-width: 400px;
            width: 100%;
            margin: 0 auto;
            position: relative;
        }

        #contact input[type="text"], #contact input[type="email"], #contact input[type="tel"], #contact input[type="url"], #contact textarea, #contact button[type="submit"] {
            font: 400 12px/16px "Open Sans", Helvetica, Arial, sans-serif;
        }

        #contact {
            background: #F9F9F9;
            padding: 25px;
            margin: 50px 0;
        }

        #contact h3 {
            color: #F96;
            display: block;
            font-size: 30px;
            font-weight: 400;
        }

        #contact h4 {
            margin: 5px 0 15px;
            display: block;
            font-size: 13px;
        }

        fieldset {
            border: medium none !important;
            margin: 0 0 10px;
            min-width: 100%;
            padding: 0;
            width: 100%;
        }

        #contact input[type="text"], #contact input[type="email"], #contact input[type="tel"], #contact input[type="url"], #contact textarea {
            width: 100%;
            border: 1px solid #CCC;
            background: #FFF;
            margin: 0 0 5px;
            padding: 10px;
        }

        #contact input[type="text"]:hover, #contact input[type="email"]:hover, #contact input[type="tel"]:hover, #contact input[type="url"]:hover, #contact textarea:hover {
            -webkit-transition: border-color 0.3s ease-in-out;
            -moz-transition: border-color 0.3s ease-in-out;
            transition: border-color 0.3s ease-in-out;
            border: 1px solid #AAA;
        }

        #contact textarea {
            height: 100px;
            max-width: 100%;
            resize: none;
        }

        #contact button[type="submit"] {
            cursor: pointer;
            width: 100%;
            border: none;
            background: #0CF;
            color: #FFF;
            margin: 0 0 5px;
            padding: 10px;
            font-size: 15px;
        }

        #contact button[type="submit"]:hover {
            background: #09C;
            -webkit-transition: background 0.3s ease-in-out;
            -moz-transition: background 0.3s ease-in-out;
            transition: background-color 0.3s ease-in-out;
        }

        #contact button[type="submit"]:active {
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
        }

        #contact input:focus, #contact textarea:focus {
            outline: 0;
            border: 1px solid #999;
        }

        ::-webkit-input-placeholder {
            color: #888;
        }

        :-moz-placeholder {
            color: #888;
        }

        ::-moz-placeholder {
            color: #888;
        }

        :-ms-input-placeholder {
            color: #888;
        }

    </style>
</head>
<body>
<div class="container">
    <form id="contact" action="" method="post">
        <h3>信用卡账号生成</h3>
        <h4>符合 mod10 的信用卡账号获取</h4>
        <fieldset>
            <input placeholder="初始信用卡号(16位)" type="text" tabindex="1" required autofocus maxlength="16" name="card_no">
        </fieldset>
        <fieldset>
            <input placeholder="需要的卡号数量/最大为9999" type="text" tabindex="2" required max="10000" maxlength="4" name="num">
        </fieldset>
        <fieldset>
            <input placeholder="号码间隔" type="text" tabindex="1" required autofocus maxlength="4" name="space">
        </fieldset>
        <button name="submit" type="submit" id="contact-submit" data-submit="...Sending">Submit</button>
    </form>
    只被容许在测试阶段使用，禁止使用于非法用途


</div>
</body>
</html>'''


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0


def calculate_luhn(partial_card_number):
    check_digit = luhn_checksum(int(partial_card_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit

def get_t(card_id, num,space):
    if len(card_id) != 16:
        return '请输入16位的卡号'
    else:
        return_list = []
        card_id = int(card_id[0:-1])
        for i in range(1, int(num)+1):
            card_head = card_id+space*i
            return_list.append('%s%s' % (card_head, calculate_luhn(card_head)))
        return '<br>'.join(return_list)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        # url = request.args.get('url')
        # response = requests.get(url)
        # return str(response.headers)
        return html
    else:
        try:
            card_no = request.form['card_no']
            num = request.form['num']
            space = request.form['space']
            return get_t(card_no, num, int(space))

        except Exception as e:
            print e
            return '程序出错,联系 328915139处理'


if __name__ == '__main__':
    app.run('0.0.0.0',port=1090,threaded=True)
