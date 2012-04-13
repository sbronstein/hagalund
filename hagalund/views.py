import datetime

def my_view(request):
    request.db.page_hits.insert({"timestamp":datetime.datetime.utcnow()})
    return {'project':'hagalund'}
