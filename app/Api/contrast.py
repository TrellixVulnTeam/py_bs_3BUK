from flask import Blueprint, make_response, request  # type:request
from flask_cors import CORS  # type: CORS
# from app.Model.models import MeiTuan_Move_Info as MT
from app.Model.models import MeiTuan_Move_Info_V2 as MT
from app.utils.message import response_info
from app.Global import CATEGORIES_ID_DATA, AREA_DATA, BAIYUN_AREA
import pandas as pd  # type: pd
from app.exts import db

contrast = Blueprint("contrast", __name__)
CORS(contrast, supports_credentials=True)


# baiyun = pd.read_excel('../static/baiyunpoi_80.xls')
# 对比
@contrast.route("/test/")
def test():
    def split_addr(data):
        addr = data['CITY'] + data['DISTRICT'] + data['TOWN'] + data['VILLAGE'] + data['STREET'] + data['DOORPN']
        return addr

    # addr_list = baiyun.apply(split_addr, axis=1).to_list()
    # print(addr_list)
    return response_info(msg='1')


@contrast.route("/test2/")
def test2():
    return "Hello Flask"


@contrast.route("/single_contr")
def single_contrast():
    if request.method == "GET":
        query = request.args.get("single")
        lat = request.args.get("lat")
        lng = request.args.get("lng")
        result = MT.query.filter(MT.areaName.in_(BAIYUN_AREA)).filter(MT.name.like(f"%{query}%"))
        query_list = []
        layer_list = [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(lng), float(lat)]
                },
                "size": 30,
                "color": "red"
            }
        ]
        for r in result:
            query_list.append(
                {
                    "name": r.name,
                    "addr": r.addr,
                    "date": r.datetime,
                    "areaName": r.areaName,
                }
            )
            layer_list.append(
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(r.lng), float(r.lat)]
                    },
                    "size": 10,
                    "color": "green"
                }
            )
        return response_info(msg="1", data={"query_list": query_list, "layer_list": layer_list})
    return response_info(msg="2")
