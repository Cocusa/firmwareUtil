from models.models import (
    ERPContext,
    DeviceContext,
    OrderInfo,
)


def is_serial_number_exists(order_info: OrderInfo):
    return (
        order_info is not None
        and order_info.nomenclature != None
        and order_info.nomenclature.id != 0
    )


def is_software_exists(db_context: ERPContext):
    return db_context.software is not None


def is_serial_number_device_valid(context: DeviceContext):
    return (
        context is not None
        and context.serialNumber is not None
        and context.serialNumber != ""
    )
