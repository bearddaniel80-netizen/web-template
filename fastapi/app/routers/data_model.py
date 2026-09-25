from pydantic import BaseModel

class FileList(BaseModel):
    name: str
 
    def to_dict(self):
        return {
            "name": self.name
        }

class UploadUrlRequest(BaseModel):
    content_type: str
    filename: str