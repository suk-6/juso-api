import os
import os.path as osp
from db import db
from tqdm import tqdm


class app:
    def __init__(self) -> None:
        self.root = osp.dirname(osp.abspath(__file__))

    def getFileList(self):
        exportPath = osp.join(self.root, "export")

        if not osp.isdir(exportPath):
            os.makedirs(exportPath)
            raise Exception("export 폴더를 생성합니다.\n다시 실행해주세요.")

        files = [
            osp.join(exportPath, file)
            for file in os.listdir(exportPath)
            if file.endswith(".txt")
        ]

        return files

    def getData(self, file):
        with open(file, "r", encoding="EUC-KR") as f:
            data = f.read().split("\n")[:-1]
            data = [line.split("|") for line in data]

        return data

    def insertData(self, filename, data):
        dbconn = db(filename)
        dbconn.initDB()

        for line in tqdm(data):
            dbconn.insertData(line)

    def run(self):
        files = self.getFileList()

        for file in files:
            filename, _ = osp.splitext(osp.basename(file))
            data = self.getData(file)
            self.insertData(filename, data)


if __name__ == "__main__":
    app().run()
