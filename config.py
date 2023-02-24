from os.path import abspath

from pydantic import BaseModel, Field, validator


class Config(BaseModel):
    host: str = Field("0.0.0.0", const=True)
    port: int = Field(8080, const=True, ge=1, le=65535)


class AllowPath(BaseModel):
    root: str = Field("..")
    allow: list[str] = Field([".."])
    exclude: list[str] = Field(["."])

    @validator("root", always=True)
    def path_validator(cls, value: str):
        return abspath(value)

    @validator("allow", "exclude", always=True)
    def path_list_validator(cls, values: list[str]):
        return list(map(abspath, values))


try:
    CONFIG = Config.parse_raw(open("config.json").read())
except:
    CONFIG = Config()

try:
    ALLOW_PATH = AllowPath.parse_raw(open("allow_path.json").read())
except:
    ALLOW_PATH = AllowPath()

open("config.json", mode="w").write(CONFIG.json(ensure_ascii=False, indent=2))
open("allow_path.json", mode="w").write(ALLOW_PATH.json(ensure_ascii=False, indent=2))
