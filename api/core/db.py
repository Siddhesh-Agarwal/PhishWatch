import pymongo

from models.Response import Response, ResponseDict


def search_data(url: str, uri: str) -> Response | None:
    """
    search_data searches the database for the given URL.

    Parameters
    ----------
    url : str
        The URL to search for.
    uri : str
        The URI of the MongoDB database.

    Returns
    -------
    Response | None
        The Response object if the URL is found, None otherwise.
    """

    client = pymongo.MongoClient(uri)  # type: ignore
    db = client["admin"]  # type: ignore
    collection = db["phishing"]  # type: ignore
    data: ResponseDict | None = collection.find_one({"url": url})  # type: ignore
    client.close()
    if data is None:
        return None
    return Response.model_construct(data)  # type: ignore


def add_data(data: Response, uri: str) -> None:
    """
    add_data adds the given data to the database.

    Parameters
    ----------
    data : Response
        The data to add.
    uri : str
        The URI of the MongoDB database.
    """

    res: Response | None = search_data(str(data.url), uri)
    client = pymongo.MongoClient(uri)  # type: ignore
    db = client["admin"]  # type: ignore
    collection = db["phishing"]  # type: ignore
    if res is None:
        collection.insert_one(data.model_dump())  # type: ignore
    else:
        collection.update_one({"url": str(data.url)}, {"$set": data.model_dump()})
    client.close()
