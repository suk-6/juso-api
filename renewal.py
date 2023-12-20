import os
import os.path as osp
from pprint import pprint
from dotenv import load_dotenv
from urllib.request import urlopen


class app:
    def __init__(self, env) -> None:
        self.env = env
        self.root = osp.dirname(osp.abspath(__file__))

        self.getData()

    def getData(self):
        url = "http://update.juso.go.kr/updateInfo.do"
        params = {
            "app_key": self.env["API_KEY"],
            "cntc_cd": self.env["CNTC_CD"],
            "date_gb": "D",
            "retry_in": "Y",
        }

        if self.env["REQ_DATE"] is not None:
            params["req_dt"] = self.env["REQ_DATE"]

        res = self.get(url, params)
        print(res.getcode())

        while True:
            seq = res.read(2)

            if not seq:
                break

            meta = {
                "seq": seq,
                "baseDate": res.read(8),
                "name": res.read(50).strip().decode(),
                "size": int(res.read(10)),
                "resCode": res.read(5),
                "reqCode": res.read(6),
                "replay": res.read(1),
                "createDate": res.read(8).decode(),
            }
            pprint(meta)

            # 파일 다운로드 경로 지정
            outpath = osp.join(self.root, "export", meta["createDate"][2:8])

            # 파일 다운로드 폴더 생성
            if not os.path.isdir(outpath):
                os.makedirs(outpath)

            # zip파일 데이터 읽기 & 쓰기
            file = res.read(meta["size"] + 10)

            with open(osp.join(outpath, meta["name"]), "wb") as f:
                f.write(file)

    def get(self, url, params):
        url = url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        return urlopen(url)


if __name__ == "__main__":
    load_dotenv()
    env = {
        "API_KEY": os.getenv("API_KEY"),
        "CNTC_CD": os.getenv("CNTC_CD"),
        "REQ_DATE": os.getenv("REQ_DATE"),
    }

    app(env)
