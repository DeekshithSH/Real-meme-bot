from aiohttp import web
from Bot.utils.Translation import Names
from Bot.utils.database import Database
db = Database()

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    return web.json_response(
        {
            "server_status": "running"
        }
    )


@routes.get("/devices", allow_head=True)
async def root_route_handler(_):
    data={}
    device = await db.get_db_names()
    for x in device:
        data[str(x)]=Names.Device.get(x, x)

    return web.json_response(data)

@routes.get("/types", allow_head=True)
async def root_route_handler(request: web.Request):
    device=request.query.get("device")
    collection = await db.get_col_names(str(device))

    return web.json_response(collection)

@routes.get("/builds", allow_head=True)
async def root_route_handler(request: web.Request):
    device=request.query.get("device")
    build_type=request.query.get("type")
    builds = await db.get_doc_names(str(device), str(build_type))

    return web.json_response(builds)

# versions?device=${FormDevice.value}&type=${FormType.value}&name=${FormBuild}
@routes.get("/versions", allow_head=True)
async def root_route_handler(request: web.Request):
    data=[]
    device=request.query.get("device")
    build_type=request.query.get("type")
    name=request.query.get("name")
    print((device, build_type, name))
    builds = await db.get_file_byname(str(device), str(build_type), str(name))
    async for x in builds:
        lite_data={
            "_id":str(x.get("_id")),
            "name": str(x.get("name")),
            "type": str(x.get("type")),
            "version": str(x.get("version")),
            "status": str(x.get("status")),
            "release_date": str((x.get("release_date")).strftime("%d-%m-%Y")),
            "dev": str(x.get("dev"))
            }
        data.append(lite_data)
    return web.json_response(data)

@routes.get("/file", allow_head=True)
async def root_route_handler(request: web.Request):
    device=request.query.get("device")
    build_type=request.query.get("type")
    id=request.query.get("id")
    builds = dict(await db.get_file_byid(str(device), str(build_type), str(id)))
    builds.pop("_id")
    builds.pop("device")
    builds.pop("type")
    builds["release_date"]=str((builds.get("release_date")).strftime("%d-%m-%Y")),

    return web.json_response(builds)