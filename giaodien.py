import pyodbc
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Cấu hình kết nối
server = 'NNTHAI\\SQLEXPRESS'  # Tên hoặc địa chỉ IP của server SQL
database = 'datagiaxe'  # Tên cơ sở dữ liệu
username = 'nnt'  # Tên người dùng SQL
password = '12345'  # Mật khẩu của người dùng SQL

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

templates = Jinja2Templates(directory="templates")


class InputData(BaseModel):
    id: int
    mauxe: str
    giadexuat: str
    giabanuudai: str


@app.get("/ ", response_class=HTMLResponse)
async def get_data(request: Request):
    connection = None
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT id, mauxe, giadexuat, giabanuudai FROM bang1;")
        rows = cursor.fetchall()

        data = []
        for row in rows:
            id_value = row[0]
            mauxe_value = row[1]
            giadexuat_value = row[2]
            giabanuudai_value = row[3]

            # Kiểm tra giá trị của mauxe
            if mauxe_value is not None:
                # Tạo đối tượng InputData chỉ khi mauxe không phải là null
                data.append(InputData(id=id_value, mauxe=mauxe_value, giadexuat=giadexuat_value, giabanuudai=giabanuudai_value))
            else:
                # Xử lý trường hợp mauxe là null (ví dụ: bỏ qua hoặc gán giá trị mặc định)
                # Ví dụ: bỏ qua dòng dữ liệu này
                pass

        return templates.TemplateResponse("web.html", {"request": request, "data": data})

    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.1.137", port=8080)
