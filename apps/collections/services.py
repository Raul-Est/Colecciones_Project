# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.



def create_collection(owner, form):
    collection = form.save(commit=False)
    collection.owner = owner
    collection.save()
    return collection


def update_collection(collection, form):
    collection = form.save(commit=False)
    collection.save()
    return collection


def create_item(collection, form):
    item = form.save(commit=False)
    item.collection = collection
    item.save()
    return item


def update_item(item, form):
    item = form.save(commit=False)
    item.save()
    return item

