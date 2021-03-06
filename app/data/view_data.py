# _*_ coding: utf-8 _*_
import os
import uuid
import datetime
import tornado.gen
import tornado.concurrent

from app.api.html_common import HtmlHandler
from app.configs import configs
from app.common.forms import DataForm
from app.data.Data import Data
from app.data.servlet_data import Servlet_data


class DataHandler(HtmlHandler):
    @tornado.gen.coroutine
    def get(self):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):

        self.html(os.path.join(configs['templates_path'], 'data/data.html'))


# 上传文件
class DataUploadHandler(HtmlHandler):
    @tornado.gen.coroutine
    def get(self):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        self.html(os.path.join(
            configs['templates_path'], 'data/upload_data.html'))

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        res = dict(code=0, msg='失败')
        file_metas = self.request.files.get('file', None)
        form = DataForm(self.form_params)
        if form.validate():
            # 实例化这个data类
            data = Data(
                name=form.data['name'],
                img_path="暂时为空",
                file_path="暂时为空",
                info=form.data['markdown'],
                createAt=datetime.datetime.now(),
                updatedAt=datetime.datetime.now()
            )
            # 将数据传给servlet处理
            servlet = Servlet_data(
                data
            )
            if servlet.process_data():
                # 数据处理成功
                res['code'] = 1
                res['msg'] = '成功'
            else:
                res['code'] = 0
                res['msg'] = '数据库格式要求不符合'
        else:
            # 定义失败接口格式
            res['data'] = form.errors
        self.write(res)

    def check_xsrf_cookie(self):
        # 非常有用的在单页面禁用xsrf_cookie的检查
        return True
