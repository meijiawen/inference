from PIL import Image
from io import BytesIO

import uvicorn
from fastapi import FastAPI, UploadFile, Response

from inference import inferencer

app = FastAPI()

@app.post("/")
async def root(files: UploadFile, response: Response):
    # 推理
    inpainting_result = inferencer(Image.open(files.file))
    
    if not isinstance(inpainting_result, Image.Image):
        response.status_code = 400
        return "result type must be PIL.Image"

    img_byte = BytesIO()
    inpainting_result.save(img_byte, format='JPEG')
    return Response(img_byte.getvalue())

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
