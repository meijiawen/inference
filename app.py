from PIL import Image
from typing import List

import uvicorn
from fastapi import FastAPI, UploadFile, Response

from inference import inferencer

app = FastAPI()


@app.post("/")
async def root(files: UploadFile, response: Response):
    print("First Step")
    classification_result = inferencer(Image.open(files.file))
    if not isinstance(classification_result, List):
        response.status_code = 400
        return "result type must be a list"
    print("Third Step")
    return classification_result


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
